#!/bin/bash

# Build script for PDF Structure Extractor
echo "Building PDF Structure Extractor..."

# Build Docker image
docker build -t pdf-extractor .

echo "Build complete!"
echo ""
echo "Usage:"
echo "  docker run -v /path/to/input:/app/input -v /path/to/output:/app/output pdf-extractor"
echo ""
echo "For local testing:"
echo "  python test_local.py"