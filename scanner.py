#!/usr/bin/env python3
"""
OCR Scanner - Tutorial Example

A simple CLI tool that extracts text from images using the APIVerve API.
https://apiverve.com/marketplace/imagetotext
"""

import requests
import sys
import os
from pathlib import Path

# ============================================
# CONFIGURATION - Add your API key here
# Get a free key at: https://dashboard.apiverve.com
# ============================================
API_KEY = 'your-api-key-here'
API_URL = 'https://api.apiverve.com/v1/imagetotext'


def extract_text_from_file(file_path: str) -> dict:
    """
    Extract text from a local image file.

    Args:
        file_path: Path to the image file

    Returns:
        Dictionary with extracted text or error
    """
    if API_KEY == 'your-api-key-here':
        return {'error': 'API key not configured. Add your key to scanner.py'}

    path = Path(file_path)
    if not path.exists():
        return {'error': f'File not found: {file_path}'}

    # Check file extension
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    if path.suffix.lower() not in valid_extensions:
        return {'error': f'Unsupported format. Use: {", ".join(valid_extensions)}'}

    # Check file size (max 5MB)
    file_size = path.stat().st_size
    if file_size > 5 * 1024 * 1024:
        return {'error': 'File too large. Maximum size is 5MB.'}

    try:
        with open(file_path, 'rb') as f:
            files = {'image': (path.name, f, f'image/{path.suffix[1:]}')}
            response = requests.post(
                API_URL,
                files=files,
                headers={'x-api-key': API_KEY}
            )

        data = response.json()

        if data.get('status') == 'ok':
            return {
                'success': True,
                'text': data['data'].get('text', ''),
                'source': file_path
            }
        else:
            return {'error': data.get('error', 'OCR extraction failed')}

    except requests.RequestException as e:
        return {'error': f'API request failed: {str(e)}'}
    except (KeyError, ValueError) as e:
        return {'error': f'Invalid response: {str(e)}'}


def extract_text_from_url(image_url: str) -> dict:
    """
    Extract text from an image URL.

    Args:
        image_url: URL of the image

    Returns:
        Dictionary with extracted text or error
    """
    if API_KEY == 'your-api-key-here':
        return {'error': 'API key not configured. Add your key to scanner.py'}

    try:
        response = requests.post(
            API_URL,
            json={'url': image_url},
            headers={
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            }
        )

        data = response.json()

        if data.get('status') == 'ok':
            return {
                'success': True,
                'text': data['data'].get('text', ''),
                'source': image_url
            }
        else:
            return {'error': data.get('error', 'OCR extraction failed')}

    except requests.RequestException as e:
        return {'error': f'API request failed: {str(e)}'}
    except (KeyError, ValueError) as e:
        return {'error': f'Invalid response: {str(e)}'}


def print_result(result: dict):
    """Print extraction result in a formatted way."""
    if 'error' in result:
        print(f"\n{'='*50}")
        print(f"  Error: {result['error']}")
        print(f"{'='*50}\n")
    else:
        print(f"\n{'='*50}")
        print("  OCR Scanner - Extracted Text")
        print(f"{'='*50}")
        print(f"\n  Source: {result['source']}\n")
        print("-" * 50)

        text = result['text'].strip()
        if text:
            # Indent each line
            for line in text.split('\n'):
                print(f"  {line}")
        else:
            print("  (No text found in image)")

        print("-" * 50)
        print(f"\n  Characters extracted: {len(text)}")
        print(f"{'='*50}\n")


def interactive_mode():
    """Run the scanner in interactive mode."""
    print("\n" + "="*50)
    print("  OCR Scanner")
    print("  Powered by APIVerve")
    print("="*50)
    print("\nExtract text from images (files or URLs)")
    print("Type 'quit' to exit\n")

    while True:
        try:
            source = input("Enter image path or URL: ").strip()
            if source.lower() == 'quit':
                break

            if not source:
                print("Please enter a file path or URL.\n")
                continue

            # Determine if it's a URL or file path
            if source.startswith('http://') or source.startswith('https://'):
                result = extract_text_from_url(source)
            else:
                result = extract_text_from_file(source)

            print_result(result)

        except KeyboardInterrupt:
            print("\n")
            break

    print("Goodbye!\n")


def main():
    """Main entry point."""
    if len(sys.argv) == 2:
        # Command line mode: python scanner.py <file_or_url>
        source = sys.argv[1]

        if source.startswith('http://') or source.startswith('https://'):
            result = extract_text_from_url(source)
        else:
            result = extract_text_from_file(source)

        print_result(result)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()
