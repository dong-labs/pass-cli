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

# 导入命令
from . import init, add, get, ls, update, delete, stats

app.command()(init.init)
app.command()(add.add)
app.command()(get.get)
app.command(name="list")(ls.list_accounts)
app.command()(update.update)
app.command()(delete.delete)
app.command()(stats.stats)


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
