"""
pytest 配置文件

提供全局 fixtures 和测试配置。
"""

import sys
from pathlib import Path
from typing import Generator

import pytest

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_data_dir() -> Path:
    """提供测试数据目录路径。"""
    return Path(__file__).parent / "data"


@pytest.fixture
def temp_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """
    临时目录 fixture。

    在测试完成后自动清理。
    """
    yield tmp_path


@pytest.fixture
def sample_json_output() -> dict:
    """示例 JSON 输出数据。"""
    return {
        "status": "success",
        "data": {
            "id": 123,
            "name": "测试条目",
            "tags": ["测试", "示例"]
        },
        "meta": {
            "timestamp": "2026-03-15T12:00:00Z",
            "version": "1.0"
        }
    }


@pytest.fixture
def sample_dates() -> list[tuple[str, str]]:
    """示例日期输入输出对。"""
    return [
        ("2026-03-15", "2026年3月15日"),
        ("2026-03", "2026年3月"),
        ("2026", "2026年"),
        ("today", "今天"),
        ("yesterday", "昨天"),
        ("tomorrow", "明天"),
    ]


@pytest.fixture
def sample_error_messages() -> dict[str, str]:
    """示例错误消息。"""
    return {
        "file_not_found": "文件不存在: test.txt",
        "invalid_format": "无效的格式: json",
        "permission_denied": "权限不足",
        "validation_error": "验证失败: 缺少必需字段",
    }
