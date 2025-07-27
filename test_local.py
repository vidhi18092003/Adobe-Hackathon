#!/usr/bin/env python3

import time
from pathlib import Path
from src.document_processor import DocumentProcessor

def main():
    start_time = time.time()
    
    # Use local directories for testing
    input_dir = Path(__file__).parent / "input"
    output_dir = Path(__file__).parent / "output"
    
    processor = DocumentProcessor()
    processor.process_directory(str(input_dir), str(output_dir))
    
    elapsed = time.time() - start_time
    print(f"Processing completed in {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()