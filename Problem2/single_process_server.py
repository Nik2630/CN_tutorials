import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def reverse_string(s):
    return s[::-1]

def handle_client(client_socket, client_address):
    print(f"Connection from: {client_address}")
    try:
        data = client_socket.recv(1024).decode()  # Receive data from client
        if not data:
            return  # Client disconnected

        print(f"Received message from client: {data}")
        reversed_message = reverse_string(data)
        time.sleep(3)  # Simulate 3-second delay
        client_socket.send(reversed_message.encode()) # Send reversed string back
        print(f"Sent reversed message: {reversed_message}")

    except socket.error as e:
        print(f"Socket error with client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed with {client_address}")

def single_process_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))  # Bind socket to address
    server_socket.listen() 
    print(f"Single-Process Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()  # Accept a connection
        handle_client(client_socket, client_address) # Handle client in the main process

if __name__ == '__main__':
    single_process_server()