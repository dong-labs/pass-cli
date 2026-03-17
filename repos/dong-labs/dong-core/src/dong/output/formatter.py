"""
统一 JSON 输出装饰器

为 CLI 命令提供一致的 JSON 输出格式。

使用示例:
    ```python
    @json_output
    def my_command():
        return {"id": 1, "content": "..."}

    # 输出: {"success": true, "data": {"id": 1, "content": "..."}}
    ```

错误处理:
    ```python
    @json_output
    def failing_command():
        raise ValidationError("Invalid input")

    # 输出: {"success": false, "error": {"code": "VALIDATION_ERROR", "message": "Invalid input"}}
    ```
"""

import json
import sys
from dataclasses import dataclass, asdict
from functools import wraps
from typing import Any, Callable, TypeVar, ParamSpec

from dong.errors.exceptions import DongError

# Type variables for generic function wrapper
P = ParamSpec("P")
T = TypeVar("T")


@dataclass
class JsonOutputConfig:
    """JSON 输出配置"""

    indent: bool = False
    ensure_ascii: bool = False
    sort_keys: bool = False

    def to_dump_kwargs(self) -> dict[str, Any]:
        """转换为 json.dump 的关键字参数"""
        return {
            "indent": 2 if self.indent else None,
            "ensure_ascii": self.ensure_ascii,
            "sort_keys": self.sort_keys,
        }


class JsonResponse:
    """JSON 响应构建器"""

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: dict[str, str] | None = None,
    ) -> None:
        self.success = success
        self.data = data
        self.error = error

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        result: dict[str, Any] = {"success": self.success}
        if self.success:
            result["data"] = self.data
        elif self.error:
            result["error"] = self.error
        return result

    def serialize(
        self, config: JsonOutputConfig | None = None
    ) -> str:
        """序列化为 JSON 字符串"""
        cfg = config or JsonOutputConfig()
        return json.dumps(self.to_dict(), **cfg.to_dump_kwargs())


def _extract_error_info(exc: Exception) -> dict[str, str]:
    """从异常中提取错误信息"""
    if isinstance(exc, DongError):
        return {"code": exc.code, "message": str(exc.message)}
    # 内置异常类型映射
    error_map: dict[type[Exception], str] = {
        ValueError: "VALUE_ERROR",
        TypeError: "TYPE_ERROR",
        KeyError: "KEY_ERROR",
        AttributeError: "ATTRIBUTE_ERROR",
        PermissionError: "PERMISSION_ERROR",
        FileNotFoundError: "NOT_FOUND",
        IOError: "IO_ERROR",
    }
    code = error_map.get(type(exc), "UNKNOWN_ERROR")
    return {"code": code, "message": str(exc)}


def json_output(
    func: Callable[P, T] | None = None,
    *,
    config: JsonOutputConfig | None = None,
    file=None,
) -> Callable[P, T]:
    """
    统一 JSON 输出装饰器

    将函数返回值包装为标准 JSON 格式输出。

    Args:
        func: 被装饰的函数
        config: JSON 输出配置
        file: 输出文件对象，默认为 sys.stdout

    Returns:
        装饰后的函数

    Examples:
        基本用法:
            ```python
            @json_output
            def get_user(user_id: int):
                return {"id": user_id, "name": "Alice"}
            ```

        带配置:
            ```python
            @json_output(config=JsonOutputConfig(indent=True))
            def list_items():
                return [{"id": 1}, {"id": 2}]
            ```

        作为装饰器工厂:
            ```python
            @json_output()
            def my_func():
                return {"status": "ok"}
            ```
    """

    def decorator(f: Callable[P, T]) -> Callable[P, T]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            captured_exception: Exception | None = None
            result: T | None = None

            try:
                result = f(*args, **kwargs)
                response = JsonResponse(success=True, data=result)
            except Exception as e:
                captured_exception = e
                error_info = _extract_error_info(e)
                response = JsonResponse(success=False, error=error_info)

            output_file = file or sys.stdout
            print(response.serialize(config), file=output_file)

            # CLI 使用模式：打印后不抛出异常，让调用者继续
            return result  # type: ignore

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


def print_json(
    data: Any,
    *,
    config: JsonOutputConfig | None = None,
    file=None,
) -> None:
    """
    直接打印 JSON 格式数据

    Args:
        data: 要输出的数据
        config: JSON 输出配置
        file: 输出文件对象

    Examples:
        ```python
        print_json({"id": 1, "name": "Alice"})
        # 输出: {"success": true, "data": {"id": 1, "name": "Alice"}}

        print_json({"error": "Not found"}, success=False)
        # 输出: {"success": false, "error": {"error": "Not found"}}
        ```
    """
    response = JsonResponse(success=True, data=data)
    output_file = file or sys.stdout
    print(response.serialize(config), file=output_file)


def print_json_error(
    code: str,
    message: str,
    *,
    config: JsonOutputConfig | None = None,
    file=None,
) -> None:
    """
    直接打印 JSON 错误格式

    Args:
        code: 错误代码
        message: 错误消息
        config: JSON 输出配置
        file: 输出文件对象

    Examples:
        ```python
        print_json_error("NOT_FOUND", "User not found")
        # 输出: {"success": false, "error": {"code": "NOT_FOUND", "message": "User not found"}}
        ```
    """
    response = JsonResponse(success=False, error={"code": code, "message": message})
    output_file = file or sys.stdout
    print(response.serialize(config), file=output_file)
