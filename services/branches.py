import json
import os
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
BRANCHES_PATH = BASE_DIR / "data" / "branches.json"
EXTERNAL_BRANCHES_PATH = os.getenv("ECASH_BRANCHES_PATH")

DEFAULT_BRANCHES: dict[str, Any] = {
    "almaty": {
        "name": "Алматы",
        "branches": {
            "zeleny_bazar": {
                "name": "Зеленый базар",
                "address": "Проспект Жибек Жолы, 53",
                "api_depcode": "ЗЕЛЕНЫЙ БАЗАР",
                "landmark": "Возле мясного павильона",
                "schedule": "9:00 до 18:30",
                "map_url": "",
                "manager_phone": "8-700-333-22-23",
            },
            "grand_park": {
                "name": "Гранд парк",
                "address": "Кабдолова улица, 1/4 Б",
                "api_depcode": "ГРАНД ПАРК",
                "landmark": "Между 6 и 7 блоком, вход с улицы, рядом с Kaz Tour",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-705-908-90-73",
            },
            "mega_park": {
                "name": "Mega Park",
                "address": "Улица Макатаева, 127/1",
                "api_depcode": "MEGA PARK",
                "landmark": "Цокольный этаж, рядом с Magnum, возле эскалатора",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-707-444-88-84",
            },
            "forum": {
                "name": "Forum",
                "address": "Проспект Сейфуллина, 617",
                "api_depcode": "FORUM",
                "landmark": "Цокольный этаж, рядом с эскалатором, уровень паркинга -1",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-777-304-40-74",
            },
            "aport1": {
                "name": "Апорт1",
                "address": "https://2gis.kz/almaty/geo/9430047375099302",
                "api_depcode": "АПОРТ",
                "landmark": "1 этаж, рядом с Kaspi Bank",
                "schedule": "10:00 до 22:00",
                "map_url": "https://2gis.kz/almaty/geo/9430047375099302",
                "manager_phone": "8-705-867-06-92",
            },
            "aport2": {
                "name": "Апорт2",
                "address": "https://2gis.kz/almaty/geo/9430047375099302",
                "api_depcode": "АПОРТ2",
                "landmark": "Возле Miami Spa, аквапарка и Funky World",
                "schedule": "10:00 до 22:00",
                "map_url": "https://2gis.kz/almaty/geo/9430047375099302",
                "manager_phone": "8-705-867-06-92",
            },
            "almaty_mall": {
                "name": "Almaty Mall",
                "address": "Ораза Жандосова улица, 83",
                "api_depcode": "ALMATY MALL",
                "landmark": "1 этаж, напротив Navat, рядом с банкоматами и магазином «Детский мир»",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-700-333-22-23",
            },
            "sputnik": {
                "name": "Спутник",
                "address": "Микрорайон Мамыр-1, 8а",
                "api_depcode": "Спутник",
                "landmark": "Цокольный этаж, рядом с банкоматами",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-700-333-22-23",
            },
            "ritz_palace": {
                "name": "Ритц палас",
                "address": "https://2gis.kz/almaty/geo/9430047375176289",
                "api_depcode": "Ритц-Палас",
                "landmark": "1 этаж, рядом с Magnum",
                "schedule": "10:00 до 22:00",
                "map_url": "https://2gis.kz/almaty/geo/9430047375176289",
                "manager_phone": "8-700-333-22-23",
            },
        },
    },
    "astana": {
        "name": "Астана",
        "branches": {
            "saryarka": {
                "name": "Сарыарка",
                "address": "Проспект Туран, 24",
                "api_depcode": "САРЫАРКА",
                "landmark": "Цокольный этаж, банкоматная зона",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-707-460-88-38",
            },
            "khan_shatyr": {
                "name": "Хан Шатыр",
                "address": "Проспект Туран, 37",
                "api_depcode": "ХАНШАТЫР",
                "landmark": "Цокольный этаж, рядом с магазином Candy Shop",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-707-895-88-86",
            },
            "asia_park": {
                "name": "Азия парк",
                "address": "Кабанбай батыр проспект, 21",
                "api_depcode": "ASIA PARK",
                "landmark": "1 этаж, рядом с «Цветной аптекой»",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "",
            },
            "eurasia": {
                "name": "Евразия",
                "address": "Улица Алексея Петрова, 24а/1",
                "api_depcode": "EURASIA",
                "landmark": "ТЦ «Евразия-3», вход со стороны ул. Жеринтаева, 1 этаж, рядом с ювелирным магазином",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-707-895-88-86",
            },
            "aruzhan": {
                "name": "Аружан",
                "address": "Илияса Жансугурова улица, 8/1",
                "api_depcode": "АРУЖАН",
                "landmark": "1 этаж, рядом с Home Credit Bank",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-700-333-22-23",
            },
            "abu_dhabi": {
                "name": "Абу даби",
                "address": "Улица Сыганак, 60/5",
                "api_depcode": "ABU DHABI",
                "landmark": "1 этаж, напротив магазина «galmart», рядом с банкоматами",
                "schedule": "10:00 до 22:00",
                "map_url": "",
                "manager_phone": "8-700-333-22-23",
            },
        },
    },
    "aktobe": {
        "name": "Актобе",
        "branches": {
            "aktobe_ecash": {
                "name": "Актобе Ecash",
                "address": "Проспект Алии Молдагуловой, 50в",
                "api_depcode": "AKTOBE",
                "landmark": "слева от здания Капитал Плаза, напротив гипермаркета «Дина»",
                "schedule": "9:00 до 20:00",
                "map_url": "",
                "manager_phone": "8-700-333-22-23, 8-747-297-04-04, 8-747-517-07-94",
            }
        },
    },
}


def _load_external_branches() -> dict[str, Any] | None:
    if not EXTERNAL_BRANCHES_PATH:
        return None
    path = Path(EXTERNAL_BRANCHES_PATH)
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict) and data:
            return data
    except (json.JSONDecodeError, OSError):
        return None
    return None


def load_branches() -> dict[str, Any]:
    external = _load_external_branches()
    if external:
        return external
    if BRANCHES_PATH.exists():
        try:
            with BRANCHES_PATH.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if data:
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_BRANCHES


def get_branch_info(branch_id: str | None) -> dict[str, Any] | None:
    if not branch_id:
        return None
    for city_data in load_branches().values():
        if branch_id in city_data.get("branches", {}):
            return city_data["branches"][branch_id]
    return None


def get_branch_display(branch_id: str | None) -> str:
    branch = get_branch_info(branch_id)
    if not branch:
        return "Не выбран"
    city_name = ""
    for city_id, city_data in load_branches().items():
        if branch_id in city_data.get("branches", {}):
            city_name = city_data.get("name", city_id)
            break
    if city_name and branch.get("name"):
        return f"{city_name} · {branch['name']}"
    return branch.get("name") or "Не выбран"


def get_branch_location(branch_id: str | None) -> tuple[str | None, str | None, str | None, str | None]:
    branch = get_branch_info(branch_id)
    if not branch:
        return None, None, None, None
    return branch.get("address"), branch.get("landmark"), branch.get("schedule"), branch.get("map_url")


def get_city_name(city_id: str | None) -> str | None:
    if not city_id:
        return None
    data = load_branches()
    city_info = data.get(city_id)
    return city_info.get("name") if city_info else None
