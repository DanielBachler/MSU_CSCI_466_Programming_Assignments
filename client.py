import http.client
import sys

localServerAddress = sys.argv[1]
localServerPort = sys.argv[2]
x = sys.argv[3]
y = sys.argv[4]

connection = http.client.HTTPConnection(localServerAddress, localServerPort, timeout=10)
#fire action
connection.request("POST", "x={}&y={}".format(x,y))
#result
response = connection.getresponse()
print(response.status)
print(response.reason)
connection.close()