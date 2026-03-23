"""密码咚 CLI 主入口"""

import typer
from rich.console import Console
from dong import json_output
from . import __version__

console = Console()

app = typer.Typer(
    name="dong-pass",
    help="密码咚 - 账号密码管理 CLI",
    no_args_is_help=True,
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """版本号回调函数"""
    if value:
        console.print(f"dong-pass {__version__}")
        raise typer.Exit()


@app.callback()
def global_options(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="显示版本号",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """全局选项"""
    pass


@app.command()
@json_output
def init():
    """初始化数据库"""
    from .commands import init
    return init.init()


@app.command()
@json_output
def add(
    site: str = typer.Argument(..., help="网站/服务名"),
    account: str = typer.Option(None, "--account", "-a", help="账号/邮箱"),
    password: str = typer.Option(None, "--password", "-p", help="密码"),
    category: str = typer.Option(None, "--category", "-c", help="分类"),
):
    """添加账号"""
    from .commands import add
    return add.add(site=site, account=account, password=password, category=category)


@app.command()
@json_output
def get(
    site: str = typer.Argument(..., help="网站/服务名"),
):
    """获取账号信息"""
    from .commands import get
    return get.get(site=site)


@app.command()
@json_output
def list(
    category: str = typer.Option(None, "--category", "-c", help="按分类筛选"),
):
    """列出所有账号"""
    from .commands import ls
    return ls.ls(category=category)


@app.command()
@json_output
def update(
    site: str = typer.Argument(..., help="网站/服务名"),
    account: str = typer.Option(None, "--account", "-a", help="新账号"),
    password: str = typer.Option(None, "--password", "-p", help="新密码"),
):
    """更新账号"""
    from .commands import update
    return update.update(site=site, account=account, password=password)


@app.command()
@json_output
def delete(
    site: str = typer.Argument(..., help="网站/服务名"),
):
    """删除账号"""
    from .commands import delete
    return delete.delete(site=site)


@app.command()
@json_output
def stats():
    """统计信息"""
    from .commands import stats
    return stats.stats()


@app.command()
def export(
    output: str = typer.Option("pass.json", "-o", "--output", help="输出文件"),
    format: str = typer.Option("json", "-f", "--format", help="格式: json"),
):
    """导出数据"""
    from .commands.export import export as do_export
    do_export(output, format)


@app.command(name="import")
def import_data(
    file: str = typer.Option(..., "-f", "--file", help="导入文件"),
    merge: bool = typer.Option(False, "--merge", help="合并模式"),
    dry_run: bool = typer.Option(False, "--dry-run", help="预览模式"),
):
    """导入数据"""
    from .commands.data_import import import_data as do_import
    do_import(file, merge, dry_run)


if __name__ == "__main__":
    app()
