"""
测试 errors.exceptions 模块

测试自定义错误类型。
"""

import pytest

from dong.errors.exceptions import (
    DongError,
    ValidationError,
    NotFoundError,
    ConflictError,
    ErrorCode,
)


class TestErrorCode:
    """测试 ErrorCode 常量类。"""

    def test_validation_error_code(self) -> None:
        """测试 VALIDATION_ERROR 常量。"""
        assert ErrorCode.VALIDATION_ERROR == "VALIDATION_ERROR"

    def test_not_found_code(self) -> None:
        """测试 NOT_FOUND 常量。"""
        assert ErrorCode.NOT_FOUND == "NOT_FOUND"

    def test_conflict_code(self) -> None:
        """测试 CONFLICT 常量。"""
        assert ErrorCode.CONFLICT == "CONFLICT"

    def test_permission_denied_code(self) -> None:
        """测试 PERMISSION_DENIED 常量。"""
        assert ErrorCode.PERMISSION_DENIED == "PERMISSION_DENIED"

    def test_internal_error_code(self) -> None:
        """测试 INTERNAL_ERROR 常量。"""
        assert ErrorCode.INTERNAL_ERROR == "INTERNAL_ERROR"


class TestDongError:
    """测试基础 DongError 类。"""

    def test_base_error_creation(self) -> None:
        """测试基础错误创建。"""
        error = DongError("CUSTOM_ERROR", "发生了自定义错误")
        assert error.code == "CUSTOM_ERROR"
        assert error.message == "发生了自定义错误"
        assert error.details == {}

    def test_error_with_details(self) -> None:
        """测试带详情的错误。"""
        details = {"field": "email", "value": "test@example.com"}
        error = DongError("CUSTOM_ERROR", "验证失败", details=details)
        assert error.details == details

    def test_to_dict_without_details(self) -> None:
        """测试转换为字典（无详情）。"""
        error = DongError("CUSTOM_ERROR", "测试错误")
        result = error.to_dict()
        assert result == {"code": "CUSTOM_ERROR", "message": "测试错误"}

    def test_to_dict_with_details(self) -> None:
        """测试转换为字典（有详情）。"""
        details = {"user_id": 123}
        error = DongError("CUSTOM_ERROR", "测试错误", details=details)
        result = error.to_dict()
        assert result == {
            "code": "CUSTOM_ERROR",
            "message": "测试错误",
            "details": details,
        }

    def test_str_returns_message(self) -> None:
        """测试 __str__ 返回消息。"""
        error = DongError("CODE", "错误消息")
        assert str(error) == "错误消息"

    def test_exception_can_be_raised_and_caught(self) -> None:
        """测试异常可以被抛出和捕获。"""
        with pytest.raises(DongError) as exc_info:
            raise DongError("TEST", "测试异常")

        assert exc_info.value.code == "TEST"
        assert exc_info.value.message == "测试异常"


class TestValidationError:
    """测试验证错误类。"""

    def test_basic_validation_error(self) -> None:
        """测试基本验证错误。"""
        error = ValidationError("email", "邮箱格式不正确")
        assert error.code == ErrorCode.VALIDATION_ERROR
        assert error.message == "邮箱格式不正确"
        assert error.field == "email"

    def test_str_includes_field(self) -> None:
        """测试 __str__ 包含字段名。"""
        error = ValidationError("age", "必须为正整数")
        assert str(error) == "必须为正整数 (field: age)"

    def test_to_dict_includes_field(self) -> None:
        """测试转换为字典包含字段信息。"""
        error = ValidationError("password", "密码太短")
        result = error.to_dict()
        assert result["code"] == ErrorCode.VALIDATION_ERROR
        assert result["message"] == "密码太短"
        assert result["details"]["field"] == "password"

    def test_validation_error_with_custom_details(self) -> None:
        """测试带自定义详情的验证错误。"""
        error = ValidationError(
            "price",
            "价格无效",
            details={"min": 0, "max": 10000, "actual": -5}
        )
        assert error.details["min"] == 0
        assert error.details["max"] == 10000
        assert error.details["actual"] == -5
        assert error.details["field"] == "price"  # field 应该被保留


class TestNotFoundError:
    """测试资源未找到错误类。"""

    def test_with_resource_type_and_id(self) -> None:
        """测试带资源类型和 ID。"""
        error = NotFoundError("User", 123)
        assert error.code == ErrorCode.NOT_FOUND
        assert error.message == "User 123 不存在"
        assert error.resource_type == "User"
        assert error.resource_id == 123

    def test_with_resource_type_only(self) -> None:
        """测试仅资源类型。"""
        error = NotFoundError(resource_type="ConfigFile")
        assert error.message == "ConfigFile 不存在"
        assert error.resource_type == "ConfigFile"
        assert error.resource_id is None

    def test_with_custom_message(self) -> None:
        """测试自定义消息。"""
        error = NotFoundError(message="配置文件未找到")
        assert error.message == "配置文件未找到"

    def test_default_message(self) -> None:
        """测试默认消息。"""
        error = NotFoundError()
        assert error.message == "资源未找到"

    def test_to_dict_with_resource_info(self) -> None:
        """测试转换为字典包含资源信息。"""
        error = NotFoundError("Task", "task-abc-123")
        result = error.to_dict()
        assert result["code"] == ErrorCode.NOT_FOUND
        assert result["message"] == "Task task-abc-123 不存在"
        assert result["details"]["resource_type"] == "Task"
        assert result["details"]["resource_id"] == "task-abc-123"

    def test_to_dict_with_custom_details(self) -> None:
        """测试带自定义详情。"""
        error = NotFoundError(
            "Document",
            "doc-1",
            details={"search_path": "/docs", "searched_ids": ["doc-1", "doc-2"]}
        )
        result = error.to_dict()
        assert result["details"]["search_path"] == "/docs"
        assert result["details"]["searched_ids"] == ["doc-1", "doc-2"]

    def test_string_resource_id(self) -> None:
        """测试字符串资源 ID。"""
        error = NotFoundError("Article", "article-slug-123")
        assert error.message == "Article article-slug-123 不存在"


class TestConflictError:
    """测试冲突错误类。"""

    def test_basic_conflict_error(self) -> None:
        """测试基本冲突错误。"""
        error = ConflictError("User", "email", "test@example.com")
        assert error.code == ErrorCode.CONFLICT
        assert error.message == "email 'test@example.com' 已被使用"
        assert error.resource_type == "User"
        assert error.conflicting_field == "email"
        assert error.conflicting_value == "test@example.com"

    def test_custom_message(self) -> None:
        """测试自定义消息。"""
        error = ConflictError(
            "Product",
            "sku",
            "SKU-123",
            message="该 SKU 已存在"
        )
        assert error.message == "该 SKU 已存在"

    def test_to_dict_structure(self) -> None:
        """测试转换为字典结构。"""
        error = ConflictError("Booking", "time_slot", "2026-03-15-14:00")
        result = error.to_dict()
        assert result["code"] == ErrorCode.CONFLICT
        assert result["details"]["resource_type"] == "Booking"
        assert result["details"]["conflicting_field"] == "time_slot"
        assert result["details"]["conflicting_value"] == "2026-03-15-14:00"

    def test_with_custom_details(self) -> None:
        """测试带自定义详情。"""
        error = ConflictError(
            "Room",
            "name",
            "会议室A",
            details={"existing_id": 5, "created_at": "2026-01-01"}
        )
        assert error.details["existing_id"] == 5
        assert error.details["created_at"] == "2026-01-01"

    def test_numeric_conflicting_value(self) -> None:
        """测试数值类型的冲突值。"""
        error = ConflictError("Item", "id", 12345)
        assert error.conflicting_value == 12345
        assert error.details["conflicting_value"] == "12345"  # 转换为字符串


class TestErrorHierarchy:
    """测试错误继承关系。"""

    def test_validation_error_is_dong_error(self) -> None:
        """测试 ValidationError 是 DongError。"""
        error = ValidationError("field", "message")
        assert isinstance(error, DongError)

    def test_not_found_error_is_dong_error(self) -> None:
        """测试 NotFoundError 是 DongError。"""
        error = NotFoundError("Resource", 1)
        assert isinstance(error, DongError)

    def test_conflict_error_is_dong_error(self) -> None:
        """测试 ConflictError 是 DongError。"""
        error = ConflictError("Type", "field", "value")
        assert isinstance(error, DongError)

    def test_can_catch_specific_error_as_base(self) -> None:
        """测试可以基类捕获特定错误。"""
        with pytest.raises(DongError):
            raise ValidationError("f", "m")

        with pytest.raises(DongError):
            raise NotFoundError("R", 1)

        with pytest.raises(DongError):
            raise ConflictError("T", "f", "v")
