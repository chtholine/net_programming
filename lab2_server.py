import socket
import random

# Define the questions
questions = [
    "What is your favorite color?",
    "What is the capital of Romania?",
    "How many continents are there?",
]


def main():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 1060)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server is listening on {}:{}'.format(*server_address))

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()

        try:
            print('Connection from', client_address)

            # Choose a random question for the client
            random_question = random.choice(questions)
            connection.sendall(random_question.encode())

            # Receive the answer from the client
            client_answer = connection.recv(1024).decode()
            print('Client answer:', client_answer)

            # Send a confirmation message to the client
            connection.sendall('Data received'.encode())

        finally:
            # Clean up the connection
            connection.close()


if __name__ == "__main__":
    main()
