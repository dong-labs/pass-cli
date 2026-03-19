"""数据库 Schema 管理基类

提供统一的 Schema 版本管理。
"""

from typing import Type, TypeVar, Optional
from dong.db.database import Database

T = TypeVar('T', bound=Database)


class SchemaManager:
    """
    Schema 管理基类
    
    子类需要实现：
    - init_schema(): 创建所有表和索引
    
    管理数据库 schema 的版本，支持初始化和迁移检查。
    """
    
    VERSION_KEY = "schema_version"
    
    def __init__(self, db_class: Type[T], current_version: str):
        """
        初始化 Schema 管理器
        
        Args:
            db_class: 数据库类
            current_version: 当前 schema 版本
        """
        self.db_class = db_class
        self.current_version = current_version
    
    def init_schema(self) -> None:
        """初始化数据库 schema（子类必须实现）"""
        raise NotImplementedError
    
    def get_stored_version(self) -> Optional[str]:
        """获取存储的 schema 版本"""
        self.db_class.ensure_meta_table()
        return self.db_class.get_meta(self.VERSION_KEY)
    
    def set_version(self, version: str) -> None:
        """设置 schema 版本"""
        self.db_class.set_meta(self.VERSION_KEY, version)
    
    def is_initialized(self) -> bool:
        """检查数据库是否已初始化"""
        return self.get_stored_version() is not None
    
    def requires_migration(self) -> bool:
        """检查是否需要迁移"""
        stored = self.get_stored_version()
        if stored is None:
            return False
        return stored != self.current_version
    
    def get_version_delta(self) -> tuple[Optional[str], str]:
        """获取版本差异
        
        Returns:
            (存储的版本, 当前版本)
        """
        return (self.get_stored_version(), self.current_version)
    
    def initialize(self) -> None:
        """初始化数据库
        
        创建 meta 表、执行 init_schema、设置版本号。
        """
        # 确保 meta 表存在
        self.db_class.ensure_meta_table()
        
        # 执行 schema 初始化
        self.init_schema()
        
        # 设置版本号
        self.set_version(self.current_version)
