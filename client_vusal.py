from socket import AF_INET, socket, SOCK_STREAM
from source.socket_helpers import read_variable_size, write_variable_size
from sys import argv, exit
from threading import Thread


class WRAgent(Thread):

    def __init__(self, sock):
        self.sock = sock
        Thread.__init__(self)

    def run(self):
        while True:
            message = input("> ")  # Prompt for user input
            if not message:
                break
            write_variable_size(self.sock, message)


class RDAgent(Thread):

    def __init__(self, sock):
        self.sock = sock
        super().__init__()

    def run(self):
        while True:
            reply = read_variable_size(self.sock)
            if reply is None:
                break
            print(reply.decode())
        print("Connection to server closed.")
        self.sock.close()


def main():
    if len(argv) != 3 or argv[1] != "--port":
        print("Usage: python client.py --port <PORT>")
        exit(1)

    HOST = "localhost"  # Change to server's IP if not local
    PORT = int(argv[2])
    c = socket(AF_INET, SOCK_STREAM)
    c.connect((HOST, PORT))

    print("Connected to server.")
    reader = RDAgent(c)
    writer = WRAgent(c)
    reader.start()
    writer.start()
    reader.join()
    writer.join()


if __name__ == "__main__":
    main()
