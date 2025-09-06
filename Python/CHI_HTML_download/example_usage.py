#!/usr/bin/env python3
"""
Example usage of the manual downloader script.
"""

from manual_downloader import ManualDownloader

def main():
    # Example URLs (replace with actual paper URLs)
    example_urls = [
        "https://dl.acm.org/doi/fullHtml/10.1145/3544548.3580646",
        "https://dl.acm.org/doi/fullHtml/10.1145/3544548.3581234",
    ]
    
    # Create downloader with custom settings
    downloader = ManualDownloader(
        output_dir="downloaded_papers",
        delay_range=(2, 5)  # Wait 2-5 seconds between requests
    )
    
    # Download each paper
    for i, url in enumerate(example_urls):
        print(f"\n--- Downloading paper {i+1}/{len(example_urls)} ---")
        success = downloader.download_paper(url, custom_filename=f"chi_paper_{i+1}")
        
        if success:
            print(f"✓ Paper {i+1} downloaded successfully")
        else:
            print(f"✗ Failed to download paper {i+1}")

if __name__ == "__main__":
    main()
