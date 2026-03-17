"""
统一错误类型定义

定义 dong 家族 CLI 工具的通用异常类型。
所有自定义异常都继承自 DongError 基类。

使用示例:
    ```python
    from dong.errors import ValidationError, NotFoundError

    def get_user(user_id: int):
        if user_id <= 0:
            raise ValidationError("user_id", "必须为正整数")
        if not find_user(user_id):
            raise NotFoundError(f"用户 {user_id} 不存在")
    ```
"""

from typing import Any


class ErrorCode:
    """错误代码常量"""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class DongError(Exception):
    """
    dong 家族 CLI 基础异常类

    所有自定义异常的基类，提供统一的错误格式。

    Attributes:
        code: 错误代码，用于程序化识别错误类型
        message: 人类可读的错误消息
        details: 额外的错误详情，可选

    Examples:
        ```python
        raise DongError("CUSTOM_ERROR", "发生了自定义错误")
        ```
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """转换为字典格式"""
        result = {"code": self.code, "message": self.message}
        if self.details:
            result["details"] = self.details
        return result

    def __str__(self) -> str:
        """返回错误消息"""
        return self.message


class ValidationError(DongError):
    """
    验证错误

    当输入数据验证失败时抛出。

    Attributes:
        field: 验证失败的字段名
        message: 验证失败的原因

    Examples:
        ```python
        raise ValidationError("email", "邮箱格式不正确")
        # 输出: ValidationError: 邮箱格式不正确 (field: email)
        ```
    """

    def __init__(
        self,
        field: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.field = field
        full_details = {"field": field}
        if details:
            full_details.update(details)
        super().__init__(ErrorCode.VALIDATION_ERROR, message, details=full_details)

    def __str__(self) -> str:
        return f"{self.message} (field: {self.field})"


class NotFoundError(DongError):
    """
    资源未找到错误

    当请求的资源不存在时抛出。

    Attributes:
        resource_type: 资源类型（如 "User", "Task"）
        resource_id: 资源标识符

    Examples:
        ```python
        raise NotFoundError("User", 123)
        # 输出: NotFoundError: User 123 不存在

        raise NotFoundError(message="配置文件未找到")
        # 输出: NotFoundError: 配置文件未找到
        ```
    """

    def __init__(
        self,
        resource_type: str | None = None,
        resource_id: Any = None,
        *,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.resource_type = resource_type
        self.resource_id = resource_id

        if message is None:
            if resource_type is not None and resource_id is not None:
                message = f"{resource_type} {resource_id} 不存在"
            elif resource_type is not None:
                message = f"{resource_type} 不存在"
            else:
                message = "资源未找到"

        full_details: dict[str, Any] = {}
        if resource_type is not None:
            full_details["resource_type"] = resource_type
        if resource_id is not None:
            full_details["resource_id"] = str(resource_id)
        if details:
            full_details.update(details)

        super().__init__(ErrorCode.NOT_FOUND, message, details=full_details)


class ConflictError(DongError):
    """
    冲突错误

    当操作与现有状态冲突时抛出，如重复创建已存在的资源。

    Attributes:
        resource_type: 冲突的资源类型
        conflicting_field: 冲突的字段名
        conflicting_value: 冲突的字段值

    Examples:
        ```python
        raise ConflictError("User", "email", "test@example.com")
        # 输出: ConflictError: email 'test@example.com' 已被使用
        ```
    """

    def __init__(
        self,
        resource_type: str,
        conflicting_field: str,
        conflicting_value: Any,
        *,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.resource_type = resource_type
        self.conflicting_field = conflicting_field
        self.conflicting_value = conflicting_value

        if message is None:
            message = (
                f"{conflicting_field} '{conflicting_value}' 已被使用"
            )

        full_details = {
            "resource_type": resource_type,
            "conflicting_field": conflicting_field,
            "conflicting_value": str(conflicting_value),
        }
        if details:
            full_details.update(details)

        super().__init__(ErrorCode.CONFLICT, message, details=full_details)
