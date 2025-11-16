"""Configuration file handling."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from utils.exceptions import ConfigurationError
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ConfigHandler:
    """Handles loading and managing configuration files."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize config handler.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or "config.yaml"
        self._config: Optional[Dict[str, Any]] = None
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Returns:
            Configuration dictionary
            
        Raises:
            ConfigurationError: If config file is invalid or missing
        """
        try:
            path = Path(self.config_path)
            if not path.exists():
                raise ConfigurationError(f"Configuration file not found: {self.config_path}")
            
            with open(path, 'r') as f:
                self._config = yaml.safe_load(f)
            
            logger.info(f"Configuration loaded from {self.config_path}")
            return self._config
        
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in config file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'clusterConfig.name')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        if self._config is None:
            self.load()
        
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def save(self, config: Dict[str, Any], output_path: Optional[str] = None):
        """
        Save configuration to YAML file.
        
        Args:
            config: Configuration dictionary
            output_path: Output file path (default: self.config_path)
        """
        path = Path(output_path or self.config_path)
        
        try:
            with open(path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            logger.info(f"Configuration saved to {path}")
        except Exception as e:
            raise ConfigurationError(f"Error saving configuration: {e}")
    
    @staticmethod
    def create_default_config(output_path: str = "config.yaml"):
        """
        Create a default configuration file.
        
        Args:
            output_path: Path to save default config
        """
        default_config = {
            "credentials": {
                "accessToken": ""
            },
            "templateConfig": {
                "templateProvider": "local",
                "templateTag": "3.1.0",
                "templateUrl": ""
            },
            "clusterConfig": {
                "name": "my-cluster",
                "type": "local",
                "groupId": 0,
                "useLocalRegistry": True,
                "portsToOpen": "80,443"
            },
            "tools": ["kubectl", "helm", "k3d"]
        }
        
        handler = ConfigHandler(output_path)
        handler.save(default_config, output_path)
