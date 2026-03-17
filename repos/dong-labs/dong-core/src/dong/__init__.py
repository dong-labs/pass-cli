"""
dong-core: 咚咚家族核心库

这是一个"瘦 core" 库，仅提供通用组件和基础设施。
不包含数据模型、业务逻辑或数据库 schema。

主要模块：
- output: 统一输出格式化
- errors: 统一错误类型
- dates: 日期处理工具
- testing: 测试工具
"""

__version__ = "0.2.0"

# 导出核心组件
from dong.output.formatter import json_output
from dong.errors.exceptions import (
    DongError,
    ValidationError,
    NotFoundError,
    ConflictError,
)
from dong.dates.utils import DateUtils

__all__ = [
    "__version__",
    "json_output",
    "DongError",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "DateUtils",
]
