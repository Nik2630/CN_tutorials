import socket

SERVER_HOST = 'localhost'  # Or '127.0.0.1'
SERVER_PORT = 12345        # Choose a port number (must be the same for server and client)
MESSAGE = "hello server"   # The string to send

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))  # Connect to the server
        client_socket.send(MESSAGE.encode())  # Send message as bytes
        data = client_socket.recv(1024).decode()  # Receive response, decode bytes to string
        print(f"Received from server: {data}")  # Print the reversed string
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        client_socket.close()  # Close the connection

if __name__ == '__main__':
    client_program()