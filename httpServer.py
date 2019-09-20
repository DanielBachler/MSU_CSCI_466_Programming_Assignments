from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import socketserver
import sys
import numpy as np

# Takes in the gameboard file and returns a 2D array of it
def makeBoard(fileName):
    boardFile = open(fileName, 'r')
    gameboard = np.chararray(shape=[10,10])
    for i in range(0,10):
        line = boardFile.readline()
        for j in range(0,10):
            gameboard[i][j] = line[j]
    return gameboard

# Takes the POST request and determines if that hits or not
def handlePost(request):
    x = request[2]
    y = request[6]
    #global gameboard
    # C B R S D
    #if(gameboard[x][y] == 'C')
    return "miss"

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
        # Get the value of result from handlePost, and send the correct HTTP message
        result = handlePost(self.path)
        # "miss", "hit", "sank D", "hit rep", "oob"
        if(result == "miss"):
            self.send_response(200, "hit={}".format(0))
        elif(result == "hit"):
            self.send_response(200, "hit={}".format(1))
        elif(result == "hit rep"):
            self.send_response(410)
        elif(result == "oob"):
            self.send_response(404)
        # C B R S D
        elif(result == "sank C"):
            self.send_response(200, "hit={}&sink={}".format(1,'C'))
        elif(result == "sank B"):
            self.send_response(200, "hit={}&sink={}".format(1,'B'))       
        elif(result == "sank R"):
            self.send_response(200, "hit={}&sink={}".format(1,'R'))
        elif(result == "sank S"):
            self.send_response(200, "hit={}&sink={}".format(1,'S'))
        elif(result == "sank D"):
            self.send_response(200, "hit={}&sink={}".format(1,'D'))
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
httpd = HTTPServer(('192.168.0.197', int(sys.argv[1])), SimpleHTTPRequestHandler)
gameboard = makeBoard(sys.argv[2])
print(gameboard)
# Server do server things forever
httpd.serve_forever()