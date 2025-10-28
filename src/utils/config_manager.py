"""
Configuration Manager
Handles loading and validation of configuration
"""
import yaml
import os
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize ConfigManager
        
        Args:
            config_path: Path to config file (default: config/config.yaml)
        """
        if config_path is None:
            # Default to config/config.yaml relative to project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            self.config_path = os.path.join(project_root, "config", "config.yaml")
        else:
            self.config_path = config_path
        
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {self.config_path}")
            self.config = self._get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "input": {"validate_format": True},
            "extraction": {"library": "pdfplumber"},
            "analysis": {"max_slides": 10, "min_slides": 6},
            "summarization": {"max_title_words": 20, "max_bullet_words": 15},
            "visuals": {"strategy": "simple_generation"},
            "slides": {"aspect_ratio": "16:9", "theme": "modern"},
            "video": {"fps": 30, "resolution": {"width": 1920, "height": 1080}},
            "output": {"directory": "output", "slides_filename": "slides.pptx", "video_filename": "video.mp4"}
        }
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get config value by key path
        
        Args:
            key: Dot-separated key path (e.g., "video.fps")
            default: Default value if key not found
            
        Returns:
            Config value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Alias for get_value"""
        return self.get_value(key, default)
    
    def validate_config(self) -> bool:
        """
        Validate that all required config keys are present
        
        Returns:
            True if valid, False otherwise
        """
        required_keys = [
            "input",
            "extraction",
            "analysis",
            "output"
        ]
        
        for key in required_keys:
            if key not in self.config:
                print(f"Warning: Missing required config key: {key}")
                return False
        
        return True
    
    def get_config(self) -> Dict[str, Any]:
        """Get full configuration dictionary"""
        return self.config

