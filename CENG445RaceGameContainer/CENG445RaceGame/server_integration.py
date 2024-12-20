from django.http import HttpRequest
from socket import AF_INET, SOCK_STREAM, socket
from source.socket_helpers import read_variable_size, write_variable_size

HOST = ""
PORT = 12345


def communicate_with_server(request: HttpRequest,
                            message: str) -> bytes | None:
    with socket(AF_INET, SOCK_STREAM) as communication_socket:
        communication_socket.connect((HOST, PORT))

        # Authenticate
        username = request.user.username
        write_variable_size(communication_socket, username)

        write_variable_size(communication_socket, message)
        reply = read_variable_size(communication_socket)
        return reply
