"""Logging utilities for the CLI."""

import logging
from rich.console import Console
from rich.logging import RichHandler

console = Console()


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with rich formatting.
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True, console=console)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    
    return logger


def log_success(message: str):
    """Log success message in green."""
    console.print(f"✓ {message}", style="bold green")


def log_error(message: str):
    """Log error message in red."""
    console.print(f"✗ {message}", style="bold red")


def log_info(message: str):
    """Log info message."""
    console.print(f"ℹ {message}", style="bold blue")


def log_warning(message: str):
    """Log warning message."""
    console.print(f"⚠ {message}", style="bold yellow")
