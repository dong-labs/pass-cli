"""密码咚 CLI 主入口"""

import typer
from rich.console import Console
from . import __version__

console = Console()

app = typer.Typer(
    name="dong-pass",
    help="密码咚 - 账号密码管理 CLI",
    no_args_is_help=True,
    add_completion=False,
)

# 导入命令模块
from .commands import init, add, get, ls, update, delete, stats

app.command(name="init")(init.init)
app.command(name="add")(add.add)
app.command(name="get")(get.get)
app.command(name="list")(ls.list_accounts)
app.command(name="update")(update.update)
app.command(name="delete")(delete.delete)
app.command(name="stats")(stats.stats)


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="显示版本"),
):
    """密码咚 - 账号密码管理 CLI"""
    if version:
        console.print(f"dong-pass {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()

@app.command()
def export(output: str = typer.Option("pass.json", "-o", "--output"), format: str = typer.Option("json", "-f", "--format")):
    """导出数据"""
    from .commands.export import export as do_export
    do_export(output, format)

@app.command(name="import")
def import_data(file: str = typer.Option(..., "-f", "--file"), merge: bool = typer.Option(False, "--merge"), dry_run: bool = typer.Option(False, "--dry-run")):
    """导入数据"""
    from .commands.data_import import import_data as do_import
    do_import(file, merge, dry_run)
