"""
Pipeline Orchestrator
Coordinates all pipeline stages
"""
import time
import os
from typing import Dict, Any, Optional
from utils.logger import Logger
from utils.config_manager import ConfigManager


class PipelineOrchestrator:
    """Orchestrates the complete pipeline execution"""
    
    def __init__(self, config_manager: ConfigManager, logger: Logger):
        """
        Initialize orchestrator
        
        Args:
            config_manager: Configuration manager
            logger: Logger instance
        """
        self.config = config_manager
        self.logger = logger
        self.start_time = None
    
    def execute_pipeline(self, pdf_path: str, output_dir: str) -> Dict[str, Any]:
        """
        Execute the complete pipeline
        
        Args:
            pdf_path: Path to input PDF
            output_dir: Output directory
            
        Returns:
            Result dictionary with status and outputs
        """
        self.start_time = time.time()
        
        try:
            # Stage 1: PDF Extraction
            self.logger.info("=" * 60)
            self.logger.info("STAGE 1: PDF Extraction")
            self.logger.info("=" * 60)
            
            document_structure = self._stage_1_extraction(pdf_path)
            
            # Stage 2: Content Analysis
            self.logger.info("=" * 60)
            self.logger.info("STAGE 2: Content Analysis")
            self.logger.info("=" * 60)
            
            ranked_sections = self._stage_2_analysis(document_structure)
            
            # Stage 3: Summarization
            self.logger.info("=" * 60)
            self.logger.info("STAGE 3: Summarization")
            self.logger.info("=" * 60)
            
            slide_contents = self._stage_3_summarization(ranked_sections)
            
            # Stage 4: Visual Generation
            self.logger.info("=" * 60)
            self.logger.info("STAGE 4: Visual Generation")
            self.logger.info("=" * 60)
            
            enriched_slides = self._stage_4_visual_generation(slide_contents)
            
            # Stage 5: Slide Assembly
            self.logger.info("=" * 60)
            self.logger.info("STAGE 5: Slide Assembly")
            self.logger.info("=" * 60)
            
            presentation = self._stage_5_slide_assembly(enriched_slides, output_dir)
            
            # Stage 6: Video Generation
            self.logger.info("=" * 60)
            self.logger.info("STAGE 6: Video Generation")
            self.logger.info("=" * 60)
            
            video_path = self._stage_6_video_generation(presentation, output_dir)
            
            # Calculate total duration
            total_duration = time.time() - self.start_time
            
            self.logger.info("=" * 60)
            self.logger.info(f"Pipeline completed in {total_duration:.2f} seconds")
            self.logger.info("=" * 60)
            
            return {
                'status': 'success',
                'slides_path': presentation,
                'video_path': video_path,
                'duration': total_duration
            }
        
        except Exception as e:
            duration = time.time() - self.start_time if self.start_time else 0
            self.logger.error(f"Pipeline failed after {duration:.2f} seconds")
            return {
                'status': 'error',
                'error_message': str(e),
                'duration': duration
            }
    
    def _stage_1_extraction(self, pdf_path: str) -> Dict[str, Any]:
        """Stage 1: Extract PDF content"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from extraction.pdf_extractor import PDFExtractor
        
        extractor = PDFExtractor(self.config, self.logger)
        return extractor.extract_text_structure(pdf_path)
    
    def _stage_2_analysis(self, doc: Dict[str, Any]) -> list:
        """Stage 2: Analyze and rank content"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from analysis.content_analyzer import ContentAnalyzer
        
        analyzer = ContentAnalyzer(self.config, self.logger)
        return analyzer.rank_sections(doc)
    
    def _stage_3_summarization(self, sections: list) -> list:
        """Stage 3: Create slide content"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from summarization.summarizer import Summarizer
        
        summarizer = Summarizer(self.config, self.logger)
        return [summarizer.summarize_section(section) for section in sections]
    
    def _stage_4_visual_generation(self, slides: list) -> list:
        """Stage 4: Add visuals to slides"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from visual.visual_generator import VisualGenerator
        
        generator = VisualGenerator(self.config, self.logger)
        return generator.generate_for_slides(slides)
    
    def _stage_5_slide_assembly(self, slides: list, output_dir: str) -> str:
        """Stage 5: Create PowerPoint presentation"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from slide.slide_assembler import SlideAssembler
        
        assembler = SlideAssembler(self.config, self.logger)
        output_path = f"{output_dir}/slides.pptx"
        assembler.create_presentation(slides, output_path)
        return output_path
    
    def _stage_6_video_generation(self, presentation_path: str, output_dir: str) -> str:
        """Stage 6: Generate video"""
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from video.video_generator import VideoGenerator
        
        generator = VideoGenerator(self.config, self.logger)
        
        # Determine output path based on format
        video_format = self.config.get_value('video.output_format', 'mp4')
        if video_format == 'gif':
            output_path = f"{output_dir}/video.gif"
        else:
            output_path = f"{output_dir}/video.mp4"
        
        generator.create_video(presentation_path, output_path)
        return output_path
