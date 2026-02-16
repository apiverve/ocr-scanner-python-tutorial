# OCR Scanner | APIVerve API Tutorial

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.7+-3776ab)](https://python.org)
[![APIVerve | Image to Text](https://img.shields.io/badge/APIVerve-Image_to_Text-purple)](https://apiverve.com/marketplace/imagetotext?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial)

A Python CLI tool that extracts text from images using OCR (Optical Character Recognition). Works with local files and URLs.

![Screenshot](https://raw.githubusercontent.com/apiverve/ocr-scanner-python-tutorial/main/screenshot.jpg)

---

### Get Your Free API Key

This tutorial requires an APIVerve API key. **[Sign up free](https://dashboard.apiverve.com?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial)** - no credit card required.

---

## Features

- Extract text from local image files
- Extract text from image URLs
- Support for JPG, PNG, and GIF formats
- Interactive mode or command-line arguments
- Clean, formatted output with character count
- Handles errors gracefully

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/apiverve/ocr-scanner-python-tutorial.git
   cd ocr-scanner-python-tutorial
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API key**

   Open `scanner.py` and replace the API key:
   ```python
   API_KEY = 'your-api-key-here'
   ```

4. **Run the scanner**

   Interactive mode:
   ```bash
   python scanner.py
   ```

   Command line mode:
   ```bash
   python scanner.py /path/to/image.jpg
   python scanner.py https://example.com/image.png
   ```

## Usage Examples

### Scan a local file
```bash
$ python scanner.py receipt.jpg

==================================================
  OCR Scanner - Extracted Text
==================================================

  Source: receipt.jpg

--------------------------------------------------
  GROCERY STORE
  123 Main Street

  Milk         $3.99
  Bread        $2.49
  Eggs         $4.99

  Total:      $11.47
--------------------------------------------------

  Characters extracted: 89
==================================================
```

### Scan from URL
```bash
$ python scanner.py https://example.com/document.png
```

### Interactive mode
```bash
$ python scanner.py

==================================================
  OCR Scanner
  Powered by APIVerve
==================================================

Extract text from images (files or URLs)
Type 'quit' to exit

Enter image path or URL: screenshot.png
```

## Project Structure

```
ocr-scanner-python-tutorial/
├── scanner.py          # Main Python script
├── requirements.txt    # Dependencies (requests)
├── screenshot.jpg      # Preview image
├── LICENSE             # MIT license
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## How It Works

1. User provides an image (file path or URL)
2. Script detects input type and validates format
3. For files: uploads image to API via multipart form
4. For URLs: sends URL in JSON body
5. API processes image with OCR
6. Script displays extracted text

### The API Call (File Upload)

```python
with open(file_path, 'rb') as f:
    files = {'image': (filename, f, 'image/jpeg')}
    response = requests.post(
        'https://api.apiverve.com/v1/imagetotext',
        files=files,
        headers={'x-api-key': API_KEY}
    )
```

### The API Call (URL)

```python
response = requests.post(
    'https://api.apiverve.com/v1/imagetotext',
    json={'url': image_url},
    headers={
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }
)
```

## API Reference

**Endpoint:** `POST https://api.apiverve.com/v1/imagetotext`

**Option 1: File Upload**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | file | Yes | Image file (JPG, PNG, GIF, max 5MB) |

**Option 2: URL**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | URL of the image |

**Example Response:**

```json
{
  "status": "ok",
  "error": null,
  "data": {
    "text": "Extracted text from the image appears here..."
  }
}
```

## Use Cases

- **Receipt scanning** - Extract totals and items from receipts
- **Document digitization** - Convert scanned documents to text
- **Screenshot text extraction** - Pull text from screenshots
- **Business card scanning** - Extract contact information
- **Sign/label reading** - Read text from photos of signs
- **Handwritten notes** - Digitize handwritten content

## Customization Ideas

- Add output to file option (`--output results.txt`)
- Add batch processing for multiple images
- Add JSON output format
- Build a web interface with Flask
- Add clipboard support (paste image)
- Integrate with cloud storage (S3, Google Drive)

## Related APIs

Explore more APIs at [APIVerve](https://apiverve.com/marketplace?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial):

- [Image Caption](https://apiverve.com/marketplace/imagecaption?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial) - Generate captions for images
- [QR Code Reader](https://apiverve.com/marketplace/qrcodereader?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial) - Read QR codes from images
- [Face Detector](https://apiverve.com/marketplace/facedetect?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial) - Detect faces in images

## License

MIT - see [LICENSE](LICENSE)

## Links

- [Get API Key](https://dashboard.apiverve.com?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial) - Sign up free
- [APIVerve Marketplace](https://apiverve.com/marketplace?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial) - Browse 300+ APIs
- [Image to Text API](https://apiverve.com/marketplace/imagetotext?utm_source=github&utm_medium=tutorial&utm_campaign=ocr-scanner-python-tutorial) - API details
