"""Cluster management orchestration."""

from typing import Dict, Any, Optional
from providers.base_provider import BaseProvider
from providers.local_provider import LocalProvider
from providers.aws_provider import AWSProvider
from providers.azure_provider import AzureProvider
from utils.exceptions import ProviderNotSupportedError, ClusterOperationError
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ClusterManager:
    """
    Manages cluster lifecycle operations across different providers.
    
    This class follows the Strategy Pattern and Dependency Inversion Principle.
    """
    
    PROVIDER_MAP = {
        "local": LocalProvider,
        "k3d": LocalProvider,
        "aws": AWSProvider,
        "eks": AWSProvider,
        "azure": AzureProvider,
        "aks": AzureProvider,
    }
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize cluster manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self._providers: Dict[str, BaseProvider] = {}
    
    def _get_provider(self, provider_type: str) -> BaseProvider:
        """
        Get or create a provider instance.
        
        Args:
            provider_type: Type of provider (local, aws, azure)
            
        Returns:
            Provider instance
            
        Raises:
            ProviderNotSupportedError: If provider type is not supported
        """
        provider_type = provider_type.lower()
        
        if provider_type not in self.PROVIDER_MAP:
            raise ProviderNotSupportedError(
                f"Provider '{provider_type}' is not supported. "
                f"Available providers: {', '.join(self.PROVIDER_MAP.keys())}"
            )
        
        # Lazy initialization of providers
        if provider_type not in self._providers:
            provider_class = self.PROVIDER_MAP[provider_type]
            self._providers[provider_type] = provider_class(self.config)
        
        return self._providers[provider_type]
    
    def create_cluster(
        self,
        name: str,
        provider_type: str = "local",
        **kwargs
    ) -> bool:
        """
        Create a cluster.
        
        Args:
            name: Cluster name
            provider_type: Cloud provider type
            **kwargs: Additional provider-specific parameters
            
        Returns:
            True if successful
        """
        provider = self._get_provider(provider_type)
        return provider.create_cluster(name, **kwargs)
    
    def delete_cluster(self, name: str, provider_type: str = "local") -> bool:
        """Delete a cluster."""
        provider = self._get_provider(provider_type)
        return provider.delete_cluster(name)
    
    def list_clusters(self, provider_type: str = "local") -> list:
        """List clusters for a provider."""
        provider = self._get_provider(provider_type)
        return provider.list_clusters()
    
    def get_cluster_info(
        self,
        name: str,
        provider_type: str = "local"
    ) -> Dict[str, Any]:
        """Get cluster information."""
        provider = self._get_provider(provider_type)
        return provider.get_cluster_info(name)
    
    def bootstrap_cluster(self, name: str, provider_type: str = "local") -> bool:
        """Bootstrap cluster with GitOps tools."""
        provider = self._get_provider(provider_type)
        return provider.bootstrap_cluster(name)
