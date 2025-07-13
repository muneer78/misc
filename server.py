#!/usr/bin/env python3
"""
Local development server for static site generator
Usage: python server.py [--port PORT] [--directory DIR] [--watch]

# Basic usage
python server.py

# With auto-reload (watches for changes)
python server.py --watch

# Custom port and auto-open browser
python server.py --port 3000 --open --watch

# Serve different directory
python server.py --directory dist --watch

# For auto-reload during development
python server.py --watch --open

"""

import http.server
import socketserver
import os
import sys
import argparse
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class ReloadHandler(FileSystemEventHandler):
    """File system event handler for auto-reloading"""
    
    def __init__(self, generator_script="ssg.py"):
        self.generator_script = generator_script
        self.last_reload = 0
        self.reload_delay = 1.0  # Minimum seconds between reloads
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only reload for relevant file changes
        relevant_extensions = {'.md', '.html', '.css', '.scss', '.js', '.py'}
        file_path = Path(event.src_path)
        
        if file_path.suffix.lower() in relevant_extensions:
            current_time = time.time()
            if current_time - self.last_reload > self.reload_delay:
                self.last_reload = current_time
                print(f"\n📝 File changed: {file_path.name}")
                self.regenerate_site()
    
    def regenerate_site(self):
        """Regenerate the static site"""
        try:
            print("🔄 Regenerating site...")
            result = subprocess.run([sys.executable, self.generator_script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Site regenerated successfully!")
                if result.stdout:
                    print(result.stdout)
            else:
                print("❌ Error regenerating site:")
                print(result.stderr)
        except subprocess.TimeoutExpired:
            print("⏰ Site generation timed out")
        except Exception as e:
            print(f"❌ Error running generator: {e}")

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with better error handling and logging"""
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def guess_type(self, path):
        """Override to handle additional file types"""
        mimetype = super().guess_type(path)
        
        # Handle additional file types
        if path.endswith('.xml'):
            return 'application/xml'
        elif path.endswith('.rss'):
            return 'application/rss+xml'
        
        return mimetype
    
    def log_message(self, format, *args):
        """Custom logging with timestamps and colors"""
        timestamp = time.strftime('%H:%M:%S')
        message = format % args
        
        # Add colors for different HTTP status codes
        if '200' in message:
            status_color = '\033[92m'  # Green
        elif '404' in message:
            status_color = '\033[93m'  # Yellow
        elif '500' in message:
            status_color = '\033[91m'  # Red
        else:
            status_color = '\033[94m'  # Blue
        
        reset_color = '\033[0m'
        print(f"[{timestamp}] {status_color}{message}{reset_color}")

def find_free_port(start_port=8000, max_attempts=50):
    """Find a free port starting from start_port"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    raise OSError(f"Could not find a free port in range {start_port}-{start_port + max_attempts}")

def start_file_watcher(watch_dirs, generator_script):
    """Start file system watcher for auto-reload"""
    event_handler = ReloadHandler(generator_script)
    observer = Observer()
    
    for watch_dir in watch_dirs:
        if Path(watch_dir).exists():
            observer.schedule(event_handler, watch_dir, recursive=True)
            print(f"👀 Watching {watch_dir} for changes...")
    
    observer.start()
    return observer

def main():
    parser = argparse.ArgumentParser(description='Local development server for static site')
    parser.add_argument('--port', '-p', type=int, default=8000, 
                       help='Port to serve on (default: 8000)')
    parser.add_argument('--directory', '-d', default='site', 
                       help='Directory to serve (default: site)')
    parser.add_argument('--watch', '-w', action='store_true',
                       help='Watch for file changes and auto-regenerate')
    parser.add_argument('--generator', '-g', default='ssg.py',
                       help='Generator script to run on changes (default: ssg.py)')
    parser.add_argument('--open', '-o', action='store_true',
                       help='Open browser automatically')
    
    args = parser.parse_args()
    
    # Check if site directory exists
    site_dir = Path(args.directory)
    if not site_dir.exists():
        print(f"❌ Directory '{args.directory}' does not exist.")
        print("💡 Run the generator first: python ssg.py")
        sys.exit(1)
    
    # Find a free port if the specified one is taken
    try:
        port = args.port
        # Test if port is available
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
    except OSError:
        port = find_free_port(args.port)
        print(f"⚠️  Port {args.port} is busy, using port {port} instead")
    
    # Change to the site directory
    os.chdir(site_dir)
    
    # Start file watcher if requested
    observer = None
    if args.watch:
        try:
            # Watch content, templates, static, and assets directories
            watch_dirs = ['../content', '../templates', '../static', '../assets']
            observer = start_file_watcher(watch_dirs, f'../{args.generator}')
        except ImportError:
            print("❌ Watchdog not installed. Install with: pip install watchdog")
            print("🔄 Serving without auto-reload...")
        except Exception as e:
            print(f"⚠️  Could not start file watcher: {e}")
            print("🔄 Serving without auto-reload...")
    
    # Create and start the server
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            server_url = f"http://localhost:{port}"
            
            print("\n" + "="*60)
            print(f"🚀 Static Site Development Server")
            print("="*60)
            print(f"📂 Serving directory: {site_dir.absolute()}")
            print(f"🌐 Server URL: {server_url}")
            print(f"📱 Network URL: http://{get_local_ip()}:{port}")
            if args.watch:
                print(f"👀 Auto-reload: {'Enabled' if observer else 'Failed'}")
            print("="*60)
            print("💡 Press Ctrl+C to stop the server")
            print()
            
            # Open browser if requested
            if args.open:
                import webbrowser
                webbrowser.open(server_url)
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        if observer:
            observer.stop()
            observer.join()
            print("👋 File watcher stopped")

def get_local_ip():
    """Get the local IP address for network access"""
    import socket
    try:
        # Connect to a remote address to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    main()
