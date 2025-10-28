"""
Logger
Handles logging throughout the application
"""
import logging
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path


class Logger:
    """Handles application logging"""
    
    _instance: Optional['Logger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.logger = logging.getLogger('visual_explanation')
            self.logger.setLevel(logging.INFO)
            
            # Avoid duplicate handlers
            if not self.logger.handlers:
                # Console handler
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel(logging.INFO)
                
                # Formatter
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                console_handler.setFormatter(formatter)
                
                self.logger.addHandler(console_handler)
    
    def initialize_logging(self, log_file: Optional[str] = None) -> None:
        """
        Initialize logging with optional file output
        
        Args:
            log_file: Optional log file path
        """
        if log_file:
            # Create directory if needed
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            
            # File handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            self.logger.addHandler(file_handler)
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def log_stage_completion(self, stage: str, duration: float) -> None:
        """
        Log completion of a pipeline stage
        
        Args:
            stage: Stage name
            duration: Duration in seconds
        """
        self.info(f"Stage '{stage}' completed in {duration:.2f} seconds")

