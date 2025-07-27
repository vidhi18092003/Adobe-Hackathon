from typing import List, Dict, Optional
from collections import Counter
import re
from .pdf_parser import TextBlock

class HeadingDetector:
    def __init__(self):
        self.font_size_threshold = 1.2
        self.min_heading_size = 10
        
    def detect_headings(self, blocks: List[TextBlock]) -> List[Dict]:
        if not blocks:
            return []
        
        font_sizes = [block.font_size for block in blocks]
        avg_font_size = sum(font_sizes) / len(font_sizes)
        
        size_counts = Counter(font_sizes)
        body_size = size_counts.most_common(1)[0][0]
        
        headings = []
        
        for block in blocks:
            if self._is_heading(block, body_size, avg_font_size):
                level = self._determine_level(block, font_sizes)
                headings.append({
                    "level": level,
                    "text": self._clean_text(block.text),
                    "page": block.page_num,
                    "font_size": block.font_size,
                    "y_position": block.y_position
                })
        
        return self._merge_multiline_headings(headings)
    
    def _is_heading(self, block: TextBlock, body_size: float, avg_size: float) -> bool:
        if block.font_size < self.min_heading_size:
            return False
        
        if block.font_size > body_size * self.font_size_threshold:
            return True
        
        if self._has_heading_patterns(block.text):
            return True
        
        if len(block.text) < 100 and block.font_size >= avg_size:
            return True
        
        return False
    
    def _has_heading_patterns(self, text: str) -> bool:
        patterns = [
            r'^\d+\.?\s+[A-Z]',
            r'^[A-Z][A-Z\s]{2,}$',
            r'^\d+\.\d+\.?\s+',
            r'^Chapter\s+\d+',
            r'^Section\s+\d+',
            r'^Part\s+[IVX]+',
        ]
        
        for pattern in patterns:
            if re.match(pattern, text.strip()):
                return True
        return False
    
    def _determine_level(self, block: TextBlock, all_sizes: List[float]) -> str:
        unique_sizes = sorted(set(all_sizes), reverse=True)
        
        if block.font_size in unique_sizes[:3]:
            size_rank = unique_sizes.index(block.font_size)
            return f"H{size_rank + 1}"
        
        return "H3"
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'^[\d\.\s]+', '', text)
        return text.strip()
    
    def _merge_multiline_headings(self, headings: List[Dict]) -> List[Dict]:
        if not headings:
            return []
        
        merged = []
        current = headings[0].copy()
        
        for i in range(1, len(headings)):
            next_heading = headings[i]
            
            if (current["page"] == next_heading["page"] and
                abs(current["y_position"] - next_heading["y_position"]) < 30 and
                current["level"] == next_heading["level"] and
                len(current["text"]) < 150):
                current["text"] += " " + next_heading["text"]
            else:
                merged.append(current)
                current = next_heading.copy()
        
        merged.append(current)
        
        # Filter out very short or code-like headings
        filtered = []
        for heading in merged:
            text = heading["text"].strip()
            if (len(text) > 3 and 
                not text.startswith(('•', '-', '*')) and
                not text.endswith((';', '{', '}', '(', ')'))):
                filtered.append(heading)
        
        return filtered