#!/usr/bin/env python3
"""
Process your specific HTML file with BeautifulSoup formatting.
"""

from local_parser import process_html_file
import os

def main():
    # Your HTML file path
    html_file = "../../Data/HTML_Files/2025/3544548.html"
    
    print("Processing your downloaded HTML file...")
    print(f"File: {html_file}")
    
    # Check if file exists
    if not os.path.exists(html_file):
        print(f"Error: File not found: {html_file}")
        print("Make sure the file is in the correct location.")
        return
    
    # Process the file
    success = process_html_file(html_file)
    
    if success:
        print("\n🎉 Your file has been processed!")
        print("The processed version is saved as '3544548_processed.html'")
        print("This version now matches the format of your existing files.")
    else:
        print("\n❌ Processing failed!")

if __name__ == "__main__":
    main()
