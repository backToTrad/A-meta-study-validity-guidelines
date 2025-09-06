#!/usr/bin/env python3
"""
Manual CHI Paper Downloader
Downloads individual papers from ACM Digital Library with enhanced anti-blocking measures.
"""

import argparse
import os
import re
import sys
import time
import random
from urllib.parse import urljoin, urlparse
from typing import Optional

import requests
from bs4 import BeautifulSoup


class ManualDownloader:
    def __init__(self, output_dir: str = "manual_downloads", delay_range: tuple = (2, 6)):
        """
        Initialize the manual downloader.
        
        Args:
            output_dir: Directory to save downloaded files
            delay_range: Range of seconds to wait between requests (min, max)
        """
        self.output_dir = output_dir
        self.delay_range = delay_range
        self.session = requests.Session()
        
        # More diverse user agents to avoid detection
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
        ]
        
        # Set initial headers with more realistic browser behavior
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        })

    def normalize_acm_url(self, url: str) -> str:
        """
        Convert different ACM URL formats to the fullHtml version.
        
        Args:
            url: Original ACM URL
            
        Returns:
            Normalized URL for fullHtml access
        """
        # Convert /doi/full/ to /doi/fullHtml/
        if '/doi/full/' in url:
            url = url.replace('/doi/full/', '/doi/fullHtml/')
            print(f"Converted URL to fullHtml format: {url}")
        
        # Convert /doi/abs/ to /doi/fullHtml/
        elif '/doi/abs/' in url:
            url = url.replace('/doi/abs/', '/doi/fullHtml/')
            print(f"Converted URL to fullHtml format: {url}")
        
        # Convert /doi/10.1145/ to /doi/fullHtml/10.1145/
        elif '/doi/10.1145/' in url and '/doi/fullHtml/' not in url:
            url = url.replace('/doi/10.1145/', '/doi/fullHtml/10.1145/')
            print(f"Converted URL to fullHtml format: {url}")
        
        return url

    def get_paper_id_from_url(self, url: str) -> str:
        """Extract paper ID from ACM URL."""
        # Extract the paper ID from URLs like https://dl.acm.org/doi/fullHtml/10.1145/3544548.3580646
        match = re.search(r'/([0-9]+)/?$', url)
        if match:
            return match.group(1)
        
        # Fallback: use last part of path
        parsed = urlparse(url)
        return os.path.basename(parsed.path) or "unknown"

    def random_delay(self):
        """Add random delay between requests."""
        delay = random.uniform(*self.delay_range)
        print(f"Waiting {delay:.1f} seconds...")
        time.sleep(delay)

    def download_with_retry(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """
        Download URL with retry logic and rotating user agents.
        
        Args:
            url: URL to download
            max_retries: Maximum number of retry attempts
            
        Returns:
            Response object if successful, None otherwise
        """
        for attempt in range(max_retries + 1):
            # Rotate user agent for each attempt
            user_agent = random.choice(self.user_agents)
            self.session.headers.update({"User-Agent": user_agent})
            
            print(f"Downloading {url} (attempt {attempt + 1}/{max_retries + 1})")
            print(f"Using User-Agent: {user_agent[:50]}...")
            
            try:
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    print(f"✓ Successfully downloaded {url}")
                    return response
                elif response.status_code == 403:
                    print(f"✗ 403 Forbidden error for {url}")
                    if attempt < max_retries:
                        wait_time = (attempt + 1) * 30  # Exponential backoff
                        print(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                elif response.status_code == 429:
                    print(f"✗ Rate limited (429) for {url}")
                    if attempt < max_retries:
                        wait_time = (attempt + 1) * 60  # Longer wait for rate limiting
                        print(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                else:
                    print(f"✗ HTTP {response.status_code} error for {url}")
                    if attempt < max_retries:
                        time.sleep(10)
                        
            except requests.exceptions.RequestException as e:
                print(f"✗ Request failed for {url}: {e}")
                if attempt < max_retries:
                    time.sleep(10)
            
            # Add delay between attempts
            if attempt < max_retries:
                self.random_delay()
        
        print(f"✗ Failed to download {url} after {max_retries + 1} attempts")
        return None

    def save_resource(self, soup: BeautifulSoup, base_url: str, resource_dir: str, tag: str, attr: str):
        """Download and save resources (images, CSS, JS) referenced in HTML."""
        if not os.path.exists(resource_dir):
            os.makedirs(resource_dir)
        
        for element in soup.find_all(tag):
            if element.has_attr(attr):
                try:
                    resource_url = urljoin(base_url, element[attr])
                    
                    # Skip data URLs and external resources from other domains
                    if resource_url.startswith('data:') or not resource_url.startswith('https://dl.acm.org'):
                        continue
                    
                    # Generate filename
                    filename = os.path.basename(urlparse(resource_url).path)
                    if not filename:
                        filename = f"resource_{hash(resource_url) % 10000}"
                    
                    # Clean filename
                    filename = re.sub(r'[^\w\-_\.]', '_', filename)
                    if not os.path.splitext(filename)[1]:
                        # Add extension based on tag
                        if tag == 'img':
                            filename += '.jpg'
                        elif tag == 'link':
                            filename += '.css'
                        elif tag == 'script':
                            filename += '.js'
                    
                    filepath = os.path.join(resource_dir, filename)
                    
                    # Update HTML reference
                    element[attr] = os.path.join(os.path.basename(resource_dir), filename)
                    
                    # Download if not already exists
                    if not os.path.exists(filepath):
                        print(f"  Downloading resource: {resource_url}")
                        self.random_delay()
                        
                        resource_response = self.download_with_retry(resource_url)
                        if resource_response:
                            with open(filepath, 'wb') as f:
                                f.write(resource_response.content)
                            print(f"  ✓ Saved: {filename}")
                        else:
                            print(f"  ✗ Failed to download: {resource_url}")
                    
                except Exception as e:
                    print(f"  ✗ Error processing resource {element.get(attr, 'unknown')}: {e}")

    def download_paper(self, url: str, custom_filename: Optional[str] = None) -> bool:
        """
        Download a single paper with all its resources.
        
        Args:
            url: Full URL to the paper
            custom_filename: Optional custom filename (without extension)
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"Starting download of: {url}")
        print(f"{'='*60}")
        
        # Normalize URL to fullHtml format
        normalized_url = self.normalize_acm_url(url)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Download main HTML
        response = self.download_with_retry(normalized_url)
        if not response:
            return False
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Generate filename
        if custom_filename:
            filename = custom_filename
        else:
            paper_id = self.get_paper_id_from_url(url)
            filename = f"paper_{paper_id}"
        
        # Clean filename
        filename = re.sub(r'[^\w\-_]', '_', filename)
        
        html_path = os.path.join(self.output_dir, f"{filename}.html")
        resource_dir = os.path.join(self.output_dir, f"{filename}_files")
        
        print(f"\nSaving to: {html_path}")
        print(f"Resources will be saved to: {resource_dir}")
        
        # Download resources
        print("\nDownloading resources...")
        resource_tags = {
            'img': 'src',
            'link': 'href', 
            'script': 'src'
        }
        
        for tag, attr in resource_tags.items():
            self.save_resource(soup, url, resource_dir, tag, attr)
        
        # Save modified HTML
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print(f"\n✓ Successfully saved paper to: {html_path}")
            return True
        except Exception as e:
            print(f"\n✗ Error saving HTML file: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Download individual CHI papers from ACM Digital Library")
    parser.add_argument("url", nargs='?', help="Full URL to the paper")
    parser.add_argument("-o", "--output", default="manual_downloads", help="Output directory (default: manual_downloads)")
    parser.add_argument("-f", "--filename", help="Custom filename (without extension)")
    parser.add_argument("--delay-min", type=float, default=1.0, help="Minimum delay between requests (seconds)")
    parser.add_argument("--delay-max", type=float, default=3.0, help="Maximum delay between requests (seconds)")
    
    args = parser.parse_args()
    
    # Get URL from command line or prompt user
    url = args.url
    if not url:
        url = input("Enter the full URL of the paper to download: ").strip()
    
    if not url:
        print("Error: No URL provided")
        sys.exit(1)
    
    # Validate URL
    if not url.startswith('http'):
        print("Error: Please provide a full URL starting with http:// or https://")
        sys.exit(1)
    
    # Create downloader
    downloader = ManualDownloader(
        output_dir=args.output,
        delay_range=(args.delay_min, args.delay_max)
    )
    
    # Download paper
    success = downloader.download_paper(url, args.filename)
    
    if success:
        print(f"\n🎉 Download completed successfully!")
        print(f"Files saved in: {args.output}")
    else:
        print(f"\n❌ Download failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
