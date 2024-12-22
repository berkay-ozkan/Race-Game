from socket import AF_INET, socket, SOCK_STREAM
from backend.source.socket_helpers import read_variable_size, write_variable_size
from sys import argv, exit
from threading import Thread


class WRAgent(Thread):

    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        while True:
            message = input()
            if not message:
                break
            write_variable_size(self.sock, message)


class RDAgent(Thread):

    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        while True:
            reply = read_variable_size(self.sock)
            if reply is None:
                break
            print(reply.decode())

        print("The server closed the connection.")
        self.sock.close()


def main() -> None:
    if len(argv) != 3:
        print("usage: ", argv[0], "--port", "[PORT]")
        exit(-1)

    HOST = ""
    PORT = int(argv[2])
    c = socket(AF_INET, SOCK_STREAM)
    c.connect((HOST, PORT))

    a = RDAgent(c)
    b = WRAgent(c)
    a.start()
    b.start()


if __name__ == "__main__":
    main()
