"""数据库连接管理基类

提供统一的 SQLite 数据库管理。

所有咚咚家族 CLI 共享 ~/.dong/ 目录。
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterator, Optional
from contextlib import contextmanager


# 统一数据目录
DONG_DIR = Path.home() / ".dong"


class Database:
    """
    数据库管理基类

    子类需要实现：
    - get_name(): 返回 CLI 名称

    数据库路径: ~/.dong/<name>/<name>.db
    """

    _connection: Optional[sqlite3.Connection] = None

    @classmethod
    def get_name(cls) -> str:
        """返回 CLI 名称（子类必须实现）"""
        raise NotImplementedError

    @classmethod
    def get_dong_dir(cls) -> Path:
        """获取咚咚家族统一目录"""
        return DONG_DIR

    @classmethod
    def get_module_dir(cls) -> Path:
        """获取模块目录 ~/.dong/<name>/"""
        name = cls.get_name()
        module_dir = DONG_DIR / name
        module_dir.mkdir(parents=True, exist_ok=True)
        return module_dir

    @classmethod
    def get_db_path(cls) -> Path:
        """获取数据库文件路径 ~/.dong/<name>/<name>.db"""
        name = cls.get_name()
        module_dir = cls.get_module_dir()
        return module_dir / f"{name}.db"
    
    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """获取数据库连接（单例）"""
        if cls._connection is None:
            db_path = cls.get_db_path()
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            cls._connection = sqlite3.connect(
                str(db_path),
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            cls._connection.row_factory = sqlite3.Row
        
        return cls._connection
    
    @classmethod
    def close_connection(cls) -> None:
        """关闭数据库连接"""
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
    
    @classmethod
    @contextmanager
    def get_cursor(cls) -> Iterator[sqlite3.Cursor]:
        """获取数据库游标的上下文管理器"""
        conn = cls.get_connection()
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    
    @classmethod
    def get_meta(cls, key: str, default: Any = None) -> Any:
        """获取元数据"""
        with cls.get_cursor() as cur:
            cur.execute(
                "SELECT value FROM __meta WHERE key = ?",
                (key,)
            )
            row = cur.fetchone()
            return row["value"] if row else default
    
    @classmethod
    def set_meta(cls, key: str, value: Any) -> None:
        """设置元数据"""
        with cls.get_cursor() as cur:
            cur.execute(
                """INSERT OR REPLACE INTO __meta (key, value)
                   VALUES (?, ?)""",
                (key, value)
            )
    
    @classmethod
    def ensure_meta_table(cls) -> None:
        """确保元数据表存在"""
        with cls.get_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS __meta (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
