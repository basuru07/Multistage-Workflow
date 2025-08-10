# app.py - Simple HTTP Server using built-in modules
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import urlparse

class SimpleHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Route handling
        if path == '/':
            response = {
                'message': 'Hello World!',
                'version': '1.0.0',
                'environment': 'development'
            }
        elif path == '/health':
            response = {'status': 'OK'}
        elif path == '/api/status':
            response = {
                'environment': 'development',
                'version': '1.0.0',
                'python_version': sys.version,
                'server': 'Python HTTP Server'
            }
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Not Found'}
        
        # Send JSON response
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    # Suppress log messages (optional)
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

def run_server():
    port = int(os.getenv('PORT', 8000))
    server_address = ('', port)
    
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'🚀 Server running on http://localhost:{port}')
    print(f'📊 Health check: http://localhost:{port}/health')
    print(f'📈 Status: http://localhost:{port}/api/status')
    print('Press Ctrl+C to stop the server')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n🛑 Server stopped')
        httpd.server_close()

if __name__ == '__main__':
    run_server()