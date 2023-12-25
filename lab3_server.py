import socket
import threading


class Customer:
    def __init__(self, username, password, name, surname):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.talks = {}  # Dictionary to store messages with other users

    def addTalk(self, user):
        if user.username not in self.talks:
            self.talks[user.username] = []

    def addMessage(self, message, user, sender):
        if user.username in self.talks:
            self.talks[user.username].append({sender: message})  # Appending message dictionaries

    def getMessages(self):
        return [message for messages in self.talks.values() for message in messages]


def handle_client(client_socket, users):
    try:
        # Receive username and password from the client
        username = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()

        # Authenticate the user
        if username in users:
            if users[username].password == password:
                client_socket.sendall("Login successful".encode())
                current_user = users[username]
            else:
                client_socket.sendall("Invalid password".encode())
                return
        else:
            # Register the user
            client_socket.sendall("Username not found. Please register.".encode())
            name = client_socket.recv(1024).decode()
            surname = client_socket.recv(1024).decode()
            users[username] = Customer(username, password, name, surname)
            client_socket.sendall(f"Registration successful. Welcome {name} {surname}. Please reconnect.".encode())
            current_user = users[username]

        while True:
            # Receive the user's choice
            choice = client_socket.recv(1024).decode()

            if "1" in choice:
                # Send messages to the client
                messages = current_user.getMessages()
                client_socket.sendall(str(messages).encode())
            elif "2" in choice:
                # Send a message to another user
                other_username = client_socket.recv(1024).decode()
                message = client_socket.recv(1024).decode()

                other_user = users.get(other_username)
                if other_user:
                    # Update message history for both users
                    current_user.addTalk(other_user)
                    current_user.addMessage(message, other_user, current_user.username)
                    other_user.addTalk(current_user)
                    other_user.addMessage(message, current_user, current_user.username)
                    client_socket.sendall("Message sent successfully".encode())
                else:
                    client_socket.sendall("User not found".encode())
            elif "3" in choice:
                # Logout the user
                client_socket.sendall("Logout successful".encode())
                break
    finally:
        client_socket.close()


def main():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configure server address and bind the socket
    server_address = ('localhost', 1060)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)
    print('Server is listening on {}:{}'.format(*server_address))

    # Sample user data
    users = {
        'user1': Customer('user1', 'pass1', 'John', 'Doe'),
        'user2': Customer('user2', 'pass2', 'Alice', 'Smith')
    }

    while True:
        print('Waiting for a connection...')
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, users))
        client_handler.start()


if __name__ == "__main__":
    main()
