#!/usr/bin/env python3
"""
Simple local development server for static site generator
No external dependencies required - uses only Python standard library
Usage: python simple_server.py [--port PORT] [--directory DIR]

# Basic usage
python simple_server.py

# Custom port and auto-open browser
python simple_server.py --port 3000 --open

# Serve different directory
python simple_server.py --directory dist

"""

import http.server
import socketserver
import os
import sys
import argparse
import webbrowser
import socket
from pathlib import Path
import time


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with better error handling and logging"""

    def end_headers(self):
        # Add CORS headers for local development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def guess_type(self, path):
        """Override to handle additional file types"""
        mimetype = super().guess_type(path)

        # Handle additional file types
        if path.endswith(".xml"):
            return "application/xml"
        elif path.endswith(".rss"):
            return "application/rss+xml"

        return mimetype

    def log_message(self, format, *args):
        """Custom logging with timestamps"""
        timestamp = time.strftime("%H:%M:%S")
        message = format % args
        print(f"[{timestamp}] {message}")


def find_free_port(start_port=8000, max_attempts=50):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            continue

    raise OSError(
        f"Could not find a free port in range {start_port}-{start_port + max_attempts}"
    )


def get_local_ip():
    """Get the local IP address for network access"""
    try:
        # Connect to a remote address to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"


def main():
    parser = argparse.ArgumentParser(
        description="Simple local development server for static site"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=8000, help="Port to serve on (default: 8000)"
    )
    parser.add_argument(
        "--directory", "-d", default="site", help="Directory to serve (default: site)"
    )
    parser.add_argument(
        "--open", "-o", action="store_true", help="Open browser automatically"
    )

    args = parser.parse_args()

    # Check if site directory exists
    site_dir = Path(args.directory)
    if not site_dir.exists():
        print(f"❌ Directory '{args.directory}' does not exist.")
        print("💡 Run the generator first: python generator.py")
        sys.exit(1)

    # Find a free port if the specified one is taken
    try:
        port = args.port
        # Test if port is available
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
    except OSError:
        port = find_free_port(args.port)
        print(f"⚠️  Port {args.port} is busy, using port {port} instead")

    # Change to the site directory
    original_dir = os.getcwd()
    os.chdir(site_dir)

    try:
        # Create and start the server
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            server_url = f"http://localhost:{port}"
            local_ip = get_local_ip()

            print("\n" + "=" * 60)
            print("🚀 Simple Static Site Server")
            print("=" * 60)
            print(f"📂 Serving: {site_dir.absolute()}")
            print(f"🌐 Local:   {server_url}")
            print(f"📱 Network: http://{local_ip}:{port}")
            print("=" * 60)
            print("💡 Press Ctrl+C to stop the server")
            print("🔄 To regenerate site, run: python ssg.py")
            print()

            # Open browser if requested
            if args.open:
                print(f"🌐 Opening {server_url} in browser...")
                webbrowser.open(server_url)

            # Start serving
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        # Return to original directory
        os.chdir(original_dir)


if __name__ == "__main__":
    main()
