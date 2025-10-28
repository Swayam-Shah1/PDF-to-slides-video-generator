# PDF to Slides & Video Generator

A complete pipeline that converts PDF documents into professional slide presentations (PowerPoint) and animated explainer videos with Text-to-Speech narration.

## Project Overview

This tool automatically extracts content from PDF files, analyzes and summarizes key sections, generates visual slides, and creates animated videos with synchronized audio narration. Perfect for creating educational content, presentations, and explainer videos from technical documents.

### Key Features

- **Intelligent PDF Extraction**: Font-based heading detection using size/weight analysis (no hardcoded keywords)
- **Smart Content Analysis**: Identifies key concepts and ranks sections while preserving document order
- **Dynamic Summarization**: Creates concise bullet points using sentence scoring and keyword extraction
- **Automatic Visual Generation**: Generates simple diagrams and selects relevant visual elements
- **Dynamic Font Sizing**: Automatically adjusts font sizes based on content length to prevent overflow
- **Professional Slides**: Creates PowerPoint presentations with proper bullet formatting and spacing
- **Video Generation**: Creates MP4 videos with TTS narration using speaker notes for natural context
- **Perfect Sync**: Reads actual audio duration to ensure perfect audio-video synchronization
- **Adaptive Layout**: Two-column layout with visuals, full-width without

### Pipeline Architecture

The system processes documents through six sequential stages:

```
PDF → Extract → Analyze → Summarize → Visualize → Assemble Slides → Generate Video
```

**Stage 1: PDF Extraction**
- Parse PDF using pdfplumber
- Extract text with font properties (size, weight, name)
- Group content into paragraphs and sections
- Detect headings based on font analysis (no keywords needed)

**Stage 2: Content Analysis**
- Extract key phrases and concepts
- Score sections by importance (word count, key terms, position)
- Rank and select top N sections while preserving order

**Stage 3: Summarization**
- Generate concise titles (6-20 words)
- Create bullet points (8-15 words each) using sentence scoring
- Generate speaker notes (15-25 words) for natural narration

**Stage 4: Visual Generation**
- Extract keywords from slide content
- Generate simple diagrams or select icons
- Assign visual elements to slides

**Stage 5: Slide Assembly**
- Create PowerPoint presentation
- Apply dynamic font sizing for titles and bullets
- Format bullets with proper spacing and indentation
- Add visuals (two-column layout when present)

**Stage 6: Video Generation**
- Extract slide content from PPTX
- Generate TTS audio from speaker notes
- Create video frames with formatted text
- Merge audio with video ensuring perfect sync

### Quick Start

#### Prerequisites

- Python 3.8 or higher
- pip

#### Installation

1. Clone this repository or navigate to the project directory:
```bash
cd infoware_assessment
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note:** For video generation, the pipeline will use `imageio-ffmpeg` which is automatically installed. If you encounter video generation issues, you may need to install ffmpeg separately:
- Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

#### Usage

Run the pipeline with a PDF file:

```bash
python src/cli/run_pipeline.py -i sample.pdf -o output/
```

**Command-Line Arguments:**
- `--input, -i` (required): Path to input PDF file
- `--outdir, -o` (optional): Output directory (default: `output/`)
- `--config, -c` (optional): Config file path (default: `config/config.yaml`)
- `--max-slides` (optional): Maximum number of slides (default: 10)
- `--video-format` (optional): Output format - `mp4` or `gif` (default: `mp4`)
- `--verbose, -v` (optional): Enable detailed debug logging

**Usage Examples:**

```bash
# Basic usage - processes PDF and generates slides + video
python src/cli/run_pipeline.py -i document.pdf -o output/

# Generate fewer slides (useful for testing or short summaries)
python src/cli/run_pipeline.py -i chapter.pdf -o output/ --max-slides 3

# Generate GIF instead of MP4 (for smaller file sizes, no audio)
python src/cli/run_pipeline.py -i document.pdf -o output/ --video-format gif

# Enable verbose logging for debugging
python src/cli/run_pipeline.py -i document.pdf -o output/ --verbose
```

#### Output Files

The pipeline generates two files in the specified output directory:

**1. `slides.pptx` - PowerPoint Presentation**
- 6-12 slides based on PDF content and max-slides setting
- **Features:**
  - Dynamic title font sizing (24pt - 32pt based on length)
  - Dynamic bullet font sizing (11pt - 14pt based on content)
  - Proper bullet formatting with "•" symbols and spacing
  - Word-wrapped content to prevent overflow
  - Two-column layout when visuals are present
  - Clean, modern design with blue theme

**2. `video.mp4` or `video.gif` - Animated Video**
- Duration: 30-90 seconds depending on content
- **Features:**
  - TTS narration using generated speaker notes (natural context)
  - Perfect audio-video synchronization (reads actual audio duration)
  - Formatted on-screen text matching slide content
  - Proper bullet symbols and line breaks
  - High quality: 1920x1080 resolution, 30 FPS
  - MP4 with audio, or GIF without audio

### Project Structure

```
infoware_assessment/
├── src/
│   ├── cli/           # Command-line interface
│   ├── extraction/    # PDF extraction services
│   ├── analysis/      # Content analysis
│   ├── summarization/ # Text summarization
│   ├── visual/        # Visual generation
│   ├── slide/         # Slide assembly
│   ├── video/         # Video generation
│   └── utils/         # Utility classes
├── config/            # Configuration files
├── assets/            # Icons, templates, music (optional)
├── output/            # Generated outputs
└── tests/             # Unit and integration tests (optional)

```

### Configuration

Edit `config/config.yaml` to customize the pipeline behavior:

**Key Configuration Sections:**

```yaml
# Content Analysis
analysis:
  max_slides: 10      # Maximum slides to generate
  min_slides: 6       # Minimum slides target

# Summarization
summarization:
  max_title_words: 20      # Max words in slide titles
  max_bullet_words: 15     # Max words per bullet point
  max_speaker_words: 25    # Max words in speaker notes
  bullet_count: 2          # Bullets per slide

# Video Settings
video:
  output_format: "mp4"     # Options: mp4, gif
  fps: 30
  resolution:
    width: 1920
    height: 1080
  min_slide_duration: 5    # Minimum seconds per slide
  max_slide_duration: 12   # Maximum seconds per slide
  tts_provider: "pyttsx3"  # TTS engine
  tts_rate: 150            # Speech rate (words per minute)
```

**See `config/config.yaml` for all available options.**

### Development

This project uses a modular architecture with independent, testable stages.

**Adding New Features:**
1. Create module in appropriate directory (`src/extraction/`, `src/analysis/`, etc.)
2. Implement the required interface
3. Add unit tests
4. Update pipeline orchestrator (`src/cli/orchestrator.py`) if needed

**Installation from Source:**
```bash
# Install in development mode
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

### Technical Stack

**Core Libraries:**
- `pdfplumber` - Advanced PDF text extraction with font properties
- `PyPDF2` - PDF metadata and structure extraction
- `nltk` - Natural language processing and text analysis
- `python-pptx` - PowerPoint presentation generation
- `pyttsx3` - Offline Text-to-Speech engine
- `pillow` - Image processing and diagram generation

**Video Processing:**
- `imageio` - Video frame handling and writing
- `imageio-ffmpeg` - Bundled ffmpeg for audio/video merging

**Configuration & Utilities:**
- `pyyaml` - Configuration file parsing
- `click` - CLI framework (optional, for advanced usage)

### Testing

**End-to-End Test:**
```bash
# Test with a sample PDF
python src/cli/run_pipeline.py -i Machine_Learning_Concept.pdf -o output/ --max-slides 3

# Check outputs
# - output/slides.pptx - Open in PowerPoint
# - output/video.mp4 - Play in any media player
```

**Expected Output:**
- Success message with paths to generated files
- Processing time (~1-2 minutes for typical PDF)
- Detailed logs if `--verbose` flag used

### Advanced Features & Improvements

**Content Extraction:**
- **Font-based heading detection** - No hardcoded keywords, works with any PDF structure
- **Word spacing preservation** - Maintains proper spacing between words
- **Mixed-font line handling** - Splits headings from body text in same line
- **Gibberish filtering** - Removes meaningless short text fragments

**Slide Generation:**
- **Dynamic font sizing** - Titles: 24-32pt, Bullets: 11-14pt based on content length
- **Proper bullet formatting** - Unicode bullets (•) with correct spacing
- **Adaptive layouts** - Two-column with visuals, full-width without
- **Word wrapping** - Automatic wrapping to prevent text overflow
- **Content validation** - Filters out short/meaningless bullets

**Video Generation:**
- **Speaker notes integration** - Uses generated notes for contextual narration
- **Perfect audio-video sync** - Reads actual audio duration for each slide
- **Formatted on-screen text** - Bullets, line breaks, proper spacing
- **Fallback captions** - Shows text when audio unavailable


### License

This is a POC project

### Author

Swayam Shah

---

## How It Works

### Data Transformation Pipeline

**1. PDF Extraction** (`src/extraction/`)
- Reads PDF with pdfplumber to extract text with font properties
- Analyzes font sizes to detect headings (larger = heading)
- Groups text into paragraphs and sections
- Returns structured JSON with titles and content

**2. Content Analysis** (`src/analysis/`)
- Extracts key phrases using NLTK
- Scores sections by length, keywords, position
- Selects top N important sections
- Preserves original document order

**3. Summarization** (`src/summarization/`)
- Creates concise titles (truncates if needed)
- Generates 2-3 bullet points using sentence scoring
- Creates speaker notes (first sentence)
- Returns slide-ready content

**4. Visual Generation** (`src/visual/`)
- Extracts keywords from slide content
- Generates simple diagrams with keywords
- Returns path to generated image

**5. Slide Assembly** (`src/slide/`)
- Creates PowerPoint
- Adds title with dynamic sizing
- Adds bullets with formatting
- Inserts visuals (two-column layout)
- Saves as .pptx file

**6. Video Generation** (`src/video/`)
- Extracts content from PPTX
- Generates TTS audio for each slide
- Creates video frames with formatted text
- Merges audio with video (perfect sync)
- Outputs MP4 or GIF file

### Data Flow

```
PDF File
  ↓
Structured Content (JSON) - Sections, paragraphs, headings
  ↓
Ranked Content (JSON) - Importance-scored sections
  ↓
Slide Data (JSON) - Titles, bullets, speaker notes
  ↓
Enriched Slides (JSON) - With visual elements
  ↓
PowerPoint (.pptx) - Formatted presentation
  ↓
Video (.mp4) - With TTS narration
```