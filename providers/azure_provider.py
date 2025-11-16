"""Azure AKS cluster provider (placeholder for future implementation)."""

from typing import Dict, Any
from providers.base_provider import BaseProvider
from utils.logger import log_info, log_warning


class AzureProvider(BaseProvider):
    """Azure AKS cluster provider (placeholder)."""
    
    def create_cluster(self, name: str, **kwargs) -> bool:
        log_warning("Azure AKS provider not yet implemented")
        log_info(f"Placeholder: Would create AKS cluster '{name}'")
        return False
    
    def delete_cluster(self, name: str) -> bool:
        log_warning("Azure AKS provider not yet implemented")
        return False
    
    def list_clusters(self) -> list:
        log_warning("Azure AKS provider not yet implemented")
        return []
    
    def get_cluster_info(self, name: str) -> Dict[str, Any]:
        log_warning("Azure AKS provider not yet implemented")
        return {}
    
    def bootstrap_cluster(self, name: str) -> bool:
        log_warning("Azure AKS provider not yet implemented")
        return False
