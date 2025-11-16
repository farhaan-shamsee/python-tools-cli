"""Cluster management commands."""

import typer
from typing import Optional
from rich.table import Table
from core.cluster_manager import ClusterManager
from core.config_handler import ConfigHandler
from utils.logger import console, log_error
from utils.exceptions import ToolsCLIException

cluster_app = typer.Typer(help="Cluster lifecycle management commands")


def get_cluster_manager() -> ClusterManager:
    """Get configured cluster manager instance."""
    config_handler = ConfigHandler()
    config = config_handler.load()
    return ClusterManager(config)


@cluster_app.command()
def create(
    name: str = typer.Argument(..., help="Cluster name"),
    provider: str = typer.Option("local", help="Cloud provider (local, aws, alicloud)"),
    ports: Optional[str] = typer.Option(None, help="Ports to open (comma-separated)"),
    registry: bool = typer.Option(False, help="Create local registry"),
):
    """Create a new cluster."""
    try:
        manager = get_cluster_manager()
        
        kwargs = {}
        if ports:
            kwargs["ports_to_open"] = ports
        if registry:
            kwargs["use_registry"] = registry
        
        manager.create_cluster(name, provider, **kwargs)
        
    except ToolsCLIException as e:
        log_error(str(e))
        raise typer.Exit(code=1)


@cluster_app.command()
def delete(
    name: str = typer.Option(..., help="Cluster name"),
    provider: str = typer.Option("local", help="Cloud provider"),
):
    """Delete an existing cluster."""
    try:
        manager = get_cluster_manager()
        manager.delete_cluster(name, provider)
        
    except ToolsCLIException as e:
        log_error(str(e))
        raise typer.Exit(code=1)


@cluster_app.command()
def list(
    provider: str = typer.Option("local", help="Cloud provider"),
):
    """List all clusters."""
    try:
        manager = get_cluster_manager()
        clusters = manager.list_clusters(provider)
        
        if not clusters:
            console.print(f"No clusters found for provider: {provider}")
            return
        
        table = Table(title=f"Clusters ({provider})")
        table.add_column("Name", style="cyan")
        table.add_column("Provider", style="magenta")
        
        for cluster in clusters:
            table.add_row(cluster, provider)
        
        console.print(table)
        
    except ToolsCLIException as e:
        log_error(str(e))
        raise typer.Exit(code=1)


@cluster_app.command()
def info(
    name: str = typer.Argument(..., help="Cluster name"),
    provider: str = typer.Option("local", help="Cloud provider"),
):
    """Get cluster information."""
    try:
        manager = get_cluster_manager()
        cluster_info = manager.get_cluster_info(name, provider)
        
        if not cluster_info:
            log_error(f"Cluster '{name}' not found")
            raise typer.Exit(code=1)
        
        table = Table(title=f"Cluster Info: {name}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in cluster_info.items():
            table.add_row(key, str(value))
        
        console.print(table)
        
    except ToolsCLIException as e:
        log_error(str(e))
        raise typer.Exit(code=1)


@cluster_app.command()
def bootstrap(
    name: str = typer.Argument(..., help="Cluster name"),
    provider: str = typer.Option("local", help="Cloud provider"),
):
    """Bootstrap cluster with GitOps tools (Flux CD)."""
    try:
        manager = get_cluster_manager()
        manager.bootstrap_cluster(name, provider)
        
    except ToolsCLIException as e:
        log_error(str(e))
        raise typer.Exit(code=1)
