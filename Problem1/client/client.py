import socket
import common

HOST = common.HOST
PORT = common.PORT
BUFFER_SIZE = common.BUFFER_SIZE

def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print("Connected to server at", (HOST, PORT))
        
        while True:
            print("\nChoose a task:")
            print("1. Change Case")
            print("2. Evaluate Expression")
            print("3. Reverse String")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '4':
                print("Exiting...")
                break

            if choice not in ('1', '2', '3'):
                print("Invalid choice. Please enter a number between 1 and 4.")
                continue

            data_to_send = choice + ":"

            if choice == '1':
                text = input("Enter a string to change case: ")
                data_to_send += text
            elif choice == '2':
                expression = input("Enter a mathematical expression: ")
                data_to_send += expression
            elif choice == '3':
                text = input("Enter a string to reverse: ")
                data_to_send += text

            try:
                client_socket.sendall(data_to_send.encode())
                response = client_socket.recv(BUFFER_SIZE).decode()
                print(f"Server response: {response}")
            except socket.error as e:
                print(f"Socket error: {e}")
                print("Connection to server lost.")
                break

    except socket.error as e:
        print(f"Failed to connect to server: {e}")
        print("Please make sure the server is running and accessible.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()