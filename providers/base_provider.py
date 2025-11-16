"""Abstract base class for cloud providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseProvider(ABC):
    """Abstract base class for cluster providers following Open/Closed Principle."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize provider with configuration.
        
        Args:
            config: Provider configuration
        """
        self.config = config
    
    @abstractmethod
    def create_cluster(self, name: str, **kwargs) -> bool:
        """
        Create a cluster.
        
        Args:
            name: Cluster name
            **kwargs: Additional provider-specific parameters
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_cluster(self, name: str) -> bool:
        """
        Delete a cluster.
        
        Args:
            name: Cluster name
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_clusters(self) -> list:
        """
        List all clusters.
        
        Returns:
            List of cluster names
        """
        pass
    
    @abstractmethod
    def get_cluster_info(self, name: str) -> Dict[str, Any]:
        """
        Get cluster information.
        
        Args:
            name: Cluster name
            
        Returns:
            Cluster information dictionary
        """
        pass
    
    @abstractmethod
    def bootstrap_cluster(self, name: str) -> bool:
        """
        Bootstrap cluster with GitOps tools.
        
        Args:
            name: Cluster name
            
        Returns:
            True if successful, False otherwise
        """
        pass
