import socket
import threading # For thread creation
import common

HOST = common.HOST
PORT = common.PORT
BUFFER_SIZE = common.BUFFER_SIZE

def handle_client_thread(client_socket, client_address):
    """Handles a client connection in a separate thread."""
    print(f"Thread ID: {threading.current_thread().name} handling client {client_address}")
    handle_client_request(client_socket, client_address) # Reuse the request handler

def handle_client_request(client_socket, client_address):
    print(f"Connected by {client_address} in thread {threading.current_thread().name}")
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            decoded_data = data.decode()
            print(f"Thread {threading.current_thread().name} received from client {client_address}: {decoded_data}")

            choice, task_data = decoded_data.split(":", 1)

            if choice == '1':
                result = common.change_case(task_data)
            elif choice == '2':
                result = common.evaluate_expression(task_data)
            elif choice == '3':
                result = common.reverse_string(task_data)
            else:
                result = "Invalid task choice"

            client_socket.sendall(result.encode())

    except Exception as e:
        print(f"Thread {threading.current_thread().name} error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Thread {threading.current_thread().name} connection with {client_address} closed.")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Multi-Threaded Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_thread, args=(conn, addr)) # Create a new thread
            client_thread.start() # Start the thread


if __name__ == "__main__":
    main()