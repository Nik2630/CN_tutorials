import socket
import time
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def reverse_string(s):
    return s[::-1]

def handle_client(client_socket, client_address):
    print(f"Thread ID: {threading.current_thread().name} handling client: {client_address}") # Print thread name
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return

        print(f"Thread {threading.current_thread().name} received message: {data}")
        reversed_message = reverse_string(data)
        time.sleep(3)
        client_socket.send(reversed_message.encode())
        print(f"Thread {threading.current_thread().name} sent reversed message: {reversed_message}")

    except socket.error as e:
        print(f"Thread {threading.current_thread().name} socket error with client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Thread {threading.current_thread().name} connection closed with {client_address}")

def multi_threaded_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print(f"Multi-Threaded Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address)) # Create a new thread
        client_thread.daemon = True # Allow main thread to exit even if threads are alive
        client_thread.start() # Start the thread

if __name__ == '__main__':
    multi_threaded_server()