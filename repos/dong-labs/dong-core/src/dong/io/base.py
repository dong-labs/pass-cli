"""
导入导出基类

提供统一的导入导出接口，各 CLI 实现具体逻辑。
"""

from abc import ABC, abstractmethod
from typing import Any
import json
import csv
from io import StringIO


class BaseExporter(ABC):
    """导出器基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """数据源名称（用于注册和识别）"""
        pass
    
    @abstractmethod
    def fetch_all(self) -> list[dict[str, Any]]:
        """
        获取所有数据
        
        Returns:
            数据列表，每条数据为字典
        """
        pass
    
    def to_json(self) -> str:
        """导出为 JSON 格式"""
        data = self.fetch_all()
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def to_csv(self) -> str:
        """导出为 CSV 格式"""
        data = self.fetch_all()
        if not data:
            return ""
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    
    def to_markdown(self) -> str:
        """导出为 Markdown 格式（子类可覆盖）"""
        data = self.fetch_all()
        lines = [f"# {self.name} 数据导出\n"]
        for item in data:
            lines.append(f"- {item}")
        return "\n".join(lines)


class BaseImporter(ABC):
    """导入器基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """数据源名称"""
        pass
    
    @abstractmethod
    def validate(self, data: list[dict[str, Any]]) -> tuple[bool, str]:
        """
        验证导入数据格式
        
        Args:
            data: 要导入的数据列表
            
        Returns:
            (是否有效, 错误信息)
        """
        pass
    
    @abstractmethod
    def import_data(
        self, 
        data: list[dict[str, Any]], 
        merge: bool = False
    ) -> dict[str, Any]:
        """
        导入数据
        
        Args:
            data: 数据列表
            merge: 是否合并（True=追加，False=替换）
            
        Returns:
            导入结果统计
        """
        pass
    
    def from_json(self, json_str: str) -> list[dict[str, Any]]:
        """从 JSON 字符串解析"""
        return json.loads(json_str)
    
    def from_csv(self, csv_str: str) -> list[dict[str, Any]]:
        """从 CSV 字符串解析"""
        reader = csv.DictReader(StringIO(csv_str))
        return list(reader)
