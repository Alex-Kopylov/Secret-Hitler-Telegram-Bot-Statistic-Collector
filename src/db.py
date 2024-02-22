import asyncio
from collections.abc import Iterable
from typing import Any, LiteralString
import aiosqlite
from src import config


async def get_db() -> aiosqlite.Connection:
    if not getattr(get_db, "db", None):
        db = await aiosqlite.connect(config.SQLITE_DB_FILE_PATH,
                                     timeout=60 * 60 * 24 * 1  # 1 day
                                     )
        get_db.db = db

    return get_db.db


async def fetch_all(
        sql: LiteralString, params: Iterable[Any] | None = None
) -> list[dict]:
    cursor = await _get_cursor(sql, params)
    rows = await cursor.fetchall()
    results = [_get_result_with_column_names(cursor, row) for row in rows]
    await cursor.close()
    return results


async def fetch_one(
        sql: LiteralString, params: Iterable[Any] | None = None
) -> dict | None:
    cursor = await _get_cursor(sql, params)
    row = await cursor.fetchone()
    result = _get_result_with_column_names(cursor, row) if row else None
    await cursor.close()
    return result


async def execute(
        sql: LiteralString, params: Iterable[Any] | None = None, *, autocommit: bool = True
) -> None:
    db = await get_db()
    await db.execute(sql, params)
    if autocommit:
        await db.commit()


def close_db() -> None:
    asyncio.run(_async_close_db())


async def _async_close_db() -> None:
    await (await get_db()).close()


async def _get_cursor(
        sql: LiteralString, params: Iterable[Any] | None
) -> aiosqlite.Cursor:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(sql, params)
    return cursor


def _get_result_with_column_names(cursor: aiosqlite.Cursor, row: aiosqlite.Row) -> dict:
    column_names = [d[0] for d in cursor.description]
    return {column_name: row[index] for index, column_name in enumerate(column_names)}
