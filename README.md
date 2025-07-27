# Connecting the Dots - PDF Structure Extractor

A fast, offline PDF structure extraction tool that detects titles and headings from PDF documents.

## Features

- Extracts document title from first page
- Detects heading hierarchy (H1, H2, H3) based on font size and patterns
- Processes up to 50 pages per PDF
- Outputs structured JSON format
- Runs completely offline
- Optimized for speed (<10 seconds per PDF)

## Project Structure

```
├── src/
│   ├── pdf_parser.py          # PDF text extraction using PyMuPDF
│   ├── heading_detector.py    # Heading detection logic
│   ├── title_extractor.py     # Title extraction from page 1
│   └── document_processor.py  # Main processing pipeline
├── input/                     # Place PDF files here
├── output/                    # JSON outputs generated here
├── main.py                    # Docker entry point
├── test_local.py             # Local testing script
└── requirements.txt
```

## Usage

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place PDF files in `input/` directory

3. Run locally:
```bash
python test_local.py
```

### Docker

1. Build image:
```bash
docker build -t pdf-extractor .
```

2. Run with mounted volumes:
```bash
docker run -v /path/to/pdfs:/app/input -v /path/to/output:/app/output pdf-extractor
```

## Output Format

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Section 1", "page": 1 },
    { "level": "H2", "text": "Subsection A", "page": 2 },
    { "level": "H3", "text": "Sub-subsection", "page": 3 }
  ]
}
```

## Algorithm

1. **Text Extraction**: Uses PyMuPDF to extract text with font metadata
2. **Title Detection**: Analyzes first page for largest, well-positioned text
3. **Heading Detection**: Combines font size analysis with pattern matching
4. **Level Assignment**: Maps font sizes to H1/H2/H3 hierarchy
5. **Output Generation**: Creates clean JSON structure

## Performance

- Processes typical academic papers in 2-5 seconds
- Memory efficient with streaming text extraction
- No AI models required (under 200MB total)