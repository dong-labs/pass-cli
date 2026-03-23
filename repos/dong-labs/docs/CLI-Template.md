# 咚咚家族 CLI 统一模板

> 所有 dong-xxx CLI 应该遵循此模板设计

---

## CLI 配置模板

```python
"""{名称} CLI 主入口"""

import typer
from rich.console import Console
from dong import json_output, ValidationError, NotFoundError
from . import __version__

app = typer.Typer(
    name="dong-{name}",               # 统一使用 dong-xxx 命名
    help="{描述}",
    no_args_is_help=True,            # 无参数时显示帮助
    add_completion=False,             # 禁用自动补全
)

console = Console()


# ============================================================================
# 全局选项（统一）
# ============================================================================

@app.callback()
def global_options(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="显示版本号",
        is_eager=True,
    ),
    json_mode: bool = typer.Option(
        False,
        "--json",
        help="强制 JSON 输出（用于调试）",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="调试模式（显示详细错误信息）",
    ),
) -> None:
    """全局选项处理"""
    if version:
        console.print(f"dong-{name} {__version__}")
        raise typer.Exit()


# ============================================================================
# 基础命令（必须）
# ============================================================================

@app.command()
@json_output
def init():
    """初始化数据库"""
    from .commands.init import cmd_init
    return cmd_init()


@app.command()
@json_output
def add(
    content: str = typer.Argument(..., help="内容"),
    tags: str = typer.Option(None, "--tags", "-t", help="标签（逗号分隔）"),
):
    """添加记录"""
    from .commands.add import cmd_add
    return cmd_add(content=content, tags=tags)


@app.command(name="list")  # 统一使用 list，不是 ls
@json_output
def list_items(
    limit: int = typer.Option(20, "--limit", "-l", help="返回数量"),
    offset: int = typer.Option(0, "--offset", "-o", help="偏移量"),
):
    """列出所有记录"""
    from .commands.list import cmd_list
    return cmd_list(limit=limit, offset=offset)


@app.command()
@json_output
def get(
    item_id: int = typer.Argument(..., help="记录 ID"),
):
    """获取单条记录详情"""
    from .commands.get import cmd_get
    return cmd_get(item_id=item_id)


@app.command()
@json_output
def update(
    item_id: int = typer.Argument(..., help="记录 ID"),
    content: str = typer.Option(None, "--content", "-c", help="更新内容"),
    tags: str = typer.Option(None, "--tags", "-t", help="标签（逗号分隔）"),
):
    """更新记录"""
    from .commands.update import cmd_update
    return cmd_update(item_id=item_id, content=content, tags=tags)


@app.command()
@json_output
def delete(
    item_id: int = typer.Argument(..., help="记录 ID"),
    force: bool = typer.Option(False, "--force", "-f", help="强制删除，不确认"),
):
    """删除记录"""
    from .commands.delete import cmd_delete
    return cmd_delete(item_id=item_id, force=force)


# ============================================================================
# 扩展命令（推荐）
# ============================================================================

@app.command()
@json_output
def search(
    query: str = typer.Argument(..., help="搜索关键词"),
    limit: int = typer.Option(20, "--limit", "-l", help="返回数量"),
):
    """搜索记录"""
    from .commands.search import cmd_search
    return cmd_search(query=query, limit=limit)


@app.command()
@json_output
def stats():
    """统计概览"""
    from .commands.stats import cmd_stats
    return cmd_stats()


@app.command()
@json_output
def tags():
    """列出所有标签及数量"""
    from .commands.tags import cmd_tags
    return cmd_tags()


# ============================================================================
# 主入口
# ============================================================================

if __name__ == "__main__":
    app()
```

---

## 设计规范

### 1. Typer 配置（必须）

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `name` | `dong-xxx` | 统一前缀 |
| `help` | 简短描述 | 帮助文本 |
| `no_args_is_help` | `True` | 无参数显示帮助 |
| `add_completion` | `False` | 禁用自动补全 |

### 2. 全局选项（必须）

| 选项 | 短选项 | 说明 |
|------|--------|------|
| `--version` | `-v` | 显示版本号 |
| `--json` | - | 强制 JSON 输出（调试用） |
| `--debug` | - | 调试模式 |

### 3. 基础命令（必须）

| 命令 | 说明 | 函数名 |
|------|------|--------|
| `init` | 初始化数据库 | `cmd_init` |
| `add` | 添加记录 | `cmd_add` |
| `list` | 列出记录 | `cmd_list` |
| `get` | 获取详情 | `cmd_get` |
| `update` | 更新记录 | `cmd_update` |
| `delete` | 删除记录 | `cmd_delete` |

> **注意**：统一使用 `list` 而不是 `ls`

### 4. 扩展命令（推荐）

| 命令 | 说明 | 函数名 |
|------|------|--------|
| `search` | 搜索记录 | `cmd_search` |
| `stats` | 统计概览 | `cmd_stats` |
| `tags` | 标签管理 | `cmd_tags` |

### 5. 输出规范（必须）

- 使用 `dong-core` 的 `@json_output` 装饰器
- 统一 JSON 格式：
  ```json
  {"success": true/false, "data": {...} 或 "error": {...}}
  ```

### 6. 错误处理（必须）

- 使用 `dong-core` 的异常类：
  - `ValidationError`
  - `NotFoundError`
  - `ConflictError`

### 7. 选项命名规范

| 选项 | 短选项 | 说明 |
|------|--------|------|
| `--limit` | `-l` | 限制数量 |
| `--offset` | `-o` | 偏移量 |
| `--tags` | `-t` | 标签 |
| `--content` | `-c` | 内容 |
| `--force` | `-f` | 强制执行 |

---

## 修复清单

### 需要修复的 CLI

| CLI | ls→list | +--version | +no_args | +add_completion | +@json_output |
|-----|---------|-----------|----------|-----------------|----------------|
| read-cli | ✅ | ✅ | ✅ | ❌ | ✅ |
| think-cli | ❌ | ❌ | ❌ | ❌ | ❌ |
| dida-cli | ❌ | ✅ | ✅ | ✅ | ✅ |
| log-cli | ❌ | ❌ | ❌ | ❌ | ❌ |
| cang-cli | - | ✅ | ✅ | ✅ | ❌ |
| expire-cli | ❌ | ✅ | ✅ | ✅ | ✅ |
| pass-cli | ❌ | ✅ | ✅ | ✅ | ❌ |
| timeline-cli | ❌ | ✅ | ❌ | ❌ | ❌ |

---

## 使用模板

```bash
# 复制模板到新 CLI
cp docs/CLI-Template.md xxx-cli/cli-template.md

# 或者直接复制代码块到 cli.py
```
