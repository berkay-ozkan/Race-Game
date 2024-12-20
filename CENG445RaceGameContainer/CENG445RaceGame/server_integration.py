from django.http import HttpRequest
from socket import AF_INET, SOCK_STREAM, socket
from source.socket_helpers import INPUT_SIZE_FORMAT, read_variable_size
from struct import pack

HOST = ""
PORT = 12345


def write_to_backend(request: HttpRequest, command: str) -> bytes | None:
    # Authenticate
    username = request.user.username

    encoded_username = username.encode()
    username_message = pack(INPUT_SIZE_FORMAT,
                            len(encoded_username)) + encoded_username

    encoded_command = command.encode()
    command_message = pack(INPUT_SIZE_FORMAT,
                           len(encoded_command)) + encoded_command

    with socket(AF_INET, SOCK_STREAM) as communication_socket:
        communication_socket.connect((HOST, PORT))
        communication_socket.send(username_message + command_message)

        reply = read_variable_size(communication_socket)
        return reply
