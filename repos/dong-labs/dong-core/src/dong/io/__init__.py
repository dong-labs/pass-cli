"""
dong.io - 导入导出模块

提供统一的数据导入导出基础设施。

使用方法：

1. 各 CLI 实现自己的导出器：

    from dong.io import BaseExporter, ExporterRegistry
    
    class LogExporter(BaseExporter):
        name = "log"
        
        def fetch_all(self) -> list[dict]:
            # 从数据库读取数据
            return [...]
    
    # 注册
    ExporterRegistry.register(LogExporter())

2. 在 CLI 中使用：

    from dong.io import ExporterRegistry
    
    @app.command()
    def export(output: str = "data.json"):
        ExporterRegistry.export_to_file(output)
"""

from .base import BaseExporter, BaseImporter
from .registry import ExporterRegistry, ImporterRegistry

__all__ = [
    "BaseExporter",
    "BaseImporter",
    "ExporterRegistry",
    "ImporterRegistry",
]
