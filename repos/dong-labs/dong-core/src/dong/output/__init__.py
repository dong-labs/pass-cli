"""
输出格式化模块

提供统一的输出格式化功能，确保所有 CLI 命令输出一致的 JSON 格式。
"""

from dong.output.formatter import json_output, JsonOutputConfig

__all__ = ["json_output", "JsonOutputConfig"]
