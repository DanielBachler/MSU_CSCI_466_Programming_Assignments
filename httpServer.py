from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import socketserver

PORT = 8081

# The base form for server and request handler taken from online examples
# Found at: (TODO insert)

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
        # Gets the length of the header as an integer
        content_length = int(self.headers['Content-Length'])
        # Sets body equal to the value of the content in the packet
        body = self.rfile.read(content_length)
        # Needed, otherwise invalid request
        self.send_response(200)
        self.end_headers()
        # Get response from Bytes.IO lib
        response = BytesIO()
        # Print out that this is a POST request 
        response.write(b'This is POST request. ')
        # Writes out what was recieved
        response.write(b'Received: ')
        response.write(body)
        # ?
        self.wfile.write(response.getvalue())

# Init server on ip for localc computer on TCP port open to firewall
httpd = HTTPServer(('127.0.0.1', 8081), SimpleHTTPRequestHandler)
# Server do server things forever
httpd.serve_forever()
