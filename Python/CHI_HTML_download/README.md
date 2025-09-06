# CHI Paper Download Scripts

## Automatic Batch Download (Original Scripts)
Both scripts need to be executed sequentially:
- **ACM_Lister.py** processes all defined .bib files from the data folder (Data\Bibliography-Files) into CSVs, adding keywords and sessions. The CSVs are saved in the same folder.
- **ACM_downloaderV2.py** reads these CSVs from the same folder and downloads the HTML from the link in the second column. The download creates year folders where the script is located (here), in which the HTMLs will be saved.

## Manual Single Paper Download (New Script)
If you're experiencing 403 errors with the automatic downloader, use the new manual downloader:

### manual_downloader.py
Downloads individual papers from ACM Digital Library with enhanced anti-blocking measures.

**Features:**
- User agent rotation to avoid detection
- Exponential backoff retry logic for 403/429 errors
- Random delays between requests
- Downloads complete HTML with all resources (images, CSS, JS)
- Command-line interface with flexible options

**Usage:**

1. **Command line with URL:**
   ```bash
   python manual_downloader.py "https://dl.acm.org/doi/fullHtml/10.1145/3544548.3580646"
   ```

2. **Interactive mode (prompts for URL):**
   ```bash
   python manual_downloader.py
   ```

3. **With custom options:**
   ```bash
   python manual_downloader.py "https://dl.acm.org/doi/fullHtml/10.1145/3544548.3580646" \
     --output "my_papers" \
     --filename "important_paper" \
     --delay-min 2.0 \
     --delay-max 5.0
   ```

**Options:**
- `-o, --output`: Output directory (default: manual_downloads)
- `-f, --filename`: Custom filename without extension
- `--delay-min`: Minimum delay between requests in seconds (default: 1.0)
- `--delay-max`: Maximum delay between requests in seconds (default: 3.0)

**Example programmatic usage:**
See `example_usage.py` for how to use the ManualDownloader class in your own scripts.

**Requirements:**
- requests
- beautifulsoup4
