"""数据库 Schema 管理"""

from dong.db import SchemaManager
from .connection import MemberDatabase

SCHEMA_VERSION = "1.2.0"


class MemberSchemaManager(SchemaManager):
    """会员咚 Schema 管理器"""

    def __init__(self):
        super().__init__(
            db_class=MemberDatabase,
            current_version=SCHEMA_VERSION
        )

    def init_schema(self) -> None:
        self._create_members_table()
        self._create_renewals_table()
        self._create_indexes()

    def _create_members_table(self) -> None:
        with MemberDatabase.get_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    wechat TEXT,
                    phone TEXT,
                    email TEXT,
                    account_id TEXT,
                    member_type TEXT DEFAULT 'yearly',
                    project TEXT DEFAULT 'donglijuan',
                    join_date TEXT NOT NULL,
                    expire_date TEXT,
                    price REAL,
                    currency TEXT DEFAULT 'CNY',
                    status TEXT DEFAULT 'active',
                    source TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def _create_renewals_table(self) -> None:
        with MemberDatabase.get_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS renewals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    old_date TEXT,
                    new_date TEXT,
                    price REAL,
                    months INTEGER,
                    renewed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (member_id) REFERENCES members(id)
                )
            """)

    def _create_indexes(self) -> None:
        with MemberDatabase.get_cursor() as cur:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_members_expire ON members(expire_date)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_members_status ON members(status)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_members_wechat ON members(wechat)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_members_account ON members(account_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_members_project ON members(project)")


def init_database():
    """初始化数据库"""
    manager = MemberSchemaManager()
    manager.init_schema()
    return {"message": "数据库初始化成功", "version": SCHEMA_VERSION}


def is_initialized() -> bool:
    """检查数据库是否已初始化"""
    db_path = MemberDatabase.get_db_path()
    if not db_path.exists():
        return False
    
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='members'")
        result = cur.fetchone() is not None
        conn.close()
        return result
    except Exception:
        return False
