"""
Summarizer
Summarizes content into slide-appropriate text
"""
from typing import Dict, Any
from utils.config_manager import ConfigManager
from utils.logger import Logger
from utils.text_processor import TextProcessor


class Summarizer:
    """Summarizes content for slides"""
    
    def __init__(self, config: ConfigManager, logger: Logger):
        """
        Initialize summarizer
        
        Args:
            config: Configuration manager
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.text_processor = TextProcessor()
        
        self.max_title_words = config.get_value('summarization.max_title_words', 20)
        self.max_bullet_words = config.get_value('summarization.max_bullet_words', 15)
        self.max_speaker_words = config.get_value('summarization.max_speaker_words', 25)
        self.bullet_count = config.get_value('summarization.bullet_count', 2)
    
    def summarize_section(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize a section into slide content
        
        Args:
            section: Section dictionary
            
        Returns:
            SlideContent dictionary
        """
        text = ' '.join(section.get('paragraphs', []))
        title = section.get('title', 'Untitled')
        
        # Generate title
        slide_title = self.generate_title(title, text)
        
        # Generate bullet points
        bullets = self.generate_bullet_points(text)
        
        # Generate speaker notes
        speaker_notes = self.generate_speaker_notes(text)
        
        return {
            'slide_number': len(section.get('page_numbers', [])),
            'title': slide_title,
            'bullets': bullets,
            'speaker_notes': speaker_notes,
            'original_section': section
        }
    
    def generate_title(self, section_title: str, text: str, max_words: int = None) -> str:
        """
        Generate slide title
        
        Args:
            section_title: Original section title
            text: Section text
            max_words: Maximum words (optional)
            
        Returns:
            Slide title
        """
        if max_words is None:
            max_words = self.max_title_words
        
        # Use section title if short enough
        words = section_title.split()
        if len(words) <= max_words:
            return section_title
        
        # Otherwise, truncate or summarize
        return self.text_processor.truncate_words(section_title, max_words)
    
    def generate_bullet_points(self, text: str, count: int = None) -> list:
        """
        Generate bullet points from text
        
        Args:
            text: Input text
            count: Number of bullets (optional)
            
        Returns:
            List of bullet point strings
        """
        if count is None:
            count = self.bullet_count
        
        if not text or len(text.strip()) < 20:
            return ["Key information", "Main points"] * ((count + 1) // 2)
        
        # Split into sentences
        sentences = self.text_processor.split_into_sentences(text)
        
        if not sentences:
            # Fallback: Split by clauses or periods
            parts = text.split('. ')
            if len(parts) < 2:
                parts = text.split(', ')
            sentences = [p.strip() + '.' if not p.endswith('.') else p.strip() for p in parts if len(p.strip()) > 20]
        
        # Select the best sentences - prioritize medium length sentences
        # (not too short, not too long)
        scored_sentences = []
        for sent in sentences:
            sent_len = len(sent.split())
            # Prefer sentences with 10-25 words
            if 10 <= sent_len <= 25:
                score = 1.0
            elif 5 <= sent_len < 10:
                score = 0.7
            elif 25 < sent_len <= 40:
                score = 0.8
            else:
                score = 0.5
            
            scored_sentences.append((score, sent))
        
        # Sort by score and select top N
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        selected = [sent for _, sent in scored_sentences[:count]]
        
        # Clean and truncate each sentence for bullets
        bullets = []
        for sent in selected:
            cleaned = self.text_processor.normalize_text(sent)
            # Truncate to appropriate length
            truncated = self.text_processor.truncate_words(cleaned, self.max_bullet_words)
            # Filter out short or meaningless text
            if truncated.strip() and len(truncated.strip()) > 15:
                # Skip if it's just fragments or gibberish
                words = truncated.strip().split()
                if len(words) >= 3:  # At least 3 words to be meaningful
                    bullets.append(truncated)
        
        # If we don't have enough bullets, add more
        if len(bullets) < count and sentences:
            remaining = sentences[len(bullets):]
            for sent in remaining[:count - len(bullets)]:
                cleaned = self.text_processor.normalize_text(sent)
                truncated = self.text_processor.truncate_words(cleaned, self.max_bullet_words)
                # Filter out short or meaningless text
                if truncated.strip() and truncated not in bullets:
                    words = truncated.strip().split()
                    if len(words) >= 3:  # At least 3 words
                        bullets.append(truncated)
        
        # Ensure we have at least count bullets
        while len(bullets) < count:
            # Extract key phrases as bullets
            key_phrases = self.text_processor.extract_keywords(text, n=3)
            if key_phrases:
                bullets.append(f"Key concepts: {', '.join(key_phrases[:3])}")
            else:
                bullets.append("Important points covered")
            if len(bullets) >= count:
                break
        
        return bullets[:count]
    
    def generate_speaker_notes(self, text: str, max_words: int = None) -> str:
        """
        Generate speaker notes from text
        
        Args:
            text: Input text
            max_words: Maximum words (optional)
            
        Returns:
            Speaker notes string
        """
        if max_words is None:
            max_words = self.max_speaker_words
        
        # Take first sentence as speaker notes
        sentences = self.text_processor.split_into_sentences(text)
        if sentences:
            notes = sentences[0]
        else:
            notes = text
        
        # Clean and truncate
        cleaned = self.text_processor.normalize_text(notes)
        truncated = self.text_processor.truncate_words(cleaned, max_words)
        
        return truncated if truncated.strip() else "Important points covered in this slide."

