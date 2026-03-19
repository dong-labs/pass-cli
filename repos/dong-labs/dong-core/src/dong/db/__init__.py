"""数据库基础模块

提供统一的数据库管理基类。
"""

from dong.db.database import Database
from dong.db.schema import SchemaManager

__all__ = ["Database", "SchemaManager"]
