from server import INPUT_SIZE_FORMAT
from socket import socket, AF_INET, SOCK_STREAM
from struct import pack
from sys import argv, exit


def main() -> None:
    if len(argv) != 3:
        print("usage: ", argv[0], "--port", "[PORT]")
        exit(-1)

    HOST = ""
    PORT = int(argv[2])
    c = socket(AF_INET, SOCK_STREAM)
    c.connect((HOST, PORT))

    while True:
        message = input()
        c.send(pack(INPUT_SIZE_FORMAT, len(message)))
        c.send(message.encode())

        reply = c.recv(1024)
        print(reply.decode())

    c.close()


if __name__ == "__main__":
    main()
