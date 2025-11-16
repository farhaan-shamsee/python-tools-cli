"""Custom exceptions for the CLI tool."""


class ToolsCLIException(Exception):
    """Base exception for all CLI errors."""
    pass


class ConfigurationError(ToolsCLIException):
    """Raised when configuration is invalid or missing."""
    pass


class ClusterOperationError(ToolsCLIException):
    """Raised when cluster operations fail."""
    pass


class ToolInstallationError(ToolsCLIException):
    """Raised when tool installation fails."""
    pass


class ProviderNotSupportedError(ToolsCLIException):
    """Raised when a cloud provider is not supported."""
    pass
