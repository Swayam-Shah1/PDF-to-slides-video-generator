"""
Image Processor
Handles image processing and generation
"""
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional, List
import os


class ImageProcessor:
    """Processes and manipulates images"""
    
    def resize_image(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """
        Resize image to target size
        
        Args:
            image: PIL Image object
            size: Target size (width, height)
            
        Returns:
            Resized image
        """
        return image.resize(size, Image.Resampling.LANCZOS)
    
    def add_text_to_image(self, image: Image.Image, text: str, position: Tuple[int, int], 
                          font_size: int = 20) -> Image.Image:
        """
        Add text overlay to image at position
        
        Args:
            image: PIL Image object
            text: Text to add
            position: Text position (x, y)
            font_size: Font size
            
        Returns:
            Image with text overlay
        """
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        draw.text(position, text, fill="black", font=font)
        return image
    
    def create_simple_diagram(self, keywords: List[str], size: Tuple[int, int] = (800, 600)) -> Image.Image:
        """
        Create simple shape-based diagram from keywords
        
        Args:
            keywords: List of keywords
            size: Image size (width, height)
            
        Returns:
            Generated image
        """
        # Create a simple image with shapes
        img = Image.new('RGB', size, color='#E8F4F8')
        draw = ImageDraw.Draw(img)
        
        # Draw simple geometric shapes based on keywords
        colors = ['#4A90E2', '#50C878', '#F5A623', '#E74C3C', '#9B59B6']
        
        for i, keyword in enumerate(keywords[:5]):  # Max 5 shapes
            color = colors[i % len(colors)]
            
            # Draw different shapes based on position
            x = 100 + (i * 150) % (size[0] - 200)
            y = 100 + (i * 100) % (size[1] - 200)
            
            # Draw circle
            bbox = (x, y, x + 100, y + 100)
            draw.ellipse(bbox, fill=color, outline='#FFFFFF', width=3)
            
            # Add simple text (first letter)
            if keyword:
                draw.text((x + 45, y + 35), keyword[0].upper(), fill='white', font=ImageFont.load_default())
        
        return img
    
    def convert_to_png(self, image: Image.Image, output_path: str) -> None:
        """
        Convert image to PNG and save
        
        Args:
            image: PIL Image object
            output_path: Output file path
        """
        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path, 'PNG')
    
    def create_placeholder_image(self, size: Tuple[int, int] = (800, 600), 
                                 color: str = "#E8F4F8", text: str = "") -> Image.Image:
        """
        Create a placeholder image
        
        Args:
            size: Image size (width, height)
            color: Background color (hex)
            text: Optional text overlay
            
        Returns:
            Placeholder image
        """
        img = Image.new('RGB', size, color=color)
        
        if text:
            draw = ImageDraw.Draw(img)
            w, h = draw.textsize(text, ImageFont.load_default())
            position = ((size[0] - w) // 2, (size[1] - h) // 2)
            draw.text(position, text, fill='#666666', font=ImageFont.load_default())
        
        return img

