"""
错误处理模块

提供统一的错误类型和错误处理机制。
"""

from dong.errors.exceptions import (
    DongError,
    ValidationError,
    NotFoundError,
    ConflictError,
    ErrorCode,
)

__all__ = [
    "DongError",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "ErrorCode",
]
