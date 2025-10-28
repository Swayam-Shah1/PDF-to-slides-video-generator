"""
Content Analyzer
Analyzes content and ranks sections by importance
"""
from typing import List, Dict, Any
from collections import Counter
from utils.config_manager import ConfigManager
from utils.logger import Logger
from utils.text_processor import TextProcessor


class ContentAnalyzer:
    """Analyzes document content and ranks sections"""
    
    def __init__(self, config: ConfigManager, logger: Logger):
        """
        Initialize content analyzer
        
        Args:
            config: Configuration manager
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.text_processor = TextProcessor()
        self.max_slides = config.get_value('analysis.max_slides', 10)
    
    def split_into_sections(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split document into sections
        
        Args:
            doc: DocumentStructure dictionary
            
        Returns:
            List of section dictionaries
        """
        return doc.get('sections', [])
    
    def calculate_importance_scores(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate importance scores for sections
        
        Args:
            sections: List of sections
            
        Returns:
            Sections with importance scores
        """
        scored_sections = []
        
        for section in sections:
            text = ' '.join(section.get('paragraphs', []))
            
            # Calculate score based on multiple factors
            word_count = self.text_processor.word_count(text)
            
            # Factor 1: Length (longer = more important)
            length_score = min(word_count / 100, 1.0)
            
            # Factor 2: Keyword density
            keywords = self.text_processor.extract_keywords(text, n=10)
            keyword_score = min(len(keywords) / 10, 1.0)
            
            # Factor 3: Position (earlier = more important)
            position = section.get('page_numbers', [])
            if position:
                page_num = min(position)
                total_pages = 50  # Approximate
                position_score = 1.0 - min(page_num / total_pages, 1.0)
            else:
                position_score = 0.5
            
            # Combined score
            importance_score = (length_score * 0.4) + (keyword_score * 0.3) + (position_score * 0.3)
            
            section['importance_score'] = importance_score
            scored_sections.append(section)
        
        return scored_sections
    
    def rank_sections(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Rank and select top sections for slides
        
        Args:
            doc: DocumentStructure dictionary
            
        Returns:
            List of top-ranked sections
        """
        self.logger.info("Analyzing document structure...")
        
        sections = self.split_into_sections(doc)
        
        if not sections:
            self.logger.warning("No sections found in document")
            return []
        
        # Calculate importance scores
        scored_sections = self.calculate_importance_scores(sections)
        
        # Keep original order (don't sort by importance)
        # Select top N sections based on importance but preserve their original order
        # First, identify the top N by importance
        sorted_by_importance = sorted(scored_sections, key=lambda x: x.get('importance_score', 0), reverse=True)
        top_important = sorted_by_importance[:self.max_slides]
        
        # Get the page numbers of top important sections
        top_page_numbers = {min(s.get('page_numbers', [999])) for s in top_important if s.get('page_numbers')}
        
        # Now get those sections in their original order
        selected = []
        seen_pages = set()
        for section in scored_sections:
            page_num = min(section.get('page_numbers', [999])) if section.get('page_numbers') else 999
            if page_num in top_page_numbers and page_num not in seen_pages:
                selected.append(section)
                seen_pages.add(page_num)
                if len(selected) >= self.max_slides:
                    break
        
        self.logger.info(f"Selected {len(selected)} sections for slides")
        
        return selected

