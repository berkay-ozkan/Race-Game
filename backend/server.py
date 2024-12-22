from inspect import Signature, signature
from json import loads
from dill import dump
from backend.source.id_tracker import ID_Tracker
from socket import AF_INET, socket, SOCK_STREAM
from backend.source.objects.components import Car
from backend.source.objects.components.cells.booster import Booster
from backend.source.objects.components.cells.fuel import Fuel
from backend.source.objects.components.cells.roads.diagonal import Diagonal
from backend.source.objects.components.cells.roads.straight import Straight
from backend.source.objects.components.cells.roads.turn90 import Turn90
from backend.source.objects.components.cells.rock import Rock
from backend.source.observer import Observer
from backend.source.repo import Repo
from backend.source.socket_helpers import read_variable_size, write_variable_size
from sys import argv, exit
from threading import Thread


class Notifications(Thread):

    def __init__(self, sock: socket, username: str, observer: Observer):
        super().__init__()
        self.sock: socket = sock
        self.username: str = username
        self.observer: Observer = observer

        self.current = 0
        self.notexit = True

    def run(self):
        while True:
            view_id = self.observer.wait(self.username)

            if view_id is not None:
                print("Sending notification")
                new_state = ID_Tracker()._objects[view_id].draw()
                write_variable_size(self.sock, new_state)


class Replies(Thread):

    def __init__(self, sock: socket, username: str, repo: Repo):
        super().__init__()
        self.sock: socket = sock
        self.username: str = username
        self.repo: Repo = repo

    def run_command(self, decoded_input: dict) -> str:
        if "id" in decoded_input:
            id = decoded_input["id"]
            object = ID_Tracker()._objects[id]
        else:
            object = self.repo

        function_name: str = decoded_input["function_name"]
        if Replies.is_internal(function_name):
            return "Calling internal functions is not supported"
        function = getattr(object, function_name)
        parameters = decoded_input["parameters"]

        result = function(*parameters[:-1], **parameters[-1])
        if result is not None:
            return str(result)
        return "Command executed"

    def run(self):
        while True:
            encoded_input = read_variable_size(self.sock)
            if encoded_input is None:
                break

            decoded_input = loads(encoded_input.decode())

            if decoded_input == "SAVE":
                with open('ID_Tracker.bin', 'wb') as file:
                    dump(ID_Tracker(), file)
                with open('Observer.bin', 'wb') as file:
                    dump(Observer(), file)
                write_variable_size(self.sock, "State saved")
                continue

            try:
                result = self.run_command(decoded_input)
            except Exception as exception:
                result = str(exception)

            write_variable_size(self.sock, result)

        print(self.username, "closed the connection.")
        self.sock.close()

    @staticmethod
    def is_internal(function_name: str) -> bool:
        if function_name.startswith("__") and function_name.endswith("__"):
            return False
        return function_name.startswith('_')


def main() -> None:
    if len(argv) != 3:
        print("usage: ", argv[0], "--port", "[PORT]")
        exit(-1)

    HOST = ""
    PORT = int(argv[2])
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    observer = Observer()
    repo = Repo()

    repo.components.register("car", Car)
    repo.components.register("diagonal", Diagonal)
    repo.components.register("straight", Straight)
    repo.components.register("turn90", Turn90)
    repo.components.register("booster", Booster)
    repo.components.register("fuel", Fuel)
    repo.components.register("rock", Rock)

    while True:
        conn, addr = s.accept()
        print("Connected by", addr)

        encoded_input = read_variable_size(conn)
        username = encoded_input.decode().strip()  # type: ignore[union-attr]

        a = Replies(conn, username, repo)
        a.start()


if __name__ == "__main__":
    main()
