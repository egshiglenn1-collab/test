from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import time

class StressTestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response_data = b"OK"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(response_data)))
        self.end_headers()
        try:
            self.wfile.write(response_data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        _ = self.rfile.read(content_length)
        
        response_data = b"OK"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(response_data)))
        self.end_headers()
        self.wfile.write(response_data)

    # Custom log method to show requests in real-time
    def log_message(self, format, *args):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        print(f"[{timestamp}] {client_ip} - {format % args}")

def run(port=8000):
    server_address = ('0.0.0.0', port)
    httpd = ThreadingHTTPServer(server_address, StressTestHandler)
    print(f"[*] Stress Test Server with Logging running on port {port}...")
    print(f"[*] Ready for traffic. Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server...")
        httpd.server_close()

if __name__ == '__main__':
    run()