"""数据库连接管理"""

import sqlite3
from pathlib import Path
from typing import Iterator
from contextlib import contextmanager
from dong.db import Database as DongDatabase


class MemberDatabase(DongDatabase):
    """会员咚数据库类"""

    @classmethod
    def get_name(cls) -> str:
        return "member"


@contextmanager
def get_cursor() -> Iterator[sqlite3.Cursor]:
    """获取数据库游标"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def get_connection() -> sqlite3.Connection:
    """获取数据库连接"""
    return MemberDatabase.get_connection()


def get_db_path() -> Path:
    """获取数据库路径"""
    return MemberDatabase.get_db_path()


def close_connection():
    """关闭数据库连接"""
    MemberDatabase.close_connection()
