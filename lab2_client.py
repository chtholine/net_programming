import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 1060)

    try:
        client_socket.connect(server_address)

        # Receive the question from the server
        question = client_socket.recv(1024).decode()
        print('Server question:', question)

        # Send an answer to the server
        answer = input('Your answer: ')
        client_socket.sendall(answer.encode())

        # Set a timeout for receiving the server confirmation
        client_socket.settimeout(5)

        try:
            # Wait for the server confirmation
            confirmation = client_socket.recv(1024).decode()
            print('Server confirmation:', confirmation)
        except socket.timeout:
            print('Error: Server confirmation timeout. The server may not be responding.')

    except ConnectionRefusedError:
        print('Error: Connection refused. The server may not be running.')
    except Exception as e:
        print(f'Error: {e}')

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
