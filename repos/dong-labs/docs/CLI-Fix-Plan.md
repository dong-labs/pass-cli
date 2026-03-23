# CLI 统一修复计划

## 修复完成 ✅

### 已修复的 CLI

| CLI | 修改内容 | 状态 |
|-----|---------|------|
| **timeline-cli** | 添加 `no_args_is_help=True, add_completion=False` | ✅ |
| **pass-cli** | 重写为使用 `@json_output` 装饰器 | ✅ |
| **think-cli** | `name="dong-think"`, `ls`→`list`, 添加配置 | ✅ |
| **log-cli** | `name="dong-log"`, `ls`→`list`, 添加配置 | ✅ |
| **dida-cli** | `name="dong-dida"`, `ls`→`list`, 版本显示 | ✅ |
| **read-cli** | `name="dong-read"`, `ls`→`list`, 版本显示 | ✅ |
| **cang-cli** | `name="dong-cang"`, 版本显示 | ✅ |
| **expire-cli** | 已符合标准，无需修改 | ✅ |

## 统一标准

### Typer 配置
```python
app = typer.Typer(
    name="dong-xxx",           # 统一命名前缀
    help="描述",
    no_args_is_help=True,      # 无参数时显示帮助
    add_completion=False,      # 禁用 shell 自动补全
)
```

### 版本回调
```python
@app.callback()
def global_options(
    version: bool = typer.Option(False, "--version", "-v", is_eager=True),
):
    if version:
        console.print(f"dong-xxx {__version__}")
        raise typer.Exit()
```

### 命令装饰器
```python
@app.command()
@json_output          # 使用 dong-core 的 JSON 输出装饰器
def command_name():
    from .commands import module
    return module.function()
```

### 命令命名
- 使用 `list` 而非 `ls` (Typer 保留字问题已解决)
- 函数名使用动词/名词形式：`add`, `get`, `delete`, `search`, `stats`, `tags`
