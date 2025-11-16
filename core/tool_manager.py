"""Tool installation and management."""

import subprocess
from typing import List, Dict
from utils.logger import setup_logger, log_success, log_error, log_info

logger = setup_logger(__name__)


class ToolManager:
    """Manages installation and listing of development tools."""
    
    SUPPORTED_TOOLS = {
        "kubectl": {
            "description": "Kubernetes command-line tool",
            "check_command": ["kubectl", "version", "--client"],
        },
        "helm": {
            "description": "Kubernetes package manager",
            "check_command": ["helm", "version"],
        },
        "k3d": {
            "description": "k3s in Docker - lightweight Kubernetes",
            "check_command": ["k3d", "version"],
        },
        "argocd": {
            "description": "GitOps toolkit for Kubernetes",
            "check_command": ["argocd", "version"],
        },
    }
    
    def list_tools(self) -> Dict[str, Dict]:
        """
        List all supported tools.
        
        Returns:
            Dictionary of tool names and their information
        """
        return self.SUPPORTED_TOOLS
    
    def check_tool_installed(self, tool_name: str) -> bool:
        """
        Check if a tool is installed.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            True if installed, False otherwise
        """
        if tool_name not in self.SUPPORTED_TOOLS:
            return False
        
        check_command = self.SUPPORTED_TOOLS[tool_name]["check_command"]
        
        try:
            result = subprocess.run(
                check_command,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_tool(self, tool_name: str) -> bool:
        """
        Install a tool (placeholder - actual implementation would vary by OS).
        
        Args:
            tool_name: Name of the tool to install
            
        Returns:
            True if successful
        """
        if tool_name not in self.SUPPORTED_TOOLS:
            log_error(f"Tool '{tool_name}' is not supported")
            return False
        
        if self.check_tool_installed(tool_name):
            log_info(f"Tool '{tool_name}' is already installed")
            return True
        
        log_info(f"Installing {tool_name}...")
        
        # Placeholder: Real implementation would use package managers
        # or download binaries based on OS
        log_info(f"Placeholder: Would install {tool_name} here")
        log_info(f"Please install {tool_name} manually for now")
        
        return False
    
    def install_multiple_tools(self, tool_names: List[str]) -> Dict[str, bool]:
        """
        Install multiple tools.
        
        Args:
            tool_names: List of tool names
            
        Returns:
            Dictionary of tool names and installation status
        """
        results = {}
        for tool_name in tool_names:
            results[tool_name] = self.install_tool(tool_name)
        return results
