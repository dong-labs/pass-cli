import typer
from rich.console import Console
from dong.io import ExporterRegistry
from expire.exporter import ExpireExporter
console = Console()
def export(output: str = typer.Option("expire.json", "-o", "--output"), format: str = typer.Option("json", "-f", "--format")):
    if not ExporterRegistry.get("expire"): ExporterRegistry.register(ExpireExporter())
    exporter = ExporterRegistry.get("expire")
    data = exporter.to_json()
    with open(output, "w", encoding="utf-8") as f: f.write(data)
    console.print(f"✅ 已导出 {len(exporter.fetch_all())} 条数据到 {output}", style="green")
