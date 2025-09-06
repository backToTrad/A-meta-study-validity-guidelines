#!/usr/bin/env python3
"""
Local HTML Parser
Processes already-downloaded HTML files with BeautifulSoup formatting to match existing files.
No downloading - just parsing and formatting.
"""

import argparse
import os
import sys
from bs4 import BeautifulSoup


def process_html_file(html_file_path: str) -> bool:
    """
    Process an HTML file with BeautifulSoup formatting (same as ACM_downloaderV2).
    
    Args:
        html_file_path: Path to the HTML file to process
        
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Processing HTML file: {html_file_path}")
    print(f"{'='*60}")
    
    # Check if file exists
    if not os.path.exists(html_file_path):
        print(f"✗ File not found: {html_file_path}")
        return False
    
    try:
        # Read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        print("✓ HTML file loaded successfully")
        
        # Parse with BeautifulSoup (same as ACM_downloaderV2)
        soup = BeautifulSoup(html_content, "html.parser")
        print("✓ HTML parsed with BeautifulSoup")
        
        # Create output path (overwrite the original or create new)
        path, ext = os.path.splitext(html_file_path)
        output_path = path + '_processed' + ext
        
        # Save with BeautifulSoup formatting (same as ACM_downloaderV2)
        with open(output_path, 'wb') as file:
            file.write(soup.prettify('utf-8'))
        
        print(f"✓ Successfully processed and saved: {output_path}")
        print(f"✓ File formatted with BeautifulSoup prettify (matches existing files)")
        return True
        
    except Exception as e:
        print(f"✗ Error processing file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Process local HTML files with BeautifulSoup formatting")
    parser.add_argument("html_file", help="Path to the HTML file to process")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the original file instead of creating _processed version")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)
    
    # Process the file
    success = process_html_file(args.html_file)
    
    if success:
        print(f"\n🎉 Processing completed successfully!")
        if args.overwrite:
            # Move processed file to original location
            path, ext = os.path.splitext(args.html_file)
            processed_path = path + '_processed' + ext
            os.replace(processed_path, args.html_file)
            print(f"✓ Original file overwritten: {args.html_file}")
        else:
            print(f"✓ Processed file saved with '_processed' suffix")
    else:
        print(f"\n❌ Processing failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
