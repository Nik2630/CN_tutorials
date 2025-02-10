import socket
import time
import os
import signal  # For handling child processes

SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def reverse_string(s):
    return s[::-1]

def handle_client(client_socket, client_address):
    print(f"Process ID: {os.getpid()} handling client: {client_address}") # Print process ID
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return

        print(f"Process {os.getpid()} received message: {data}")
        reversed_message = reverse_string(data)
        time.sleep(3)
        client_socket.send(reversed_message.encode())
        print(f"Process {os.getpid()} sent reversed message: {reversed_message}")

    except socket.error as e:
        print(f"Process {os.getpid()} socket error with client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Process {os.getpid()} connection closed with {client_address}")
        os._exit(0)  # Exit child process cleanly

def multi_process_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print(f"Multi-Process Server listening on {SERVER_HOST}:{SERVER_PORT}")

    def sigchld_handler(signum, frame):
        # Simple non-blocking wait to prevent zombies
        try:
            while os.waitpid(-1, os.WNOHANG)[0] > 0:
                pass
        except ChildProcessError:
            pass

    # Set up signal handler
    signal.signal(signal.SIGCHLD, sigchld_handler)

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            pid = os.fork()

            if pid == 0:  # Child process
                server_socket.close()
                handle_client(client_socket, client_address)
            else:  # Parent process
                client_socket.close()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

    server_socket.close()

if __name__ == '__main__':
    multi_process_server()