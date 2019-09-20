import socket

# Local server socket
localServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enemy server socket
enemyServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to local server
localServer.connect(("127.0.0.1",8080))
# Connect to enemy server
enemyServer.connect(("192.168.0.197", 8081))


while True:
    # Message from local server
    msg = localServer.recv(128)
    print(msg.decode("utf-8"))
    # Message from enemy server
    msgE = enemyServer.recv(128)
    print(msgE.decode("utf-8"))
