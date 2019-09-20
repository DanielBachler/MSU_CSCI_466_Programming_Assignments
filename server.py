import socket

# Socket for the local client to local server
localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Socket for "enemy" client to server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket for local client
localSocket.bind(("127.0.0.1", 8080))
# Bind socket for "enemy" client
#clientSocket.bind(("192.168.0.122", 8081))

#Connect to local client
localSocket.listen(1)
#Connect to enemy client
#clientSocket.listen(1)


while True:
    # Local client connection
    conn, addr = localSocket.accept()
    print(f"got connected to {addr}")
    conn.send(bytes("Hi this is the server", "utf-8 "))
    # Enemy client connection
    #connEnemy, addrEnemy = clientSocket.accept()
    #print(f"got connected to {addrEnemy}")
    #connEnemy.send(bytes("Hi this is the server", "utf-8 "))