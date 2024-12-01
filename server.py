from threading import Thread, RLock, Condition
from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack
from sys import argv, exit

INPUT_SIZE_FORMAT = ">I"


class Monitor:
    """A generic monitor class, derive from this class and
	   call super().__init__()
	   then decorate sync methods with Monitor.sync """

    def __init__(self):
        self.mlock = RLock()

    @classmethod
    def sync(self, method):

        def w(self, *p, **kw):
            with self.mlock:
                return method(self, *p, **kw)

        return w

    def CV(self):
        """Create condition variables with this method to get
		   them share the monitor lock"""
        return Condition(self.mlock)


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
                    self.sock.send('\n'.join(mlist).encode())
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
