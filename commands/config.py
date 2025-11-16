"""Configuration management commands."""

import typer
from pathlib import Path
from core.config_handler import ConfigHandler
from utils.logger import log_success, log_error, log_info, console
from utils.exceptions import ConfigurationError

config_app = typer.Typer(help="Configuration file management")


@config_app.command()
def init(
    output: str = typer.Option("config.yaml", help="Output file path"),
    force: bool = typer.Option(False, help="Overwrite existing config"),
):
    """Initialize a new configuration file."""
    try:
        path = Path(output)
        
        if path.exists() and not force:
            log_error(f"Configuration file already exists: {output}")
            log_info("Use --force to overwrite")
            raise typer.Exit(code=1)
        
        ConfigHandler.create_default_config(output)
        log_success(f"Configuration file created: {output}")
        
    except ConfigurationError as e:
        log_error(str(e))
        raise typer.Exit(code=1)


@config_app.command()
def show(
    config_path: str = typer.Option("config.yaml", help="Config file path"),
):
    """Display current configuration."""
    try:
        handler = ConfigHandler(config_path)
        config = handler.load()
        
        import yaml
        console.print(yaml.dump(config, default_flow_style=False))
        
    except ConfigurationError as e:
        log_error(str(e))
        raise typer.Exit(code=1)


@config_app.command()
def validate(
    config_path: str = typer.Option("config.yaml", help="Config file path"),
):
    """Validate configuration file."""
    try:
        handler = ConfigHandler(config_path)
        handler.load()
        log_success("Configuration is valid")
        
    except ConfigurationError as e:
        log_error(f"Configuration is invalid: {e}")
        raise typer.Exit(code=1)
