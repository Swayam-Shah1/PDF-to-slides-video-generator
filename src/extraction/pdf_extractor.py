"""
PDF Extractor
Extracts structured text from PDF files
"""
import pdfplumber
from typing import Dict, Any, List
from utils.config_manager import ConfigManager
from utils.logger import Logger


class PDFExtractor:
    """Extracts text from PDF files"""
    
    def __init__(self, config: ConfigManager, logger: Logger):
        """
        Initialize PDF extractor
        
        Args:
            config: Configuration manager
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
    
    def load_pdf(self, pdf_path: str):
        """
        Load PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            pdfplumber PDF object
        """
        try:
            return pdfplumber.open(pdf_path)
        except Exception as e:
            self.logger.error(f"Failed to load PDF: {e}")
            raise
    
    def extract_text_structure(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract structured text from PDF with font-based heading detection
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            DocumentStructure dictionary
        """
        self.logger.info(f"Extracting text from: {pdf_path}")
        
        pdf = self.load_pdf(pdf_path)
        
        document_structure = {
            'metadata': {
                'title': 'Unknown',
                'author': 'Unknown',
                'total_pages': len(pdf.pages)
            },
            'pages': [],
            'sections': []
        }
        
        # First pass: analyze font sizes to determine heading threshold
        self.logger.info("Analyzing font sizes to detect headings...")
        font_sizes = self._analyze_font_sizes(pdf)
        self.logger.debug(f"Detected font size distribution: {font_sizes}")
        
        sections = []
        current_section = {'title': 'Introduction', 'paragraphs': [], 'page_numbers': []}
        section_id = 1
        
        for page_num, page in enumerate(pdf.pages, 1):
            page_data = {
                'page_number': page_num,
                'elements': []
            }
            
            # Extract text with character-level attributes
            text_content = page.extract_text()
            
            if text_content:
                # Analyze text with character attributes to find headings
                text_elements = self._extract_text_with_properties(page)
                
                # Group text elements into paragraphs
                paragraphs = self._group_into_paragraphs(text_elements)
                
                for para in paragraphs:
                    if not para['lines']:
                        continue
                        
                    first_line_text = para['lines'][0]['text']
                    first_line_props = para['lines'][0].get('properties', {})
                    
                    # Check if first line is a heading based on font properties
                    is_heading = self._is_heading_font_based(first_line_text, first_line_props, font_sizes)
                    
                    if is_heading and len(para['lines']) > 1:
                        # Extract just the heading text (may have extra words from body text)
                        # Split the first line where font changes from heading to body
                        heading_text = self._extract_heading_text(para['lines'][0], font_sizes)
                        
                        # This paragraph starts with a heading
                        # Save current section if it has content
                        if current_section['paragraphs']:
                            current_section['page_numbers'] = list(set(current_section['page_numbers']))
                            current_section['section_id'] = f'section_{section_id}'
                            sections.append(current_section.copy())
                            section_id += 1
                        
                        # Start new section with the heading as title
                        current_section = {
                            'section_id': f'section_{section_id}',
                            'title': heading_text,
                            'paragraphs': [],
                            'page_numbers': []
                        }
                        
                        # Add remaining lines as paragraphs
                        for remaining_line in para['lines'][1:]:
                            if remaining_line['text'] and len(remaining_line['text']) > 20:
                                current_section['paragraphs'].append(remaining_line['text'])
                                current_section['page_numbers'].append(page_num)
                    else:
                        # This is a regular paragraph - add to current section
                        full_para_text = '\n'.join(line['text'] for line in para['lines'])
                        if full_para_text and len(full_para_text) > 30:
                            current_section['paragraphs'].append(full_para_text)
                            current_section['page_numbers'].append(page_num)
            
            document_structure['pages'].append(page_data)
        
        # Add final section
        if current_section['paragraphs']:
            current_section['page_numbers'] = list(set(current_section['page_numbers']))
            sections.append(current_section)
        
        document_structure['sections'] = sections
        pdf.close()
        
        self.logger.info(f"Extracted {len(sections)} sections from {len(pdf.pages)} pages")
        
        return document_structure
    
    def _analyze_font_sizes(self, pdf) -> Dict[str, Any]:
        """
        Analyze font sizes across all pages to determine heading threshold
        
        Args:
            pdf: pdfplumber PDF object
            
        Returns:
            Dictionary with font size statistics
        """
        from collections import Counter
        
        font_size_counts = Counter()
        font_info = {'min': float('inf'), 'max': 0, 'sizes': []}
        
        # Sample first few pages for efficiency
        sample_pages = min(5, len(pdf.pages))
        
        for page in pdf.pages[:sample_pages]:
            chars = page.chars
            if chars:
                for char in chars:
                    size = char.get('size', 0)
                    if size > 0:
                        font_size_counts[size] += 1
                        font_info['sizes'].append(size)
                        font_info['min'] = min(font_info['min'], size)
                        font_info['max'] = max(font_info['max'], size)
        
        # Calculate median and mode
        if font_info['sizes']:
            sorted_sizes = sorted(font_info['sizes'])
            median_idx = len(sorted_sizes) // 2
            font_info['median'] = sorted_sizes[median_idx]
        
        # Most common font size is likely body text
        if font_size_counts:
            most_common_size, most_common_count = font_size_counts.most_common(1)[0]
            font_info['mode'] = most_common_size
            font_info['mode_count'] = most_common_count
            
            # Heading threshold: larger than 120% of most common size
            font_info['heading_threshold'] = most_common_size * 1.2
        else:
            font_info['heading_threshold'] = 12  # Default fallback
        
        return font_info
    
    def _extract_text_with_properties(self, page) -> List[Dict[str, Any]]:
        """
        Extract text with font properties from page
        
        Args:
            page: pdfplumber page object
            
        Returns:
            List of text elements with properties
        """
        # Use pdfplumber's words which preserves spacing
        words = page.extract_words()
        
        # Group words into lines based on vertical position
        lines = []
        current_line = {'text': '', 'words': [], 'bottom': None, 'properties': {}}
        
        for word in words:
            word_text = word.get('text', '')
            word_bottom = word.get('bottom', 0)
            
            # New line if vertical position changes significantly (3 points)
            if current_line['bottom'] is not None and abs(word_bottom - current_line['bottom']) > 3:
                if current_line['words']:
                    lines.append(current_line)
                current_line = {'text': '', 'words': [], 'bottom': word_bottom, 'properties': {}}
            
            # Update bottom position for line
            if current_line['bottom'] is None:
                current_line['bottom'] = word_bottom
            
            # Add word to current line with space
            if current_line['text']:
                current_line['text'] += ' '  # Add space between words
            current_line['text'] += word_text
            current_line['words'].append(word)
            
            # Use first word's properties for the line
            if not current_line['properties']:
                # Try to get font info from word coordinates if available
                current_line['properties'] = {
                    'size': word.get('size', 0),
                    'fontname': word.get('fontname', '')
                }
        
        if current_line['words']:
            lines.append(current_line)
        
        return lines
    
    def _group_into_paragraphs(self, text_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Group text lines into paragraphs
        
        Args:
            text_elements: List of line dictionaries
            
        Returns:
            List of paragraph dictionaries
        """
        paragraphs = []
        current_para = {'lines': []}
        
        for element in text_elements:
            text = element.get('text', '').strip()
            
            # New paragraph if empty line or significant gap
            if not text:
                if current_para['lines']:
                    paragraphs.append(current_para)
                current_para = {'lines': []}
            else:
                current_para['lines'].append({
                    'text': text,
                    'properties': element.get('properties', {})
                })
        
        if current_para['lines']:
            paragraphs.append(current_para)
        
        return paragraphs
    
    def _extract_heading_text(self, line_data: Dict[str, Any], font_sizes: Dict[str, Any]) -> str:
        """
        Extract just the heading text from a line that might contain mixed font sizes
        
        Args:
            line_data: Line dictionary with words and properties
            font_sizes: Font size analysis
            
        Returns:
            Heading text without trailing body text
        """
        full_text = line_data.get('text', '')
        words = line_data.get('words', [])
        
        if not words:
            return full_text.strip()
        
        # Find where heading font ends and body text begins
        heading_threshold = font_sizes.get('heading_threshold', 12)
        heading_words = []
        
        for word in words:
            word_size = word.get('size', 0)
            # If we encounter a word that's not a heading size, stop
            if word_size > 0 and word_size <= heading_threshold:
                # Check if this is actually body text
                # If we have at least a few heading words already, this is probably the boundary
                if len(heading_words) >= 2:
                    break
            
            heading_words.append(word.get('text', ''))
        
        # If we found heading words, return them
        if heading_words:
            heading_text = ''.join(heading_words).strip()
            # Clean up the text
            return heading_text
        
        # Fallback: return full text
        return full_text.strip()
    
    def _is_heading_font_based(self, text: str, properties: Dict[str, Any], font_sizes: Dict[str, Any]) -> bool:
        """
        Detect headings based on font properties
        
        Args:
            text: Text to check
            properties: Font properties of the text
            font_sizes: Font size analysis
            
        Returns:
            True if likely a heading
        """
        if not text or len(text) < 3:
            return False
        
        font_size = properties.get('size', 0)
        fontname = properties.get('fontname', '')
        
        # Check if font size is significantly larger than body text
        if font_size > font_sizes.get('heading_threshold', 12):
            self.logger.debug(f"Detected heading by font size: '{text[:50]}' (size: {font_size:.1f})")
            return True
        
        # Check if font name suggests bold or heading
        fontname_lower = fontname.lower()
        if any(indicator in fontname_lower for indicator in ['bold', 'black', 'heavy', 'extrabold']):
            self.logger.debug(f"Detected heading by font weight: '{text[:50]}' (font: {fontname})")
            return True
        
        # Fallback to heuristics if font info is not available
        if font_size == 0:
            return self._is_heading(text)  # Use old heuristic as fallback
        
        # Check if text is short and title case
        if len(text) < 150:
            if text.istitle() and len(text) < 100:
                return True
            
            # Check for all caps (common in headings)
            if text.isupper() and len(text) < 80:
                return True
        
        return False
    
    def _is_heading(self, text: str) -> bool:
        """
        Generic heuristic to detect if text is a heading (fallback method)
        Uses text characteristics rather than keywords for generic detection
        
        Args:
            text: Text to check
            
        Returns:
            True if likely a heading
        """
        if not text or len(text) < 3:
            return False
        
        text_len = len(text)
        words = text.split()
        
        # Very short text (likely heading)
        if text_len < 20 and len(words) < 5:
            return True
        
        # Short text in title case (common heading pattern)
        if text.istitle() and text_len < 100 and len(words) < 10:
            return True
        
        # All caps text that's not too long (common in headings)
        if text.isupper() and text_len < 80 and len(words) < 12:
            return True
        
        # Text with multiple capitalized words (heading pattern)
        if len(words) < 8 and text_len < 80:
            capitalized_count = sum(1 for w in words if w and w[0].isupper())
            # If most words are capitalized
            if capitalized_count >= len(words) * 0.7:
                return True
        
        # Short lines ending with colon (common heading pattern)
        if text.endswith(':') and text_len < 100:
            return True
        
        # Very short text relative to typical paragraph length
        if text_len < 150 and len(words) < 15:
            # Additional check: no sentence-ending punctuation in middle
            # (headings rarely have periods, question marks, etc. in the middle)
            mid_text = text[10:-10] if text_len > 20 else text
            if not any(punct in mid_text for punct in ['.', '!', '?', ',']):
                return True
            
        return False

