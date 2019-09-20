from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import socketserver

PORT = 8081

#Handle override
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # When contacted by a client, send Hello World
    def do_GET(self):
        # Needed
        self.send_response(200)
        self.end_headers()
        # Send message
        self.wfile.write(b'Hello, World')

    # Handling POST requests
    def do_POST(self):
        # ?
        content_length = int(self.headers['Content-Length'])
        # ?
        body = self.rfile.read(content_length)
        # Needed
        self.send_response(200)
        self.end_headers()
        # Get response
        response = BytesIO()
        # Label
        response.write(b'This is POST request. ')
        # ?
        response.write(b'Received: ')
        # ?
        response.write(body)
        # ?
        self.wfile.write(response.getvalue())

# Init server on ip for localc computer on TCP port open to firewall
httpd = HTTPServer(('192.168.0.138', 8081), SimpleHTTPRequestHandler)
# Server do server things forever
httpd.serve_forever()