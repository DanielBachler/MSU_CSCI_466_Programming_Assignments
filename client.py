#Kyle Webster- HTTP Client
import http.client
import sys
import csv

array = [[0 for x in range(10)] for y in range(10)]
#writes either the hit or miss to the csv file
def write(x,y,status):
    with open("opponent_board.csv", mode = "w") as file:
        writer = csv.writer(file, delimiter=',')
        for i in array:
            writer.writerow(i)
#Made read to read the csv file (Choosen for formatting purposes) and print an output that the user can see with each move
def read(x,y, status):
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
        array[int(x)][int(y)] = status
        #prints the array
        #for i in range(10):
        #    print(array[i])
    write(x,y,status)

#uses the arguments to create the required variables
localServerAddress = sys.argv[1]
localServerPort = sys.argv[2]
x = sys.argv[3]
y = sys.argv[4]

#The server we are connected to
connection = http.client.HTTPConnection(localServerAddress, localServerPort, timeout=10)
#Sends fire action to server
connection.request("POST", "x={}&y={}".format(x,y))
#Processes response, first checking for bad messages
response = connection.getresponse()
file = "board.csv"
if(response.status == 404):
    print("Shot was out of bounds, try again.")
elif(response.status == 410):
    print("Something went wrong with the opponents board")
elif(response.status == 400):
    print("enter (x,y) coordinates as numbers... No funny A3 shenanagins")
elif("hit=1&sink=" in response.reason):
    print("Hit and sink" , response.reason[-1])
elif("hit=" in response.reason):
    read(x,y,response.reason[4])
else:
    print(response.status, response.reason)

connection.close()
