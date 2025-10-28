"""
Visual Generator
Generates or selects visual elements for slides
"""
from typing import List, Dict, Any
from utils.config_manager import ConfigManager
from utils.logger import Logger
from utils.image_processor import ImageProcessor
from utils.text_processor import TextProcessor
import os


class VisualGenerator:
    """Generates visual elements for slides"""
    
    def __init__(self, config: ConfigManager, logger: Logger):
        """
        Initialize visual generator
        
        Args:
            config: Configuration manager
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.image_processor = ImageProcessor()
        self.text_processor = TextProcessor()
        
        self.strategy = config.get_value('visuals.strategy', 'simple_generation')
        self.image_width = config.get_value('visuals.image_width', 800)
        self.image_height = config.get_value('visuals.image_height', 600)
    
    def generate_for_slides(self, slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add visuals to slides
        
        Args:
            slides: List of SlideContent dictionaries
            
        Returns:
            List of enriched SlideContent dictionaries
        """
        self.logger.info(f"Generating visuals for {len(slides)} slides...")
        
        enriched_slides = []
        
        for i, slide in enumerate(slides):
            # Extract keywords
            keywords = self._extract_keywords_from_slide(slide)
            
            # Generate or select image
            if self.strategy == 'icon_library':
                visual_path = self.select_icon(keywords)
            else:
                visual_path = self.generate_simple_image(keywords, f"slide_{i+1}")
            
            # Add visual to slide
            slide['visual'] = {
                'type': self.strategy,
                'path': visual_path,
                'keywords_matched': keywords
            }
            
            enriched_slides.append(slide)
        
        self.logger.info("Visual generation complete")
        
        return enriched_slides
    
    def _extract_keywords_from_slide(self, slide: Dict[str, Any]) -> List[str]:
        """
        Extract keywords from slide content
        
        Args:
            slide: SlideContent dictionary
            
        Returns:
            List of keywords
        """
        # Combine title and bullets
        text = f"{slide.get('title', '')} {' '.join(slide.get('bullets', []))}"
        
        return self.text_processor.extract_keywords(text, n=3)
    
    def select_icon(self, keywords: List[str]) -> str:
        """
        Select icon based on keywords
        
        Args:
            keywords: List of keywords
            
        Returns:
            Icon file path
        """
        # Placeholder: return a default icon path
        # In full implementation, would match keywords to icon library
        return "assets/icons/default.png"
    
    def generate_simple_image(self, keywords: List[str], filename: str) -> str:
        """
        Generate a simple image from keywords
        
        Args:
            keywords: List of keywords
            filename: Base filename for image
            
        Returns:
            Image file path
        """
        # Create directory for images
        image_dir = "temp/images"
        os.makedirs(image_dir, exist_ok=True)
        
        # Generate simple diagram
        image = self.image_processor.create_simple_diagram(
            keywords,
            size=(self.image_width, self.image_height)
        )
        
        # Save image
        image_path = f"{image_dir}/{filename}.png"
        self.image_processor.convert_to_png(image, image_path)
        
        return image_path

