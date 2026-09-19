#!/usr/bin/env python3
"""
Text from an image, from the command line.

    python scanner.py receipt.png                     # a local image
    python scanner.py https://example.com/sign.jpg    # an image online

Reads APIVERVE_API_KEY from .env, like the web app.
"""
import sys
from pathlib import Path

from apiverve import ApiError, call_api

TYPES = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif'}
MAX_BYTES = 5 * 1024 * 1024


def from_file(path):
    path = Path(path)
    if not path.is_file():
        raise ApiError(f'File not found: {path}')
    if path.suffix.lower() not in TYPES:
        raise ApiError('Use a JPG, PNG or GIF image.')
    if path.stat().st_size > MAX_BYTES:
        raise ApiError('Images must be 5 MB or smaller.')
    with path.open('rb') as f:
        return call_api('imagetotext', files={'image': (path.name, f, TYPES[path.suffix.lower()])})


def from_url(url):
    return call_api('imagetotext', json={'url': url})


def main():
    source = sys.argv[1] if len(sys.argv) == 2 else input('Image path or URL: ').strip()
    try:
        d = from_url(source) if source.startswith(('http://', 'https://')) else from_file(source)
    except ApiError as err:
        raise SystemExit(f'Error: {err}')
    text = (d.get('text') or '').strip()
    print('\n' + (text or '(No text found in this image)') + '\n')


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
