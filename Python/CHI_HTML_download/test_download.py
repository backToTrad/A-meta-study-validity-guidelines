#!/usr/bin/env python3
"""
Quick test script for the manual downloader with the problematic URL.
"""

from manual_downloader import ManualDownloader

def main():
    # The URL you mentioned that gives 403 error
    test_url = "https://dl.acm.org/doi/full/10.1145/3544548.3580646"
    
    print("Testing manual downloader with enhanced anti-blocking measures...")
    print(f"Target URL: {test_url}")
    
    # Create downloader with longer delays to be more conservative
    downloader = ManualDownloader(
        output_dir="test_downloads",
        delay_range=(3, 8)  # Longer delays to avoid detection
    )
    
    # Attempt download
    success = downloader.download_paper(test_url, custom_filename="test_paper_3580646")
    
    if success:
        print("\n🎉 Test download successful!")
        print("Check the 'test_downloads' folder for the downloaded paper.")
    else:
        print("\n❌ Test download failed!")
        print("The URL might still be blocked. You may need to:")
        print("1. Try again later (ACM might have temporary blocks)")
        print("2. Use a VPN to change your IP address")
        print("3. Access the paper from an institutional network")

if __name__ == "__main__":
    main()
