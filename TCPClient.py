# Import socket module
from socket import * 
import sys # In order to terminate the program

serverName = 'localhost'
# Assign a port number
serverPort = 120

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

# Recieves client number from server and prints it
clientNo = clientSocket.recv(1024)
print(clientNo.decode())

while True:
        sentence = input('Enter message: ')
        if (sentence != 'exit'):
            clientSocket.send(sentence.encode())
        else:
            print('closing socket')
            clientSocket.close()
            break

        while True:
            modifiedSentence = clientSocket.recv(1024)
            print('Server Response:', modifiedSentence.decode())
            break
    
