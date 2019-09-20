from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import socketserver
import sys

# Takes in the gameboard file and returns a 2D array of it
def makeBoard(fileName):
    print("test")

# Takes the POST request and determines if that hits or not
def handlePost(request):
    x = request[2]
    y = request[6]
    global gameboard
    # C B R S D
    if(gameboard[x][y] == 'C')
    return "test"

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
        result = handlePost(self.path)
        
        self.send_response(200)
        self.end_headers()
        # Create BytesIO object
        response = BytesIO()
        # Print out that this is a POST request 
        response.write(b'This is POST request. ')
        # Writes out what was recieved
        response.write(b'Received: ')
        response.write(body)
        # ?
        self.wfile.write(response.getvalue())

# Init server on ip for localc computer on TCP port open to firewall
httpd = HTTPServer(('192.168.0.197', sys.argv[1]), SimpleHTTPRequestHandler)
gameboard = makeBoard(sys.argv[2])
# Server do server things forever
httpd.serve_forever()