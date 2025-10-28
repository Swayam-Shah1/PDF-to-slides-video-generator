"""
Text Processor
Handles text processing and manipulation
"""
import re
from typing import List
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass


class TextProcessor:
    """Processes and manipulates text"""
    
    def __init__(self):
        """Initialize TextProcessor"""
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
    
    def normalize_text(self, text: str) -> str:
        """
        Remove extra whitespace and normalize line breaks
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Normalize line breaks
        text = text.replace('\n', ' ').replace('\r', ' ')
        # Strip leading/trailing whitespace
        return text.strip()
    
    def extract_keywords(self, text: str, n: int = 10) -> List[str]:
        """
        Extract top N keywords from text using simple frequency
        
        Args:
            text: Input text
            n: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        # Tokenize and normalize
        words = word_tokenize(text.lower())
        
        # Filter out stopwords and non-alphabetic tokens
        words = [w for w in words if w.isalpha() and w not in self.stop_words]
        
        # Count frequencies
        from collections import Counter
        word_freq = Counter(words)
        
        # Get top N
        return [word for word, _ in word_freq.most_common(n)]
    
    def word_count(self, text: str) -> int:
        """
        Count words in text
        
        Args:
            text: Input text
            
        Returns:
            Word count
        """
        words = word_tokenize(text)
        return len(words)
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        try:
            return sent_tokenize(text)
        except:
            # Fallback if NLTK fails
            return [s.strip() for s in text.split('.') if s.strip()]
    
    def remove_special_chars(self, text: str) -> str:
        """
        Remove special characters from text
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Keep alphanumeric, spaces, and common punctuation
        return re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', text)
    
    def truncate_words(self, text: str, max_words: int) -> str:
        """
        Truncate text to maximum number of words
        
        Args:
            text: Input text
            max_words: Maximum words
            
        Returns:
            Truncated text with ellipsis if needed
        """
        words = text.split()
        if len(words) <= max_words:
            return text
        
        return ' '.join(words[:max_words]) + '...'

