"""
导入导出注册器

统一管理所有数据源的导入导出器。
"""

from typing import Optional
import json
from pathlib import Path

from .base import BaseExporter, BaseImporter


class ExporterRegistry:
    """导出器注册中心"""
    
    _exporters: dict[str, BaseExporter] = {}
    
    @classmethod
    def register(cls, exporter: BaseExporter) -> None:
        """
        注册导出器
        
        Args:
            exporter: 导出器实例
        """
        cls._exporters[exporter.name] = exporter
    
    @classmethod
    def get(cls, name: str) -> Optional[BaseExporter]:
        """
        获取导出器
        
        Args:
            name: 数据源名称
            
        Returns:
            导出器实例，不存在则返回 None
        """
        return cls._exporters.get(name)
    
    @classmethod
    def list_all(cls) -> list[str]:
        """列出所有已注册的数据源"""
        return list(cls._exporters.keys())
    
    @classmethod
    def export(
        cls, 
        sources: Optional[list[str]] = None,
        format: str = "json"
    ) -> dict[str, Any]:
        """
        导出指定数据源
        
        Args:
            sources: 要导出的数据源列表，None 表示全部
            format: 导出格式（json/csv/markdown）
            
        Returns:
            导出数据字典
        """
        sources = sources or cls.list_all()
        result = {}
        
        for name in sources:
            exporter = cls.get(name)
            if exporter:
                result[name] = exporter.fetch_all()
        
        return result
    
    @classmethod
    def export_to_file(
        cls,
        filename: str,
        sources: Optional[list[str]] = None,
        format: str = "json"
    ) -> int:
        """
        导出到文件
        
        Args:
            filename: 输出文件名
            sources: 要导出的数据源列表
            format: 导出格式
            
        Returns:
            导出的数据条数
        """
        data = cls.export(sources, format)
        total_count = sum(len(records) for records in data.values())
        
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            if format == "json":
                json.dump(data, f, ensure_ascii=False, indent=2)
            elif format == "csv":
                # CSV 只支持单数据源
                if len(data) == 1:
                    source_name = list(data.keys())[0]
                    exporter = cls.get(source_name)
                    if exporter:
                        f.write(exporter.to_csv())
            else:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        return total_count


class ImporterRegistry:
    """导入器注册中心"""
    
    _importers: dict[str, BaseImporter] = {}
    
    @classmethod
    def register(cls, importer: BaseImporter) -> None:
        """注册导入器"""
        cls._importers[importer.name] = importer
    
    @classmethod
    def get(cls, name: str) -> Optional[BaseImporter]:
        """获取导入器"""
        return cls._importers.get(name)
    
    @classmethod
    def list_all(cls) -> list[str]:
        """列出所有已注册的数据源"""
        return list(cls._importers.keys())
    
    @classmethod
    def import_from_file(
        cls,
        filename: str,
        merge: bool = False
    ) -> dict[str, dict[str, Any]]:
        """
        从文件导入数据
        
        Args:
            filename: 导入文件名
            merge: 是否合并模式
            
        Returns:
            各数据源的导入结果统计
        """
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        results = {}
        for name, records in data.items():
            importer = cls.get(name)
            if importer:
                # 验证数据
                is_valid, error_msg = importer.validate(records)
                if not is_valid:
                    results[name] = {
                        "success": False,
                        "error": error_msg,
                    }
                    continue
                
                # 导入数据
                result = importer.import_data(records, merge=merge)
                results[name] = {
                    "success": True,
                    **result
                }
        
        return results
