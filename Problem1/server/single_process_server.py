import socket
import common

HOST = common.HOST
PORT = common.PORT
BUFFER_SIZE = common.BUFFER_SIZE

def handle_client_request(client_socket, client_address):
    print(f"Connected by {client_address}")
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break # Client disconnected
            decoded_data = data.decode()
            print(f"Received from client {client_address}: {decoded_data}")

            choice, task_data = decoded_data.split(":", 1) # Split into choice and data

            if choice == '1':
                result = common.change_case(task_data)
            elif choice == '2':
                result = common.evaluate_expression(task_data)
            elif choice == '3':
                result = common.reverse_string(task_data)
            else:
                result = "Invalid task choice"

            client_socket.sendall(result.encode()) # Send the result back

    except Exception as e: # Catch potential errors during client handling
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed.")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Single-Process Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept() # Accept a connection
            handle_client_request(conn, addr) 

if __name__ == "__main__":
    main()