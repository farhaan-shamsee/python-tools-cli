"""Tool installation and management commands."""

import typer
from typing import List, Optional
from rich.table import Table
from core.tool_manager import ToolManager
from utils.logger import console, log_success, log_error

tools_app = typer.Typer(help="Development tool installation and management")


@tools_app.command()
def list():
    """List all supported tools."""
    manager = ToolManager()
    tools = manager.list_tools()
    
    table = Table(title="Supported Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Installed", style="magenta")
    
    for tool_name, tool_info in tools.items():
        installed = "✓" if manager.check_tool_installed(tool_name) else "✗"
        table.add_row(tool_name, tool_info["description"], installed)
    
    console.print(table)


@tools_app.command()
def install(
    tool_names: List[str] = typer.Argument(..., help="Tool name(s) to install"),
):
    """Install one or more tools."""
    manager = ToolManager()
    
    console.print(f"Installing tools: {', '.join(tool_names)}")
    
    results = manager.install_multiple_tools(tool_names)
    
    for tool_name, success in results.items():
        if success:
            log_success(f"{tool_name} installed successfully")
        else:
            log_error(f"Failed to install {tool_name}")


@tools_app.command()
def check(
    tool_name: str = typer.Argument(..., help="Tool name to check"),
):
    """Check if a tool is installed."""
    manager = ToolManager()
    
    if manager.check_tool_installed(tool_name):
        log_success(f"{tool_name} is installed")
    else:
        log_error(f"{tool_name} is not installed")
        raise typer.Exit(code=1)
