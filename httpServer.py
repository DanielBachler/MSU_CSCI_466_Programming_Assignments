#Dan and Logan, HTTP Server to run Battleship from
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import socketserver
import sys
import numpy as np
import re

# Takes in the gameboard file and returns a 2D array of it
def makeBoard(fileName):
    boardFile = open(fileName, 'r')
    gameboard = [['0' for x in range(10)] for y in range(10)]
    for i in range(0,10):
        line = boardFile.readline()
        #print(line)
        for j in range(0,10):
            gameboard[i][j] = line[j]
    boardFile.close()
    return gameboard

def printBoard():
    for i in range(0,10):
        print(gameboard[i])

# Takes the POST request and determines if that hits or not
def handlePost(request):
    request = re.sub('[yx=]', '', request)
    request = re.sub('[&]', ' ', request)
    request = request.split(" ")
    
    try:
        x = int(request[0])
        y = int(request[1])
    except:
        return "bad-req"
    #global gameboard
    # C B R S D
    # If out of bounds handle
    if((x > 9 and x < 0) or (y > 9 or y < 0)):
        return "oob"
    # Get value into one var so I dont have to type gameboard[x][y] a thousand times
    target = gameboard[x][y]
    # Target handling
    if(target != '_'): 
        if(target.islower()):
            return "hit rep"
        gameboard[x][y] = target.lower()
        if(didSink(target)):
            return "sank " + target
        else:
            return "hit"
    else:
        return "miss"

def didSink(shipType):
    shipSunk = True
    for i in range(0,10):
        for j in range(0,10):
            if gameboard[i][j] == shipType:
                shipSunk = False
    return shipSunk

# The base form for server and request handler taken from online examples
# Found at: (TODO insert)

#Handle override
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # When contacted by a client, send gameboard
    def do_GET(self):
        # Needed
        self.send_response(200)
        self.end_headers()
        # Send message
        for i in range(0,10):
            for j in range(0,10):
                self.wfile.write(bytes(gameboard[i][j], "UTF-8"))
            self.wfile.write(b'\n')

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
        elif(result == "bad-req"):
            self.send_response(400)
        self.end_headers()
        printBoard()
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
httpd = HTTPServer(('100.64.11.151', int(sys.argv[1])), SimpleHTTPRequestHandler)
gameboard = makeBoard(sys.argv[2])
printBoard()
# Server do server things forever
httpd.serve_forever()
