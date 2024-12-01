from monitor import Monitor
from socket import AF_INET, socket, SOCK_STREAM
from struct import pack, unpack
from sys import argv, exit
from threading import Thread

INPUT_SIZE_FORMAT = ">I"


class Chat(Monitor):

    def __init__(self):
        super().__init__()
        self.buf = []
        self.newmess = self.CV()

    @Monitor.sync
    def newmessage(self, mess):
        self.buf.append(mess)
        self.newmess.notify_all()

    @Monitor.sync
    def getmessages(self, after=0):
        if len(self.buf) < after:
            a = []
        else:
            a = self.buf[after:]
        return a

    @Monitor.sync
    def wait(self):
        self.newmess.wait()


class WRAgent(Thread):

    def __init__(self, sock, addr, chat):
        self.sock, self.addr = sock, addr
        self.chat = chat
        self.current = 0
        self.notexit = True
        Thread.__init__(self)

    def run(self):
        while True:
            oldmess = self.chat.getmessages(self.current)
            if len(oldmess) != 0:
                self.current += len(oldmess)
                try:
                    mlist = [
                        str(addr) + ":" + m.strip().decode()
                        for (addr, m) in oldmess
                    ] + [""]
                    message = '\n'.join(mlist).encode()
                    self.sock.send(pack(INPUT_SIZE_FORMAT, len(message)))
                    self.sock.send(message)
                except Exception:
                    print("Writer terminating")
                    break

            self.chat.wait()


class RDAgent(Thread):

    def __init__(self, sock, addr, chatroom):
        self.sock, self.addr, self.chatroom = sock, addr, chatroom
        super().__init__()

    def run(self):
        while True:
            packed_input_size = self.sock.recv(
                4)  # An unsigned int takes 4 bytes
            if not packed_input_size:
                break
            input_size = unpack(INPUT_SIZE_FORMAT, packed_input_size)[0]
            input = self.sock.recv(input_size)
            if not input:
                break
            self.chatroom.newmessage((self.addr, input))
        print("peer closed the connection")
        self.sock.close()
        self.chatroom.newmessage((self.addr, b"bye"))


def main() -> None:
    if len(argv) != 3:
        print("usage: ", argv[0], "--port", "[PORT]")
        exit(-1)

    HOST = ""
    PORT = int(argv[2])
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    chatroom = Chat()

    while True:
        conn, addr = s.accept()

        print("Connected by", addr)
        a = RDAgent(conn, addr, chatroom)
        b = WRAgent(conn, addr, chatroom)
        a.start()
        b.start()


if __name__ == "__main__":
    main()
