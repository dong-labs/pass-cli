"""
测试 Fixtures 和辅助工具

提供常用的测试 fixtures 和辅助函数。

Examples:
    ```python
    import pytest
    from dong.testing import temp_dir, mock_date, capture_output

    def test_with_temp_dir(temp_dir):
        # temp_dir 是一个临时目录路径
        # 测试结束后自动清理
        pass

    def test_with_mock_date(mock_date):
        # mock_date 默认冻结在 2024-01-01
        from datetime import date
        assert date.today() == date(2024, 1, 1)

    def test_with_custom_date():
        with mock_date("2024-06-15"):
            assert date.today() == date(2024, 6, 15)

    def test_capture_output(capture_output):
        # 捕获 stdout
        print("Hello")
        assert "Hello" in capture_output.stdout
    ```
"""

import contextlib
import json
import os
import shutil
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import Any, Generator
from unittest.mock import patch

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    创建临时目录 fixture

    生成一个临时目录路径，测试结束后自动清理。

    Yields:
        临时目录的 Path 对象

    Examples:
        ```python
        def test_write_file(temp_dir):
            file_path = temp_dir / "test.txt"
            file_path.write_text("content")
            assert file_path.exists()
            # 测试结束后 temp_dir 自动删除
        ```
    """
    temp_path = Path(tempfile.mkdtemp())
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_file(temp_dir: Path) -> Generator[Path, None, None]:
    """
    创建临时文件 fixture

    在临时目录中创建一个空文件，返回文件路径。

    Yields:
        临时文件的 Path 对象

    Examples:
        ```python
        def test_temp_file(temp_file):
            temp_file.write_text("test content")
            assert temp_file.read_text() == "test content"
        ```
    """
    file_path = temp_dir / "temp_file.txt"
    file_path.touch()
    yield file_path
    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def mock_date(monkeypatch: pytest.MonkeyPatch) -> Generator[callable, None, None]:
    """
    模拟日期 fixture

    可以冻结时间或指定特定日期。

    Args:
        monkeypatch: pytest 的 monkeypatch fixture

    Yields:
        一个函数，用于设置模拟日期

    Examples:
        ```python
        def test_today_is_2024(mock_date):
            mock_date("2024-01-01")
            assert date.today() == date(2024, 1, 1)

        def test_freeze_time(mock_date):
            mock_date.freeze()
            # date.today() 返回固定日期
        ```
    """

    class DatePatcher:
        def __init__(self) -> None:
            self.mock_date = date(2024, 1, 1)
            self.original_date = date

        def __call__(self, target_date: str | date) -> None:
            """设置模拟日期"""
            if isinstance(target_date, str):
                self.mock_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            else:
                self.mock_date = target_date
            self._patch()

        def freeze(self) -> None:
            """冻结在默认日期"""
            self._patch()

        def _patch(self) -> None:
            def mock_today() -> date:
                return self.mock_date

            def mock_fromtimestamp(ts: float) -> date:
                return self.mock_date

            monkeypatch.setattr(date, "today", mock_today)
            monkeypatch.setattr(date, "fromtimestamp", mock_fromtimestamp)

    patcher = DatePatcher()
    patcher.freeze()
    yield patcher


@pytest.fixture
def capture_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> Generator[Any, None, None]:
    """
    捕获输出 fixture

    提供 context manager 和属性访问两种方式捕获输出。

    Yields:
        带有 stdout/stderr 属性的对象

    Examples:
        ```python
        def test_print(capture_output):
            print("Hello")
            assert "Hello" in capture_output.stdout

        def test_context_manager():
            with capture_output as captured:
                print("Hidden")
            assert "Hidden" in captured.stdout
        ```
    """
    class OutputCapture:
        def __init__(self) -> None:
            self._captured = None

        def _capture(self) -> None:
            self._captured = capsys.readouterr()

        @property
        def stdout(self) -> str:
            """获取捕获的标准输出"""
            self._capture()
            return self._captured.out if self._captured else ""

        @property
        def stderr(self) -> str:
            """获取捕获的标准错误"""
            self._capture()
            return self._captured.err if self._captured else ""

        def json(self) -> dict[str, Any]:
            """尝试将输出解析为 JSON"""
            self._capture()
            output = self.stdout.strip()
            if output:
                return json.loads(output)
            return {}

        def __enter__(self) -> "OutputCapture":
            return self

        def __exit__(self, *args: Any) -> None:
            self._capture()

    yield OutputCapture()


@pytest.fixture
def sample_json_file(temp_dir: Path) -> Generator[Path, None, None]:
    """
    创建示例 JSON 文件 fixture

    在临时目录中创建一个包含示例数据的 JSON 文件。

    Yields:
        JSON 文件的 Path 对象

    Examples:
        ```python
        def test_read_json(sample_json_file):
            import json
            data = json.loads(sample_json_file.read_text())
            assert data["name"] == "test"
        ```
    """
    data = {
        "id": 1,
        "name": "test",
        "items": ["a", "b", "c"],
    }
    file_path = temp_dir / "sample.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    yield file_path


@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch) -> Generator[dict[str, str], None, None]:
    """
    模拟环境变量 fixture

    提供一个临时环境变量字典，测试结束后恢复原始环境。

    Yields:
        可修改的环境变量字典

    Examples:
        ```python
        def test_with_env(mock_env):
            mock_env["TEST_VAR"] = "test_value"
            assert os.getenv("TEST_VAR") == "test_value"
            # 测试结束后环境变量自动恢复
        ```
    """
    original_env = os.environ.copy()

    class EnvDict(dict):
        def __setitem__(self, key: str, value: str) -> None:
            super().__setitem__(key, value)
            monkeypatch.setenv(key, value)

        def __delitem__(self, key: str) -> None:
            if key in self:
                super().__delitem__(key)
            monkeypatch.delenv(key, raising=False)

    env_dict = EnvDict(original_env)
    yield env_dict

    # 恢复原始环境
    for key in set(os.environ) - set(original_env):
        monkeypatch.delenv(key, raising=False)
    for key, value in original_env.items():
        if os.environ.get(key) != value:
            monkeypatch.setenv(key, value)


class JsonOutputMatcher:
    """
    JSON 输出匹配器

    用于测试 JSON 输出格式的辅助类。

    Examples:
        ```python
        def test_json_output(capture_output):
            print('{"success": true, "data": {"id": 1}}')

            matcher = JsonOutputMatcher.parse(capture_output.stdout)
            assert matcher.success
            assert matcher.data["id"] == 1
        ```
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def success(self) -> bool:
        """是否成功"""
        return self._data.get("success", False)

    @property
    def data(self) -> Any:
        """响应数据"""
        return self._data.get("data")

    @property
    def error(self) -> dict[str, str] | None:
        """错误信息"""
        return self._data.get("error")

    @property
    def error_code(self) -> str | None:
        """错误代码"""
        error = self.error
        return error.get("code") if error else None

    @property
    def error_message(self) -> str | None:
        """错误消息"""
        error = self.error
        return error.get("message") if error else None

    @classmethod
    def parse(cls, json_str: str) -> "JsonOutputMatcher":
        """从 JSON 字符串解析"""
        return cls(json.loads(json_str))


@pytest.fixture
def json_matcher() -> type[JsonOutputMatcher]:
    """
    JSON 匹配器 fixture

    返回 JsonOutputMatcher 类供测试使用。

    Examples:
        ```python
        def test_json_output(json_matcher):
            result = json_matcher.parse('{"success": true, "data": {"id": 1}}')
            assert result.success
            assert result.data["id"] == 1
        ```
    """
    return JsonOutputMatcher
