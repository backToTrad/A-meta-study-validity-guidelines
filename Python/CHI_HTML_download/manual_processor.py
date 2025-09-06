#!/usr/bin/env python3
"""
Manual HTML Processor for CHI Papers
Processes manually downloaded HTML files to match the format of ACM_downloaderV2.py output.
Handles resource extraction, localization, and BeautifulSoup formatting.
"""

import argparse
import os
import re
import sys
import time
import random
from urllib.parse import urljoin, urlparse
from typing import Optional, Dict, List

import requests
from bs4 import BeautifulSoup


class ManualProcessor:
    def __init__(self, delay_range: tuple = (1, 3)):
        """
        Initialize the manual processor.
        
        Args:
            delay_range: Range of seconds to wait between resource downloads (min, max)
        """
        self.delay_range = delay_range
        self.session = requests.Session()
        
        # User agents for resource downloading
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        ]
        
        # Set headers
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": random.choice(self.user_agents)
        })

    def extract_paper_id(self, html_content: str, filename: str) -> str:
        """
        Extract paper ID from HTML content or filename.
        
        Args:
            html_content: HTML content to search
            filename: Original filename
            
        Returns:
            Paper ID string
        """
        # Try to extract from URL in HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for canonical URL or DOI links
        canonical = soup.find('link', {'rel': 'canonical'})
        if canonical and canonical.get('href'):
            match = re.search(r'/([0-9]+)/?$', canonical['href'])
            if match:
                return match.group(1)
        
        # Look for DOI in meta tags
        doi_meta = soup.find('meta', {'name': 'citation_doi'})
        if doi_meta and doi_meta.get('content'):
            match = re.search(r'10\.1145/[0-9]+\.([0-9]+)', doi_meta['content'])
            if match:
                return match.group(1)
        
        # Extract from filename
        match = re.search(r'([0-9]{7,})', filename)
        if match:
            return match.group(1)
        
        # Fallback
        return "unknown"

    def random_delay(self):
        """Add random delay between requests."""
        delay = random.uniform(*self.delay_range)
        print(f"  Waiting {delay:.1f} seconds...")
        time.sleep(delay)

    def download_resource(self, url: str, max_retries: int = 2) -> Optional[bytes]:
        """
        Download a resource with retry logic.
        
        Args:
            url: URL to download
            max_retries: Maximum number of retry attempts
            
        Returns:
            Resource content as bytes if successful, None otherwise
        """
        for attempt in range(max_retries + 1):
            try:
                # Rotate user agent
                self.session.headers.update({"User-Agent": random.choice(self.user_agents)})
                
                response = self.session.get(url, timeout=15)
                if response.status_code == 200:
                    return response.content
                elif response.status_code in [403, 404]:
                    print(f"    ✗ HTTP {response.status_code} for {url}")
                    return None
                else:
                    print(f"    ✗ HTTP {response.status_code} for {url}")
                    
            except requests.exceptions.RequestException as e:
                print(f"    ✗ Request failed: {e}")
                
            if attempt < max_retries:
                time.sleep(2)
        
        return None

    def save_and_rename_resources(self, soup: BeautifulSoup, page_folder: str, base_url: str, tag: str, attr: str) -> int:
        """
        Download resources and update HTML references (replicates savenRename from ACM_downloaderV2).
        
        Args:
            soup: BeautifulSoup object
            page_folder: Folder to save resources
            base_url: Base URL for resolving relative URLs
            tag: HTML tag to process (img, link, script)
            attr: Attribute containing the URL (src, href)
            
        Returns:
            Number of resources processed
        """
        if not os.path.exists(page_folder):
            os.makedirs(page_folder, exist_ok=True)
        
        processed_count = 0
        
        for element in soup.find_all(tag):
            if element.has_attr(attr):
                try:
                    original_url = element[attr]
                    
                    # Skip data URLs, javascript:, and empty URLs
                    if (not original_url or 
                        original_url.startswith(('data:', 'javascript:', '#', 'mailto:'))):
                        continue
                    
                    # Resolve relative URLs
                    if original_url.startswith('//'):
                        file_url = 'https:' + original_url
                    elif original_url.startswith('/'):
                        file_url = urljoin(base_url, original_url)
                    elif not original_url.startswith('http'):
                        file_url = urljoin(base_url, original_url)
                    else:
                        file_url = original_url
                    
                    # Generate filename (replicates ACM_downloaderV2 logic)
                    filename, ext = os.path.splitext(os.path.basename(urlparse(original_url).path))
                    ext = re.sub(r'\?.*', '', ext)  # Remove query parameters
                    filename = re.sub(r'\W+', '', filename) + ext  # Clean special chars
                    
                    # Ensure we have a filename
                    if not filename or filename == ext:
                        filename = f"resource_{hash(original_url) % 10000}{ext}"
                    
                    # Add default extensions if missing
                    if not ext:
                        if tag == 'img':
                            filename += '.jpg'
                        elif tag == 'link' and 'stylesheet' in element.get('rel', []):
                            filename += '.css'
                        elif tag == 'script':
                            filename += '.js'
                    
                    filepath = os.path.join(page_folder, filename)
                    
                    # Update HTML reference (matches ACM_downloaderV2 format)
                    element[attr] = os.path.join(os.path.basename(page_folder), filename)
                    
                    # Download if not already exists
                    if not os.path.isfile(filepath):
                        print(f"    Downloading {tag} resource: {filename}")
                        
                        # Add delay between downloads
                        if processed_count > 0:
                            self.random_delay()
                        
                        resource_content = self.download_resource(file_url)
                        if resource_content:
                            with open(filepath, 'wb') as f:
                                f.write(resource_content)
                            print(f"    ✓ Saved: {filename}")
                        else:
                            print(f"    ✗ Failed to download: {filename}")
                    else:
                        print(f"    ✓ Already exists: {filename}")
                    
                    processed_count += 1
                    
                except Exception as e:
                    print(f"    ✗ Error processing {tag} resource {original_url}: {e}")
        
        return processed_count

    def process_html_file(self, html_file_path: str, output_dir: str = None, paper_id: str = None) -> bool:
        """
        Process an HTML file to match ACM_downloaderV2 output format.
        
        Args:
            html_file_path: Path to the HTML file to process
            output_dir: Output directory (defaults to same directory as input)
            paper_id: Paper ID (extracted automatically if not provided)
            
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
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")
            print("✓ HTML parsed with BeautifulSoup")
            
            # Extract paper ID
            if not paper_id:
                paper_id = self.extract_paper_id(html_content, os.path.basename(html_file_path))
            print(f"✓ Paper ID: {paper_id}")
            
            # Set up output paths
            if output_dir is None:
                output_dir = os.path.dirname(html_file_path)
            
            output_html_path = os.path.join(output_dir, f"{paper_id}.html")
            page_folder = os.path.join(output_dir, f"{paper_id}_files")
            
            print(f"✓ Output HTML: {output_html_path}")
            print(f"✓ Resources folder: {page_folder}")
            
            # Determine base URL for resource resolution
            base_url = "https://dl.acm.org"
            
            # Process resources (replicates ACM_downloaderV2 logic)
            print("\nProcessing resources...")
            tags_attrs = {'img': 'src', 'link': 'href', 'script': 'src'}
            total_resources = 0
            
            for tag, attr in tags_attrs.items():
                print(f"\n  Processing {tag} elements...")
                count = self.save_and_rename_resources(soup, page_folder, base_url, tag, attr)
                total_resources += count
                print(f"  ✓ Processed {count} {tag} elements")
            
            print(f"\n✓ Total resources processed: {total_resources}")
            
            # Save the modified HTML with BeautifulSoup prettify (matches ACM_downloaderV2)
            print("\nSaving processed HTML...")
            with open(output_html_path, 'wb') as file:
                file.write(soup.prettify('utf-8'))
            
            print(f"✓ Successfully saved: {output_html_path}")
            print(f"✓ File formatted with BeautifulSoup prettify (matches existing files)")
            
            return True
            
        except Exception as e:
            print(f"✗ Error processing file: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Process manually downloaded HTML files to match ACM_downloaderV2 format")
    parser.add_argument("html_file", help="Path to the HTML file to process")
    parser.add_argument("-o", "--output", help="Output directory (defaults to same directory as input)")
    parser.add_argument("-i", "--id", help="Paper ID (extracted automatically if not provided)")
    parser.add_argument("--delay-min", type=float, default=1.0, help="Minimum delay between resource downloads (seconds)")
    parser.add_argument("--delay-max", type=float, default=3.0, help="Maximum delay between resource downloads (seconds)")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)
    
    # Create processor
    processor = ManualProcessor(delay_range=(args.delay_min, args.delay_max))
    
    # Process the file
    success = processor.process_html_file(args.html_file, args.output, args.id)
    
    if success:
        print(f"\n🎉 Processing completed successfully!")
        print(f"The processed file now matches the format of your existing CHI papers.")
        print(f"All resources have been downloaded and localized.")
    else:
        print(f"\n❌ Processing failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
