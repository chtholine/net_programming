import socket


class Customer:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def main():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address
    server_address = ('localhost', 1060)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Get user credentials
        username = input('Enter username: ')
        password = input('Enter password: ')

        # Send username and password to the server
        client_socket.sendall(username.encode())
        client_socket.sendall(password.encode())

        # Receive and print login status from the server
        login_status = client_socket.recv(1024).decode()
        print(login_status)

        # If the user needs to register, get name and surname and send to the server
        if login_status == "Username not found. Please register.":
            name = input('Enter your name: ')
            surname = input('Enter your surname: ')
            client_socket.sendall(name.encode())
            client_socket.sendall(surname.encode())
            registration_status = client_socket.recv(1024).decode()
            print(registration_status)

        # If login is successful, enter the main loop
        elif login_status == "Login successful":
            while True:
                print("Choose an option:")
                print("1. View messages")
                print("2. Send a message")
                print("3. Logout")

                # Get user's choice
                choice = input()
                client_socket.sendall(choice.encode())

                if "1" in choice:
                    try:
                        # Receive and print messages from the server
                        messages = eval(client_socket.recv(1024).decode())
                        print("Messages:")
                        for message in messages:
                            for key, value in message.items():
                                print(f"{key}: {value}")
                    except Exception as e:
                        print(f'Error retrieving messages: {e}')
                elif "2" in choice:
                    # Get recipient's username and message from the user
                    other_username = input('Enter the username of the recipient: ')
                    message = input('Enter your message: ')

                    # Send recipient's username and message to the server
                    client_socket.sendall(other_username.encode())
                    client_socket.sendall(message.encode())

                    try:
                        # Receive and print the status of the message sending operation
                        status = client_socket.recv(1024).decode()
                        print(status)
                    except Exception as e:
                        print(f'Error sending message: {e}')
                elif "3" in choice:
                    try:
                        # Receive and print logout status from the server
                        logout_status = client_socket.recv(1024).decode()
                        print(logout_status)
                        break
                    except Exception as e:
                        print(f'Error logging out: {e}')

    except ConnectionRefusedError:
        print('Error: Connection refused. The server may not be running.')
    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Clean up the connection
        client_socket.close()


if __name__ == "__main__":
    main()
