# Manual HTML Processor for CHI Papers

This tool solves the 403 error problem with ACM_downloaderV2.py by processing manually downloaded HTML files to match the exact format and structure of the original downloader.

## Problem Solved

The original `ACM_downloaderV2.py` gets 403 errors when accessing ACM's website due to anti-bot measures. This manual processor allows you to:

1. Download HTML files manually via your browser
2. Process them to match the exact format of existing files
3. Download and localize all resources (CSS, JS, images)
4. Apply BeautifulSoup prettification
5. Create the same file structure as the original downloader

## Files

- **`manual_processor.py`** - Main comprehensive processor (replicates full ACM_downloaderV2 functionality)
- **`process_2025_file.py`** - Simple script to process your specific 2025 file
- **`local_parser.py`** - Basic BeautifulSoup formatting only (incomplete solution)
- **`manual_downloader.py`** - Attempts automated download (still gets 403s)

## Quick Start

### Option 1: Process Your Specific File
```bash
cd Python/CHI_HTML_download
python process_2025_file.py
```

### Option 2: Process Any HTML File
```bash
cd Python/CHI_HTML_download
python manual_processor.py /path/to/your/file.html
```

### Option 3: Advanced Usage
```bash
python manual_processor.py /path/to/file.html -o /output/directory -i 3544548
```

## How It Works

The manual processor replicates the exact functionality of `ACM_downloaderV2.py`:

1. **HTML Parsing**: Uses BeautifulSoup to parse the HTML (same as original)
2. **Resource Extraction**: Finds all `img`, `link`, and `script` elements
3. **Resource Download**: Downloads CSS, JS, and image files with anti-blocking measures
4. **URL Localization**: Updates HTML references to point to local files
5. **File Naming**: Uses the same naming convention as the original (`paperid_files/`)
6. **HTML Formatting**: Applies `soup.prettify('utf-8')` (same as original)

## Workflow

1. **Manual Download**: Save the ACM paper HTML via your browser
2. **Run Processor**: Use the manual processor to download resources and format
3. **Result**: Get files that match your existing 2023 format exactly

## Output Structure

The processor creates the same structure as ACM_downloaderV2.py:
```
Data/HTML_Files/2025/
├── 3544548.html                 # Processed HTML file
└── 3544548_files/              # Resources folder
    ├── bootstrap.min.css
    ├── acm-main.js
    ├── figure1.jpg
    └── ...
```

## Command Line Options

```bash
python manual_processor.py [OPTIONS] HTML_FILE

Arguments:
  HTML_FILE                    Path to the HTML file to process

Options:
  -o, --output DIR            Output directory (defaults to same as input)
  -i, --id ID                 Paper ID (auto-extracted if not provided)
  --delay-min SECONDS         Min delay between downloads (default: 1.0)
  --delay-max SECONDS         Max delay between downloads (default: 3.0)
```

## Features

- **Complete Resource Handling**: Downloads CSS, JS, images, and other assets
- **Anti-Blocking Measures**: Rotating user agents, delays, retry logic
- **Automatic Paper ID Extraction**: From HTML content or filename
- **Exact Format Matching**: Output matches existing 2023 files perfectly
- **Error Handling**: Graceful handling of failed resource downloads
- **Progress Reporting**: Detailed output showing what's being processed

## Comparison with Other Scripts

| Script | HTML Formatting | Resource Download | URL Localization | Complete Solution |
|--------|----------------|-------------------|------------------|-------------------|
| `local_parser.py` | ✓ | ✗ | ✗ | ✗ |
| `manual_downloader.py` | ✓ | ✓ | ✓ | ✗ (still gets 403s) |
| **`manual_processor.py`** | ✓ | ✓ | ✓ | ✓ |

## Requirements

```bash
pip install requests beautifulsoup4
```

## Example Usage

```bash
# Process a manually downloaded file
python manual_processor.py ~/Downloads/paper.html

# Process with custom output directory
python manual_processor.py ~/Downloads/paper.html -o ../../Data/HTML_Files/2025

# Process with specific paper ID
python manual_processor.py ~/Downloads/paper.html -i 3544548

# Process with custom delays (slower, more polite)
python manual_processor.py ~/Downloads/paper.html --delay-min 2 --delay-max 5
```

## Integration with Existing Pipeline

The processed files are fully compatible with your existing pipeline:
- Same HTML structure as 2023 files
- Same resource folder naming (`paperid_files/`)
- Same BeautifulSoup prettification
- Same localized resource references

You can use the processed files directly with your existing analysis tools without any modifications.
