"""
Main CLI entry point for the pipeline
"""
import argparse
import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logger import Logger
from utils.file_manager import FileManager
from utils.config_manager import ConfigManager


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Visual Explanation Prototype - Convert PDF to Slides and Video'
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Path to input PDF file'
    )
    
    parser.add_argument(
        '-o', '--outdir',
        default='output',
        help='Output directory (default: output/)'
    )
    
    parser.add_argument(
        '-c', '--config',
        default='config/config.yaml',
        help='Config file path (default: config/config.yaml)'
    )
    
    parser.add_argument(
        '--max-slides',
        type=int,
        default=10,
        help='Maximum number of slides (default: 10)'
    )
    
    parser.add_argument(
        '--video-format',
        choices=['mp4', 'gif'],
        default='mp4',
        help='Output video format: mp4 or gif (default: mp4)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Initialize logger
    logger = Logger()
    if args.verbose:
        logger.logger.setLevel(logging.DEBUG)
    
    logger.info("Starting Visual Explanation Prototype Pipeline")
    
    # Validate input file
    if not FileManager.validate_pdf_file(args.input):
        logger.error(f"Invalid PDF file: {args.input}")
        sys.exit(1)
    
    # Load configuration
    config_manager = ConfigManager(args.config)
    config_manager.validate_config()
    
    # Override max_slides if specified
    if 'analysis' not in config_manager.config:
        config_manager.config['analysis'] = {}
    config_manager.config['analysis']['max_slides'] = args.max_slides
    
    # Override video format if specified
    if 'video' not in config_manager.config:
        config_manager.config['video'] = {}
    config_manager.config['video']['output_format'] = args.video_format
    
    # Create output directory
    output_dir = FileManager.create_output_directory(args.outdir)
    
    try:
        # Import and run pipeline
        from orchestrator import PipelineOrchestrator
        
        orchestrator = PipelineOrchestrator(config_manager, logger)
        result = orchestrator.execute_pipeline(args.input, output_dir)
        
        if result['status'] == 'success':
            logger.info("Pipeline completed successfully!")
            logger.info(f"Slides: {result.get('slides_path', 'N/A')}")
            logger.info(f"Video: {result.get('video_path', 'N/A')}")
            sys.exit(0)
        else:
            logger.error(f"Pipeline failed: {result.get('error_message', 'Unknown error')}")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        import traceback
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()

