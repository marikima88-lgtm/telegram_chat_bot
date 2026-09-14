import json
import logging
import os
import time
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import aiohttp


class RateProvider:
    def __init__(self, data_path: str | None = None, branches_path: str | None = None) -> None:
        base_dir = Path(__file__).resolve().parents[1]
        self.data_path = Path(data_path) if data_path else base_dir / "data" / "currencies.json"
        self.branches_path = Path(branches_path) if branches_path else base_dir / "data" / "branches.json"
        self._fallback_data = self._load_fallback_data()
        self._cache: dict[str, dict[str, Any]] = {}
        self._cache_ttl_seconds = 300
        self._logger = logging.getLogger(__name__)

    def _load_fallback_data(self) -> dict[str, Any]:
        with self.data_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _load_branches(self) -> dict[str, Any]:
        with self.branches_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _resolve_branch_config(self, branch_id: str) -> dict[str, Any]:
        for city in self._load_branches().values():
            branches = city.get("branches", {})
            if branch_id in branches:
                return branches[branch_id]
        return {}

    async def _fetch_live_rates(self, branch_id: str) -> dict[str, Any] | None:
        branch_config = self._resolve_branch_config(branch_id)
        depcode = branch_config.get("api_depcode") or branch_id
        token = os.getenv("QUIQ_API_TOKEN", "").strip()

        cache_bust = int(time.time() * 1000)
        url = f"https://api.quiq.kz/Department/getDepsLandingInfo?cache_bust={cache_bust}"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Auth2": "Code",
            "Origin": "https://ecash.kz",
            "Referer": "https://ecash.kz/",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
            ),
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            ssl = False
            connector = aiohttp.TCPConnector(ssl=ssl)
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10), connector=connector) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        self._logger.warning("Quiq API вернул статус %s", response.status)
                        return None
                    payload = await response.json()
        except Exception as exc:
            self._logger.warning("Не удалось получить курсы из Quiq API: %s", exc)
            return None

        for branch_data in payload or []:
            candidate_code = str(branch_data.get("depcode", "")).upper()
            if depcode and str(depcode).upper() != candidate_code:
                continue
            if not depcode and branch_data.get("isActive") == 0:
                continue
            return self._normalize_api_payload(branch_data)

        if not depcode and payload:
            first_entry = next((item for item in payload if item.get("isActive") != 0), None)
            if first_entry is not None:
                return self._normalize_api_payload(first_entry)

        return None

    _EXCLUDED_GOLD_CODES = {"GOLD5", "GOLD10", "GOLD20", "GOLD50", "GOLD100"}

    def _normalize_api_payload(self, branch_data: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for currency in branch_data.get("currencies", []):
            if not currency.get("isActive"):
                continue
            code = currency.get("code", "").upper()
            if code in self._EXCLUDED_GOLD_CODES:
                continue
            rate_list = currency.get("rateList") or []
            if not rate_list:
                continue
            rate_item = rate_list[0]
            result[code] = {
                "name": currency.get("description") or currency.get("code", ""),
                "buy": Decimal(str(rate_item.get("buy", 0))),
                "sell": Decimal(str(rate_item.get("sale", 0))),
                "updated_at": datetime.utcnow().strftime("%H:%M"),
                "source": "api",
            }
        return result

    async def _load_rates_for_branch(self, branch_id: str) -> dict[str, Any]:
        now = time.time()
        cached = self._cache.get(branch_id)
        if cached and cached.get("expires_at", 0) > now:
            return cached["data"]

        live_data = await self._fetch_live_rates(branch_id)
        if live_data:
            self._cache[branch_id] = {"data": live_data, "expires_at": now + self._cache_ttl_seconds}
            return live_data

        fallback_data = self._fallback_data.get(branch_id, {})
        self._cache[branch_id] = {"data": fallback_data, "expires_at": now + self._cache_ttl_seconds}
        return fallback_data

    async def get_rate(self, branch_id: str, currency_code: str) -> dict[str, Any] | None:
        branch_data = await self._load_rates_for_branch(branch_id)
        return branch_data.get(currency_code.upper())

    async def get_all_rates(self, branch_id: str) -> dict[str, Any]:
        return await self._load_rates_for_branch(branch_id)

    def format_rate(self, rate: dict[str, Any], currency_code: str) -> str:
        buy = Decimal(str(rate["buy"]))
        sell = Decimal(str(rate["sell"]))
        return (
            f"{currency_code} — {rate.get('name', currency_code)}\n\n"
            f"Покупка: {buy.quantize(Decimal('1'))} ₸\n"
            f"Продажа: {sell.quantize(Decimal('1'))} ₸"
        )
