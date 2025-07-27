import json
from pathlib import Path
from typing import Dict, List
from .pdf_parser import PDFParser
from .heading_detector import HeadingDetector
from .title_extractor import TitleExtractor

class DocumentProcessor:
    def __init__(self):
        self.parser = PDFParser()
        self.heading_detector = HeadingDetector()
        self.title_extractor = TitleExtractor()
    
    def process_pdf(self, pdf_path: str) -> Dict:
        blocks = self.parser.extract_text_blocks(pdf_path)
        
        title = self.title_extractor.extract_title(blocks)
        headings = self.heading_detector.detect_headings(blocks)
        
        outline = []
        for heading in headings:
            outline.append({
                "level": heading["level"],
                "text": heading["text"],
                "page": heading["page"]
            })
        
        return {
            "title": title or "Untitled Document",
            "outline": outline
        }
    
    def process_directory(self, input_dir: str, output_dir: str) -> None:
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        output_path.mkdir(exist_ok=True)
        
        pdf_files = list(input_path.glob("*.pdf"))
        
        for pdf_file in pdf_files:
            try:
                result = self.process_pdf(str(pdf_file))
                
                output_file = output_path / f"{pdf_file.stem}.json"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f"Processed: {pdf_file.name} -> {output_file.name}")
                
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {str(e)}")
                continue