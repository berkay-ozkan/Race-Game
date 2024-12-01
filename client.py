from server import INPUT_SIZE_FORMAT
from socket import AF_INET, socket, SOCK_STREAM
from struct import pack, unpack
from sys import argv, exit
from threading import Thread


class WRAgent(Thread):

    def __init__(self, sock):
        self.sock = sock
        Thread.__init__(self)

    def run(self):
        while True:
            message = input()
            if not message:
                break

            self.sock.send(pack(INPUT_SIZE_FORMAT, len(message)))
            self.sock.send(message.encode())


class RDAgent(Thread):

    def __init__(self, sock):
        self.sock = sock
        super().__init__()

    def run(self):
        while True:
            packed_reply_size = self.sock.recv(
                4)  # An unsigned int takes 4 bytes
            if not packed_reply_size:
                break
            reply_size = unpack(INPUT_SIZE_FORMAT, packed_reply_size)[0]
            reply = self.sock.recv(reply_size)
            if not reply:
                break

            print(reply.decode())
        print("peer closed the connection")
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
