from socket import socket
from struct import calcsize, pack, unpack

INPUT_SIZE_FORMAT = ">I"


def read_variable_size(socket: socket) -> None | bytes:
    packed_input_size = socket.recv(calcsize(INPUT_SIZE_FORMAT))
    if not packed_input_size:
        return None
    input_size = unpack(INPUT_SIZE_FORMAT, packed_input_size)[0]
    input = socket.recv(input_size)
    if not input:
        return None
    return input


def write_variable_size(socket: socket, message: str) -> None:
    encoded_message = message.encode()
    socket.send(pack(INPUT_SIZE_FORMAT, len(encoded_message)))
    socket.send(encoded_message)
