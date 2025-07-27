from typing import List, Optional
import re
from .pdf_parser import TextBlock

class TitleExtractor:
    def __init__(self):
        self.max_title_length = 200
        self.min_title_length = 5
        
    def extract_title(self, blocks: List[TextBlock]) -> Optional[str]:
        if not blocks:
            return None
        
        page_1_blocks = [b for b in blocks if b.page_num == 1]
        if not page_1_blocks:
            return None
        
        candidates = self._get_title_candidates(page_1_blocks)
        
        if not candidates:
            return None
        
        return self._select_best_title(candidates)
    
    def _get_title_candidates(self, blocks: List[TextBlock]) -> List[str]:
        candidates = []
        
        sorted_blocks = sorted(blocks, key=lambda x: (-x.font_size, x.y_position))
        
        for block in sorted_blocks[:10]:
            text = self._clean_title_text(block.text)
            
            if self._is_valid_title(text):
                candidates.append(text)
        
        return candidates
    
    def _clean_title_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'^[\d\.\s\-]+', '', text)
        text = re.sub(r'[\d\.\s\-]+$', '', text)
        return text.strip()
    
    def _is_valid_title(self, text: str) -> bool:
        if len(text) < self.min_title_length or len(text) > self.max_title_length:
            return False
        
        if re.match(r'^\d+$', text):
            return False
        
        if text.lower() in ['page', 'contents', 'index', 'abstract', 'introduction']:
            return False
        
        if re.match(r'^(chapter|section|part)\s+\d+$', text.lower()):
            return False
        
        return True
    
    def _select_best_title(self, candidates: List[str]) -> str:
        if not candidates:
            return "Untitled Document"
        
        scored_candidates = []
        for candidate in candidates:
            score = self._score_title(candidate)
            scored_candidates.append((score, candidate))
        
        scored_candidates.sort(reverse=True)
        return scored_candidates[0][1]
    
    def _score_title(self, text: str) -> float:
        score = 0.0
        
        if 10 <= len(text) <= 80:
            score += 2.0
        
        if text[0].isupper():
            score += 1.0
        
        if not re.search(r'\d', text):
            score += 1.0
        
        word_count = len(text.split())
        if 2 <= word_count <= 10:
            score += 1.0
        
        if re.search(r'[.!?]$', text):
            score -= 1.0
        
        return score