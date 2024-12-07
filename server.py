from inspect import signature
from json import loads
from source.id_tracker import ID_Tracker
from source.monitor import Monitor
from socket import AF_INET, socket, SOCK_STREAM
from source.object import Object
from source.objects.components import Car
from source.objects.components.cells.booster import Booster
from source.objects.components.cells.checkpoint import Checkpoint
from source.objects.components.cells.fuel import Fuel
from source.objects.components.cells.road import Road
from source.objects.components.cells.roads.diagonal import Diagonal
from source.objects.components.cells.roads.straight import Straight
from source.objects.components.cells.roads.turn90 import Turn90
from source.objects.components.cells.rock import Rock
from source.repo import Repo
from source.socket_helpers import read_variable_size, write_variable_size
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
        super().__init__()
        self.sock, self.addr = sock, addr
        self.chat = chat
        self.current = 0
        self.notexit = True

    def run(self):
        while True:
            oldmess = self.chat.getmessages(self.current)
            if len(oldmess) != 0:
                self.current += len(oldmess)
                try:
                    mlist = [
                        str(addr) + ": " + m.strip().decode()
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
        super().__init__()
        self.sock, self.addr, self.chatroom, self.repo = sock, addr, chatroom, repo
        self.username: str

    def read_username(self) -> None:
        encoded_input = read_variable_size(self.sock)
        input = encoded_input.decode().split()  # type: ignore[union-attr]

        username = input[1]
        self.username = username

    def run_command(self, decoded_input: dict) -> str | None:
        if "id" in decoded_input:
            id = decoded_input["id"]
            object = ID_Tracker()._objects[id]
        else:
            object = self.repo

        function_name: str = decoded_input["function_name"]
        if function_name.startswith('_'):
            return "Calling internal functions is not supported"

        parameters = decoded_input["parameters"]

        function = getattr(object, function_name)
        function_signature = signature(function)
        for parameter in function_signature.parameters.values():
            parameter_name = parameter.name
            parameter_type = parameter.annotation
            if issubclass(parameter_type, Object):
                object_id = parameters[parameter_name]
                object = ID_Tracker()._objects[object_id]
                parameters[parameter_name] = object

        result = function(**parameters)
        if result is not None:
            return str(result)
        return None

    def run(self):
        self.read_username()

        while True:
            encoded_input = read_variable_size(self.sock)
            if encoded_input is None:
                break
            decoded_input = loads(encoded_input.decode())

            result = self.run_command(decoded_input)
            if result is not None:
                self.chatroom.newmessage((self.username, result.encode()))

        print(self.username, "closed the connection.")
        self.chatroom.newmessage(f"{self.username} closed the connection.")
        self.sock.close()


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

    repo.components.register("car", Car)
    repo.components.register("diagonal", Diagonal)
    repo.components.register("straight", Straight)
    repo.components.register("turn90", Turn90)
    repo.components.register("booster", Booster)
    repo.components.register("checkpoint", Checkpoint)
    repo.components.register("fuel", Fuel)
    repo.components.register("road", Road)
    repo.components.register("rock", Rock)

    while True:
        conn, addr = s.accept()

        print("Connected by", addr)
        a = RDAgent(conn, addr, chatroom, repo)
        b = WRAgent(conn, addr, chatroom)
        a.start()
        b.start()


if __name__ == "__main__":
    main()
