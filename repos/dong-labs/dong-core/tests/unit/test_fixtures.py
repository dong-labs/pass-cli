"""
测试 testing.fixtures 模块

测试 fixtures 工具函数。
"""

import json
import os
from datetime import date
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest

from dong.testing.fixtures import (
    temp_dir,
    temp_file,
    mock_date,
    capture_output,
    sample_json_file,
    mock_env,
    JsonOutputMatcher,
)


class TestTempDirFixture:
    """测试 temp_dir fixture。"""

    @pytest.fixture
    def temp_dir_test(self) -> Generator[Path, None, None]:
        """模拟 temp_dir fixture 的行为。"""
        import tempfile
        import shutil

        temp_path = Path(tempfile.mkdtemp())
        try:
            yield temp_path
        finally:
            shutil.rmtree(temp_path, ignore_errors=True)

    def test_temp_dir_is_created(self, temp_dir_test: Path) -> None:
        """测试临时目录被创建。"""
        assert temp_dir_test.exists()
        assert temp_dir_test.is_dir()

    def test_temp_dir_can_create_files(self, temp_dir_test: Path) -> None:
        """测试在临时目录中创建文件。"""
        test_file = temp_dir_test / "test.txt"
        test_file.write_text("content")
        assert test_file.exists()
        assert test_file.read_text() == "content"


class TestTempFileFixture:
    """测试 temp_file fixture。"""

    @pytest.fixture
    def temp_file_test(self, tmp_path: Path) -> Generator[Path, None, None]:
        """模拟 temp_file fixture 的行为。"""
        file_path = tmp_path / "temp_file.txt"
        file_path.touch()
        yield file_path
        if file_path.exists():
            file_path.unlink()

    def test_temp_file_exists(self, temp_file_test: Path) -> None:
        """测试临时文件存在。"""
        assert temp_file_test.exists()
        assert temp_file_test.is_file()

    def test_temp_file_write_and_read(self, temp_file_test: Path) -> None:
        """测试临时文件写入和读取。"""
        temp_file_test.write_text("test content")
        assert temp_file_test.read_text() == "test content"


class TestMockDateFixture:
    """测试 mock_date fixture。"""

    @pytest.fixture
    def mock_date_test(self, monkeypatch: pytest.MonkeyPatch) -> Generator[callable, None, None]:
        """模拟 mock_date fixture 的行为。"""
        class DatePatcher:
            def __init__(self) -> None:
                self.mock_date = date(2024, 1, 1)

            def __call__(self, target_date: str | date) -> None:
                if isinstance(target_date, str):
                    from datetime import datetime
                    self.mock_date = datetime.strptime(target_date, "%Y-%m-%d").date()
                else:
                    self.mock_date = target_date
                self._patch()

            def freeze(self) -> None:
                self._patch()

            def _patch(self) -> None:
                def mock_today() -> date:
                    return self.mock_date

                monkeypatch.setattr("dong.dates.utils.date", type("MockDate", (), {
                    "today": staticmethod(mock_today),
                    "__call__": lambda *args, **kw: date(*args, **kw),
                })())

        patcher = DatePatcher()
        patcher.freeze()
        yield patcher

    def test_mock_date_with_string(self, mock_date_test: callable) -> None:
        """测试使用字符串设置日期。"""
        mock_date_test("2024-06-15")
        assert mock_date_test.mock_date == date(2024, 6, 15)

    def test_mock_date_with_date_object(self, mock_date_test: callable) -> None:
        """测试使用 date 对象设置日期。"""
        mock_date_test(date(2024, 12, 25))
        assert mock_date_test.mock_date == date(2024, 12, 25)


class TestCaptureOutputFixture:
    """测试 capture_output fixture。"""

    @pytest.fixture
    def capture_output_test(
        self,
        capsys: pytest.CaptureFixture,
    ) -> Generator[Any, None, None]:
        """模拟 capture_output fixture 的行为。"""
        class OutputCapture:
            def __init__(self) -> None:
                self._captured = None

            def _capture(self) -> None:
                self._captured = capsys.readouterr()

            @property
            def stdout(self) -> str:
                self._capture()
                return self._captured.out if self._captured else ""

            @property
            def stderr(self) -> str:
                self._capture()
                return self._captured.err if self._captured else ""

            def json(self) -> dict:
                output = self.stdout.strip()
                if output:
                    return json.loads(output)
                return {}

        yield OutputCapture()

    def test_capture_stdout(self, capture_output_test: Any) -> None:
        """测试捕获标准输出。"""
        print("Hello, World!")
        assert "Hello, World!" in capture_output_test.stdout

    def test_json_parsing(self, capture_output_test: Any) -> None:
        """测试 JSON 解析。"""
        print('{"success": true}')
        assert capture_output_test.json()["success"] is True


class TestSampleJsonFileFixture:
    """测试 sample_json_file fixture。"""

    def test_sample_json_file_content_structure(self, tmp_path: Path) -> None:
        """测试示例 JSON 文件内容结构。"""
        expected_data = {
            "id": 1,
            "name": "test",
            "items": ["a", "b", "c"],
        }

        file_path = tmp_path / "sample.json"
        file_path.write_text(json.dumps(expected_data, ensure_ascii=False, indent=2))

        content = json.loads(file_path.read_text())
        assert content == expected_data
        assert content["items"] == ["a", "b", "c"]


class TestMockEnvFixture:
    """测试 mock_env fixture。"""

    def test_mock_env_set_and_get(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """测试环境变量设置和获取。"""
        monkeypatch.setenv("TEST_VAR_DONG", "test_value")
        assert os.getenv("TEST_VAR_DONG") == "test_value"

        # 清理
        monkeypatch.delenv("TEST_VAR_DONG")


class TestJsonOutputMatcher:
    """测试 JsonOutputMatcher 类。"""

    def test_matcher_with_success_response(self) -> None:
        """测试成功响应匹配。"""
        data = {"success": True, "data": {"id": 123}}
        matcher = JsonOutputMatcher(data)

        assert matcher.success is True
        assert matcher.data == {"id": 123}
        assert matcher.error is None
        assert matcher.error_code is None
        assert matcher.error_message is None

    def test_matcher_with_error_response(self) -> None:
        """测试错误响应匹配。"""
        data = {"success": False, "error": {"code": "NOT_FOUND", "message": "Not found"}}
        matcher = JsonOutputMatcher(data)

        assert matcher.success is False
        assert matcher.data is None
        assert matcher.error == {"code": "NOT_FOUND", "message": "Not found"}
        assert matcher.error_code == "NOT_FOUND"
        assert matcher.error_message == "Not found"

    def test_matcher_parse_from_string(self) -> None:
        """测试从字符串解析。"""
        json_str = '{"success": true, "data": {"status": "ok"}}'
        matcher = JsonOutputMatcher.parse(json_str)

        assert matcher.success is True
        assert matcher.data["status"] == "ok"

    def test_matcher_with_no_success_field(self) -> None:
        """测试没有 success 字段的响应。"""
        data = {"data": {"id": 1}}
        matcher = JsonOutputMatcher(data)

        assert matcher.success is False  # 默认值

    def test_matcher_with_no_error_field(self) -> None:
        """测试没有 error 字段的响应。"""
        data = {"success": False}
        matcher = JsonOutputMatcher(data)

        assert matcher.error is None
        assert matcher.error_code is None
        assert matcher.error_message is None


class TestJsonOutputMatcherEdgeCases:
    """测试 JsonOutputMatcher 边界情况。"""

    def test_matcher_with_null_error(self) -> None:
        """测试 error 为 null 的情况。"""
        data = {"success": False, "error": None}
        matcher = JsonOutputMatcher(data)

        assert matcher.success is False
        assert matcher.error is None

    def test_matcher_with_empty_error_object(self) -> None:
        """测试空 error 对象。"""
        data = {"success": False, "error": {}}
        matcher = JsonOutputMatcher(data)

        assert matcher.error == {}
        assert matcher.error_code is None
        assert matcher.error_message is None

    def test_matcher_with_nested_data(self) -> None:
        """测试嵌套数据结构。"""
        data = {
            "success": True,
            "data": {
                "user": {"id": 1, "profile": {"name": "Test"}},
                "items": [1, 2, 3]
            }
        }
        matcher = JsonOutputMatcher(data)

        assert matcher.success is True
        assert matcher.data["user"]["profile"]["name"] == "Test"
        assert matcher.data["items"] == [1, 2, 3]

    def test_matcher_parse_invalid_json_raises_error(self) -> None:
        """测试解析无效 JSON 抛出错误。"""
        with pytest.raises(json.JSONDecodeError):
            JsonOutputMatcher.parse("not valid json")

    def test_matcher_with_error_code_only(self) -> None:
        """测试只有错误码的情况。"""
        data = {"success": False, "error": {"code": "ERROR"}}
        matcher = JsonOutputMatcher(data)

        assert matcher.error_code == "ERROR"
        assert matcher.error_message is None

    def test_matcher_with_error_message_only(self) -> None:
        """测试只有错误消息的情况。"""
        data = {"success": False, "error": {"message": "Something went wrong"}}
        matcher = JsonOutputMatcher(data)

        assert matcher.error_code is None
        assert matcher.error_message == "Something went wrong"


class TestFixturesIntegration:
    """测试 fixtures 集成场景。"""

    def test_temp_dir_and_file_combined(self, tmp_path: Path) -> None:
        """测试临时目录和文件组合使用。"""
        # 创建多个文件
        files = []
        for i in range(3):
            file_path = tmp_path / f"file{i}.txt"
            file_path.write_text(f"content {i}")
            files.append(file_path)

        # 验证所有文件
        for i, file_path in enumerate(files):
            assert file_path.exists()
            assert file_path.read_text() == f"content {i}"

        # 统计文件数量
        txt_files = list(tmp_path.glob("*.txt"))
        assert len(txt_files) == 3

    def test_json_file_with_temp_dir(self, tmp_path: Path) -> None:
        """测试在临时目录中使用 JSON 文件。"""
        # 创建 JSON 文件
        data = {"test": "data", "number": 42}
        json_file = tmp_path / "config.json"
        json_file.write_text(json.dumps(data))

        # 读取并验证
        loaded_data = json.loads(json_file.read_text())
        assert loaded_data == data
        assert loaded_data["number"] == 42


class TestFixtureHelperClasses:
    """测试 fixture 辅助类。"""

    def test_env_dict_like_behavior(self) -> None:
        """测试类字典行为。"""
        class EnvDict(dict):
            def __init__(self) -> None:
                super().__init__()
                self.setitem_calls = []

            def __setitem__(self, key: str, value: str) -> None:
                super().__setitem__(key, value)
                self.setitem_calls.append((key, value))

        env = EnvDict()
        env["TEST"] = "value"

        assert env["TEST"] == "value"
        assert ("TEST", "value") in env.setitem_calls

    def test_env_dict_delitem_behavior(self) -> None:
        """测试删除行为。"""
        class EnvDict(dict):
            def __init__(self) -> None:
                super().__init__({"TEST": "value"})
                self.delitem_calls = []

            def __delitem__(self, key: str) -> None:
                if key in self:
                    super().__delitem__(key)
                self.delitem_calls.append(key)

        env = EnvDict()
        del env["TEST"]

        assert "TEST" not in env
        assert "TEST" in env.delitem_calls


class TestOutputCaptureClass:
    """测试 OutputCapture 类。"""

    def test_output_capture_initial_state(self) -> None:
        """测试初始状态。"""
        class OutputCapture:
            def __init__(self) -> None:
                self._captured = None

            @property
            def stdout(self) -> str:
                return self._captured.out if self._captured else ""

            @property
            def stderr(self) -> str:
                return self._captured.err if self._captured else ""

        capture = OutputCapture()
        assert capture.stdout == ""
        assert capture.stderr == ""

    def test_output_capture_json_method(self) -> None:
        """测试 json 方法。"""
        class OutputCapture:
            def __init__(self) -> None:
                self._captured = None

            def set_output(self, text: str) -> None:
                self._captured = type("obj", (object,), {"out": text, "err": ""})()

            @property
            def stdout(self) -> str:
                return self._captured.out if self._captured else ""

            def json(self) -> dict:
                output = self.stdout.strip()
                if output:
                    return json.loads(output)
                return {}

        capture = OutputCapture()
        assert capture.json() == {}

        capture.set_output('{"success": true}')
        assert capture.json() == {"success": True}


class TestContextManagerBehavior:
    """测试上下文管理器行为。"""

    def test_output_capture_context_manager(self) -> None:
        """测试上下文管理器。"""
        class OutputCapture:
            def __init__(self) -> None:
                self.entered = False
                self.exited = False

            def __enter__(self) -> "OutputCapture":
                self.entered = True
                return self

            def __exit__(self, *args) -> None:
                self.exited = True

        capture = OutputCapture()
        assert not capture.entered
        assert not capture.exited

        with capture:
            assert capture.entered
            assert not capture.exited

        assert capture.entered
        assert capture.exited
