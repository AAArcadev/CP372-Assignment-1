import socket
import threading
import datetime
import sys

HEADER_SIZE = 8
MAX_CLIENTS = 3

SERVER_IP = '127.0.0.1'
SERVER_PORT = 120

clients = {}
client_count = 0
client_address_list = [0,0,0]

def run_server():
    global client_count

    #Misc Variables
    atLimitPrinted = False
    
    # Bind socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(MAX_CLIENTS)
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}.")

    while True:
        # Add client if limit not reached
        if client_count < MAX_CLIENTS:
            client_socket, client_address = server_socket.accept()
            client_count += 1
            client_name = f"Client{client_count:02d}"
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_name))
            client_thread.start()
        elif not atLimitPrinted: # Keeps track if the following sentence has been printed
            print("Max number of clients reached. Please wait")
            atLimitPrinted = True

def handle_client(client_socket, client_address, client_name):
    global client_count
    global client_address_list
    print(f"{client_name} connected from {client_address}")

    # Log info about the connection
    connection_start_time = datetime.datetime.now() # Changed from 'datetime.now() to datetime.datetime.now()
    clients[client_name] = {
        'address': client_address,
        'start_time': connection_start_time,
        'end_time': None
    }

    client_socket.send(f"You are {client_name}".encode())

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(f"Received from {client_name}: {data}")
        if data.lower() == "exit":
            print(f"{client_name} is disconnecting")
            clients[client_name]['end_time'] = datetime.now() # Changed from 'datetime.now() to datetime.datetime.now() 
            break
        
        elif data.lower() == "status":
            status_message = "Connected clients:\n"
            clientNumOn = 0
            for name, info in clients.items():
                start_time_str = info['start_time'].strftime('%Y-%m-%d %H:%M:%S')
                end_time_str = info['end_time'].strftime('%Y-%m-%d %H:%M:%S') if info['end_time'] else "Still connected"
                status_message += f"{name}: address: {info['address']}, connected at {start_time_str}, ended at {end_time_str}\n"
                clientNumOn += 1
            client_socket.send(status_message.encode())    

        else:
            client_socket.send(f"{data} ACK".encode())

    client_socket.close()
    print(f"{client_name} disconnected")
    client_count -= 1
    

if __name__ == "__main__":
    run_server()
