#!/usr/bin/env python3
"""
Process your specific 2025 HTML file with the comprehensive manual processor.
This script will fully replicate the ACM_downloaderV2.py functionality.
"""

import os
import sys
from manual_processor import ManualProcessor

def main():
    # Your HTML file path
    html_file = "../../Data/HTML_Files/2025/3706598.html"
    output_dir = "../../Data/HTML_Files/2025"
    
    print("Processing your 2025 HTML file with comprehensive resource handling...")
    print(f"Input file: {html_file}")
    print(f"Output directory: {output_dir}")
    
    # Check if file exists
    if not os.path.exists(html_file):
        print(f"Error: File not found: {html_file}")
        print("Make sure the file is in the correct location.")
        return False
    
    # Create processor
    processor = ManualProcessor(delay_range=(1, 3))
    
    # Process the file
    success = processor.process_html_file(
        html_file_path=html_file,
        output_dir=output_dir,
        paper_id=None  # Will be auto-extracted
    )
    
    if success:
        print("\n🎉 Your file has been fully processed!")
        print("✓ HTML formatted with BeautifulSoup prettify")
        print("✓ All resources (CSS, JS, images) downloaded and localized")
        print("✓ File structure matches your existing 2023 files")
        print("✓ Ready to use with your existing pipeline")
    else:
        print("\n❌ Processing failed!")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
