#!/usr/bin/env python3
"""
Python Tools CLI - A comprehensive command-line tool for managing 
Kubernetes clusters, infrastructure, and GitOps workflows.
"""

import typer
from commands.cluster import cluster_app
from commands.tools import tools_app
from commands.config import config_app

# Create main CLI application
app = typer.Typer(
    name="tools-cli",
    help="A comprehensive CLI tool for Kubernetes and infrastructure management",
    add_completion=True,
)

# Register command groups
app.add_typer(cluster_app, name="cluster")
app.add_typer(tools_app, name="tools")
app.add_typer(config_app, name="config")


@app.command()
def version():
    """Display CLI version."""
    typer.echo("Python Tools CLI v1.0.0")


if __name__ == "__main__":
    app()
