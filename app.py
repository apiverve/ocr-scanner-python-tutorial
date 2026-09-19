"""
The web app: the page in public/ and the API route it calls, which holds your key.

Run it locally with `python app.py`, then open http://localhost:3000
On Vercel, this file becomes a Python function and public/ is served from the CDN.
"""
import os
import re
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from apiverve import ApiError, api_key, call_api, rate_limited

app = Flask(__name__)
PUBLIC = Path(__file__).with_name('public')


@app.before_request
def guard():
    """Every /api route needs the key, and counts against the visitor's rate limit."""
    if not request.path.startswith('/api/'):
        return None
    api_key()
    ip = request.headers.get('x-forwarded-for', '').split(',')[0].strip() or request.remote_addr or 'local'
    if rate_limited(ip):
        return fail('Too many requests. Wait a minute and try again.', 429)
    return None


@app.errorhandler(ApiError)
def api_error(err):
    return fail(str(err), err.status)


def fail(message, status=400):
    return jsonify(error=message), status

# Vercel caps a function's request body at 4.5 MB, so uploads stop at 4 MB.
MAX_BYTES = 4 * 1024 * 1024
TYPES = {'image/jpeg', 'image/png', 'image/gif'}


@app.post('/api/scan')
def scan():
    """POST /api/scan (multipart, field "image"): the text in an image."""
    image = request.files.get('image')
    if not image or not image.filename:
        return fail('Choose an image with text in it.')
    if image.mimetype not in TYPES:
        return fail('Use a JPG, PNG or GIF image.')
    data = image.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        return fail('Images must be 4 MB or smaller.')
    return jsonify(call_api('imagetotext', files={'image': (image.filename, data, image.mimetype)}))


# The page. On Vercel the CDN serves public/ before a request reaches this app;
# these routes serve it when you run the app locally.
@app.get('/')
def index():
    return send_from_directory(PUBLIC, 'index.html')


@app.get('/<path:name>')
def static_file(name):
    return send_from_directory(PUBLIC, name)


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 3000)), debug=True)
