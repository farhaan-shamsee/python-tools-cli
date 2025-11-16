"""Local k3d cluster provider implementation."""

import subprocess
from typing import Dict, Any, List
from providers.base_provider import BaseProvider
from utils.exceptions import ClusterOperationError
from utils.logger import setup_logger, log_success, log_error, log_info

logger = setup_logger(__name__)


class LocalProvider(BaseProvider):
    """Local k3d cluster provider."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize local provider."""
        super().__init__(config)
        self.provider_type = "k3d"
    
    def _run_command(self, command: List[str]) -> tuple:
        """
        Run shell command and return output.
        
        Args:
            command: Command as list of strings
            
        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return "", str(e), 1
    
    def create_cluster(self, name: str, **kwargs) -> bool:
        """
        Create a local k3d cluster.
        
        Args:
            name: Cluster name
            **kwargs: Additional parameters (ports_to_open, registry, etc.)
            
        Returns:
            True if successful
        """
        log_info(f"Creating local k3d cluster: {name}")
        
        # Build k3d command
        command = ["k3d", "cluster", "create", name]
        
        # Add port mappings if specified
        ports = kwargs.get("ports_to_open", self.config.get("portsToOpen", ""))
        if ports:
            for port in ports.split(","):
                command.extend(["-p", f"{port.strip()}:{port.strip()}@loadbalancer"])
        
        # Add registry if specified
        if kwargs.get("use_registry", self.config.get("useLocalRegistry", False)):
            registry_name = f"{name}-registry"
            command.extend(["--registry-create", registry_name])
        
        stdout, stderr, returncode = self._run_command(command)
        
        if returncode == 0:
            log_success(f"Cluster '{name}' created successfully")
            return True
        else:
            log_error(f"Failed to create cluster: {stderr}")
            raise ClusterOperationError(f"Cluster creation failed: {stderr}")
    
    def delete_cluster(self, name: str) -> bool:
        """Delete a local k3d cluster."""
        log_info(f"Deleting local k3d cluster: {name}")
        
        command = ["k3d", "cluster", "delete", name]
        stdout, stderr, returncode = self._run_command(command)
        
        if returncode == 0:
            log_success(f"Cluster '{name}' deleted successfully")
            return True
        else:
            log_error(f"Failed to delete cluster: {stderr}")
            raise ClusterOperationError(f"Cluster deletion failed: {stderr}")
    
    def list_clusters(self) -> list:
        """List all local k3d clusters."""
        command = ["k3d", "cluster", "list", "--no-headers"]
        stdout, stderr, returncode = self._run_command(command)
        
        if returncode == 0:
            clusters = [line.split()[0] for line in stdout.strip().split("\n") if line]
            return clusters
        else:
            log_error(f"Failed to list clusters: {stderr}")
            return []
    
    def get_cluster_info(self, name: str) -> Dict[str, Any]:
        """Get information about a specific cluster."""
        clusters = self.list_clusters()
        
        if name in clusters:
            return {
                "name": name,
                "type": "local",
                "provider": "k3d",
                "status": "running"
            }
        else:
            return {}
    
    def bootstrap_cluster(self, name: str) -> bool:
        """
        Bootstrap cluster with Flux CD and other GitOps tools.
        
        This is a placeholder for Flux installation logic.
        """
        log_info(f"Bootstrapping cluster '{name}' with Flux CD")
        
        # Placeholder: In real implementation, install Flux CD
        # flux bootstrap github --owner=<org> --repository=<repo> --path=clusters/<name>
        
        log_success(f"Cluster '{name}' bootstrapped successfully (placeholder)")
        return True
