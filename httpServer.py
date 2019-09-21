#Dan and Logan, HTTP Server to run Battleship from
# import needed libraries
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import socketserver
import sys
import re

# Takes in the gameboard file and returns a "2D array" of it
def makeBoard(fileName):
    # Open file provided by sys arg to read
    boardFile = open(fileName, 'r')
    # Create an empty 10x10 matrix
    gameboard = [['0' for x in range(10)] for y in range(10)]
    # Iterate over the 10 lines of the file
    for i in range(0,10):
        # Get each line
        line = boardFile.readline()
        # Iterate over the line and place each indivdual character into the matrix
        for j in range(0,10):
            gameboard[i][j] = line[j]
    # Close the file to prevent memory leaks
    boardFile.close()
    # Return completed gameboard object
    return gameboard

# Prints the gameboard in a nicely formatted way
def printBoard():
    for i in range(0,10):
        print(gameboard[i])

# Takes the POST request and determines how to reply
def handlePost(request):
    # Cleaning the input of unneeded characters
    request = re.sub('[yx=]', '', request)
    request = re.sub('[&]', ' ', request)
    # Splits the request into 2 strings on the space added by regex
    request = request.split(" ")
    
    # checking for request formatting errors, if not what is expected then return bad formatting
    try:
        x = int(request[0])
        y = int(request[1])
    except:
        return "bad-req"
    # If coords are out of bounds sends that request
    if((x > 9 and x < 0) or (y > 9 or y < 0)):
        return "oob"
    # Get value into one var so I dont have to type gameboard[x][y] a thousand times
    target = gameboard[x][y]

    # Target handling
    # If the square being shot is not water keep going through logic tree
    # else return miss val
    if(target != '_'): 
        # If the targetted square is a letter and lower case it has been shot already
        if(target.islower()):
            return "hit rep"
        # Sets the hit square to lower to show it has been shot at
        gameboard[x][y] = target.lower()
        # Check if that shot sank the ship
        # If it didn't, then return normal hit
        if(didSink(target)):
            return "sank " + target
        else:
            return "hit"
    else:
        return "miss"

# Checks if a given ship is sunk or not
def didSink(shipType):
    # Assume the ship is sunk until proven otherwise
    # Iterate over the entire board, looking for an uppercase marker 
    for i in range(0,10):
        for j in range(0,10):
            # If an uppercase marker is found return false
            if gameboard[i][j] == shipType:
                return False
    return True

# The base form for server and request handler taken from online examples
# Found at: (TODO insert)

#Handle override
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # When contacted by a client, send gameboard
    def do_GET(self):
        # Needed for "proper" request
        self.send_response(200)
        self.end_headers()
        # Prints gameboard to local site
        self.wfile.write(bytes("Your board\n", "UTF-8"))
        for i in range(0,10):
            for j in range(0,10):
                self.wfile.write(bytes(gameboard[i][j], "UTF-8"))
            self.wfile.write(b'\n')
        # Prints opponent board
        self.wfile.write(bytes("\nOpponent board\n", "UTF-8"))
        array = [[0 for x in range(10)] for y in range(10)]
        with open("opponent_board.csv", mode="r") as file:
            counter = 0
            #seperates the various levels of lists and and fills the array
            lines = [line.split() for line in file]
            for line in lines:
                if(len(line) > 0):
                    line = line[0].split(',')
                    for i in range(10):
                        array[counter][i] = line[i]
                    counter += 1
            #prints the array
            for i in range(10):
                for j in range(10):
                    self.wfile.write(bytes(array[i][j], "UTF-8"))
                self.wfile.write(b'\n')

    # Handling POST requests
    def do_POST(self):
        # Get the value of result from handlePost, and send the correct HTTP message
        result = handlePost(self.path)

        # Possible values returned
        # "miss", "hit", "sank [CBRSD]", "hit rep", "oob", "bad-req"
        if(result == "miss"):
            self.send_response(200, "hit={}".format(0))
        elif(result == "hit"):
            self.send_response(200, "hit={}".format(1))
        elif(result == "hit rep"):
            self.send_response(410)
        elif(result == "oob"):
            self.send_response(404)
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
        # Closes header, needed for proper formatted request
        self.end_headers()
        # Print the board after each request
        printBoard()

# Init server on ip for given IP on TCP port provided by Sys ARGS.
# Port must be open on firewall
httpd = HTTPServer(('192.168.0.197', int(sys.argv[1])), SimpleHTTPRequestHandler)
# Creates the board from the Sys ARG file
gameboard = makeBoard(sys.argv[2])
# Prints the inital board
printBoard()
# Server runs until ctrl+C is pressed in terminal
httpd.serve_forever()