"""
File Manager
Handles file operations and directory management
"""
import os
import shutil
from pathlib import Path
from typing import Optional


class FileManager:
    """Manages file operations"""
    
    @staticmethod
    def create_output_directory(path: str) -> str:
        """
        Create output directory if it doesn't exist
        
        Args:
            path: Directory path
            
        Returns:
            Absolute path to directory
        """
        abs_path = os.path.abspath(path)
        os.makedirs(abs_path, exist_ok=True)
        return abs_path
    
    @staticmethod
    def validate_pdf_file(path: str) -> bool:
        """
        Validate that PDF file exists and is readable
        
        Args:
            path: PDF file path
            
        Returns:
            True if valid, False otherwise
        """
        if not os.path.exists(path):
            return False
        
        if not path.lower().endswith('.pdf'):
            return False
        
        # Check if file is readable
        try:
            with open(path, 'rb') as f:
                f.read(4)  # Try to read first bytes
            return True
        except Exception:
            return False
    
    @staticmethod
    def copy_file(source: str, dest: str) -> None:
        """
        Copy file from source to destination
        
        Args:
            source: Source file path
            dest: Destination file path
            
        Raises:
            FileNotFoundError: If source file doesn't exist
        """
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source file not found: {source}")
        
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(source, dest)
    
    @staticmethod
    def cleanup_temp_files(pattern: str = "*.tmp") -> None:
        """
        Clean up temporary files matching pattern
        
        Args:
            pattern: File pattern to match (e.g., "*.tmp")
        """
        # This is a placeholder - actual implementation would use glob
        # For now, we'll clean up common temp directories
        temp_dirs = ["temp", "tmp"]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    print(f"Warning: Could not clean {temp_dir}: {e}")
    
    @staticmethod
    def get_file_size(path: str) -> int:
        """
        Get file size in bytes
        
        Args:
            path: File path
            
        Returns:
            File size in bytes
        """
        return os.path.getsize(path)
    
    @staticmethod
    def ensure_directory(path: str) -> None:
        """
        Ensure directory exists (create if not)
        
        Args:
            path: Directory path
        """
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def file_exists(path: str) -> bool:
        """
        Check if file exists
        
        Args:
            path: File path
            
        Returns:
            True if file exists
        """
        return os.path.exists(path)

