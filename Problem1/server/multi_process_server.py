import socket
import os  # For process creation (fork)
import common

HOST = common.HOST
PORT = common.PORT
BUFFER_SIZE = common.BUFFER_SIZE

def handle_client_process(client_socket, client_address):
    """Handles a client connection in a separate process."""
    print(f"Process ID: {os.getpid()} handling client {client_address}")
    handle_client_request(client_socket, client_address) # Reuse the request handler


def handle_client_request(client_socket, client_address):
    print(f"Connected by {client_address} in process {os.getpid()}")
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            decoded_data = data.decode()
            print(f"Process {os.getpid()} received from client {client_address}: {decoded_data}")

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
        print(f"Process {os.getpid()} error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Process {os.getpid()} connection with {client_address} closed.")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Multi-Process Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            process_id = os.fork() # Create a new process
            if process_id == 0: # Child process
                server_socket.close() # Child process doesn't need the listening socket
                handle_client_process(conn, addr) # Handle client in child process
                exit(0) # Child process exits after handling client
            else: # Parent process
                conn.close() # Parent process doesn't need the client socket
                # Parent process continues to accept new connections


if __name__ == "__main__":
    main()