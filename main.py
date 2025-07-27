#!/usr/bin/env python3

import time
from src.document_processor import DocumentProcessor

def main():
    start_time = time.time()
    
    processor = DocumentProcessor()
    processor.process_directory("/app/input", "/app/output")
    
    elapsed = time.time() - start_time
    print(f"Processing completed in {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()