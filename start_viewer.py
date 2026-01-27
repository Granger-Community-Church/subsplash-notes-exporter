#!/usr/bin/env python3
"""
Start a local web server to view your notes
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

def start_server():
    # Change to project directory
    os.chdir(Path(__file__).parent)

    # Create custom handler that sets proper MIME types
    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.md': 'text/markdown',
    })

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/viewer/"
        print("=" * 60)
        print("Subsplash Notes Viewer")
        print("=" * 60)
        print(f"\nServer running at: {url}")
        print("\nPress Ctrl+C to stop the server")
        print()

        # Open browser
        print("Opening browser...")
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    start_server()
