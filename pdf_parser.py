import fitz
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class TextBlock:
    text: str
    font_size: float
    font_name: str
    bbox: Tuple[float, float, float, float]
    page_num: int
    y_position: float

class PDFParser:
    def __init__(self, max_pages: int = 50):
        self.max_pages = max_pages
    
    def extract_text_blocks(self, pdf_path: str) -> List[TextBlock]:
        blocks = []
        
        with fitz.open(pdf_path) as doc:
            page_count = min(len(doc), self.max_pages)
            
            for page_num in range(page_count):
                page = doc[page_num]
                text_dict = page.get_text("dict")
                
                for block in text_dict["blocks"]:
                    if "lines" not in block:
                        continue
                    
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue
                            
                            blocks.append(TextBlock(
                                text=text,
                                font_size=span["size"],
                                font_name=span["font"],
                                bbox=span["bbox"],
                                page_num=page_num + 1,
                                y_position=span["bbox"][1]
                            ))
        
        return blocks