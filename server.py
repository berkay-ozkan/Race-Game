from id_tracker import ID_Tracker
from monitor import Monitor
from socket import AF_INET, socket, SOCK_STREAM
from repo import Repo
from socket_helpers import read_variable_size, write_variable_size
from sys import argv, exit
from threading import Thread


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
                    message = '\n'.join(mlist)
                    write_variable_size(self.sock, message)
                except Exception:
                    print("Writer terminating")
                    break

            self.chat.wait()


class RDAgent(Thread):

    def __init__(self, sock, addr, chatroom, repo: Repo):
        self.sock, self.addr, self.chatroom, self.repo = sock, addr, chatroom, repo
        self.username: str
        super().__init__()

    def read_username(self) -> None:
        encoded_input = read_variable_size(self.sock)
        input = encoded_input.decode()  # type: ignore[union-attr]

        username = input[input.find("USER") + 4:]
        self.username = username

    def run(self):
        self.read_username()

        while True:
            encoded_input = read_variable_size(self.sock)
            if encoded_input is None:
                break
            input = encoded_input.decode()

            # TODO: Evaluate commands as required
            reply = eval(input)
            if reply is not None:
                self.chatroom.newmessage((self.username, str(reply).encode()))

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
    repo = Repo()

    while True:
        conn, addr = s.accept()

        print("Connected by", addr)
        a = RDAgent(conn, addr, chatroom, repo)
        b = WRAgent(conn, addr, chatroom)
        a.start()
        b.start()


if __name__ == "__main__":
    main()
