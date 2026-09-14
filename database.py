import logging
from datetime import datetime
from typing import Any

import aiosqlite

from config import DB_PATH


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                phone TEXT,
                city_id TEXT,
                branch_id TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER,
                application_type TEXT,
                branch_id TEXT,
                data_json TEXT,
                status TEXT,
                created_at TEXT
            )
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rate_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER,
                branch_id TEXT,
                currency_code TEXT,
                rate_type TEXT,
                condition_type TEXT,
                target_rate TEXT,
                is_active INTEGER,
                created_at TEXT,
                notified_at TEXT
            )
            """
        )
        cursor = await conn.execute("PRAGMA table_info(users)")
        user_columns = {row[1] for row in await cursor.fetchall()}
        if "language" not in user_columns:
            await conn.execute("ALTER TABLE users ADD COLUMN language TEXT")
        await conn.commit()


async def get_user_language(telegram_user_id: int) -> str | None:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT language FROM users WHERE telegram_user_id = ?", (telegram_user_id,))
        row = await cursor.fetchone()
    return row[0] if row else None


async def set_user_language(telegram_user_id: int, language: str) -> None:
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            """
            INSERT INTO users (telegram_user_id, language, created_at, updated_at) VALUES (?, ?, ?, ?)
            ON CONFLICT(telegram_user_id) DO UPDATE SET
                language=excluded.language,
                updated_at=excluded.updated_at
            """,
            (telegram_user_id, language, now, now),
        )
        await conn.commit()


async def save_or_update_user(telegram_user_id: int, username: str | None, full_name: str | None, phone: str | None, city_id: str | None, branch_id: str | None) -> None:
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            """
            INSERT INTO users (
                telegram_user_id, username, full_name, phone, city_id, branch_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(telegram_user_id) DO UPDATE SET
                username=excluded.username,
                full_name=excluded.full_name,
                phone=excluded.phone,
                city_id=excluded.city_id,
                branch_id=excluded.branch_id,
                updated_at=excluded.updated_at
            """,
            (telegram_user_id, username, full_name, phone, city_id, branch_id, now, now),
        )
        await conn.commit()


async def get_user(telegram_user_id: int) -> dict[str, Any] | None:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT telegram_user_id, username, full_name, phone, city_id, branch_id, created_at, updated_at FROM users WHERE telegram_user_id = ?",
            (telegram_user_id,),
        )
        row = await cursor.fetchone()
    if row is None:
        return None
    return {
        "telegram_user_id": row[0],
        "username": row[1],
        "full_name": row[2],
        "phone": row[3],
        "city_id": row[4],
        "branch_id": row[5],
        "created_at": row[6],
        "updated_at": row[7],
    }


async def save_application(telegram_user_id: int, application_type: str, branch_id: str | None, data: dict[str, Any], status: str = "new") -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT INTO applications (telegram_user_id, application_type, branch_id, data_json, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (telegram_user_id, application_type, branch_id, str(data), status, datetime.utcnow().isoformat()),
        )
        await conn.commit()


async def add_rate_alert(telegram_user_id: int, branch_id: str, currency_code: str, rate_type: str, condition_type: str, target_rate: str) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT INTO rate_alerts (telegram_user_id, branch_id, currency_code, rate_type, condition_type, target_rate, is_active, created_at, notified_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (telegram_user_id, branch_id, currency_code, rate_type, condition_type, target_rate, 1, datetime.utcnow().isoformat(), None),
        )
        await conn.commit()


async def list_rate_alerts(telegram_user_id: int) -> list[dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT id, telegram_user_id, branch_id, currency_code, rate_type, condition_type, target_rate, is_active FROM rate_alerts WHERE telegram_user_id = ? ORDER BY id DESC",
            (telegram_user_id,),
        )
        rows = await cursor.fetchall()
    return [
        {
            "id": row[0],
            "telegram_user_id": row[1],
            "branch_id": row[2],
            "currency_code": row[3],
            "rate_type": row[4],
            "condition_type": row[5],
            "target_rate": row[6],
            "is_active": bool(row[7]),
        }
        for row in rows
    ]


async def list_active_rate_alerts() -> list[dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT id, telegram_user_id, branch_id, currency_code, rate_type, condition_type, target_rate, is_active FROM rate_alerts WHERE is_active = 1 ORDER BY id DESC"
        )
        rows = await cursor.fetchall()
    return [
        {
            "id": row[0],
            "telegram_user_id": row[1],
            "branch_id": row[2],
            "currency_code": row[3],
            "rate_type": row[4],
            "condition_type": row[5],
            "target_rate": row[6],
            "is_active": bool(row[7]),
        }
        for row in rows
    ]


async def deactivate_rate_alert(alert_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE rate_alerts SET is_active = 0, notified_at = ? WHERE id = ?",
            (datetime.utcnow().isoformat(), alert_id),
        )
        await conn.commit()


async def deactivate_all_alerts(telegram_user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE rate_alerts SET is_active = 0, notified_at = ? WHERE telegram_user_id = ?",
            (datetime.utcnow().isoformat(), telegram_user_id),
        )
        await conn.commit()
