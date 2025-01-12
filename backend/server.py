from django import setup
from json import loads
from os import environ
from subprocess import Popen, PIPE
from sys import argv, exit, path
from threading import Thread
from websockets.sync.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

pwd = Popen(["pwd"], stdout=PIPE)
pwd.wait()
project_path = pwd.stdout.readline().decode().strip()
path.append(project_path)
environ.setdefault('DJANGO_SETTINGS_MODULE', 'CENG445RaceGame.settings')
setup()

from backend.source.component_factory import ComponentFactory
from backend.source.object import Object
from backend.source.objects.map import Map
from backend.source.objects.component import Component
from backend.source.objects.components import Car
from backend.source.objects.components.cells.booster import Booster
from backend.source.objects.components.cells.fuel import Fuel
from backend.source.objects.components.cells.roads.diagonal import Diagonal
from backend.source.objects.components.cells.roads.straight import Straight
from backend.source.objects.components.cells.roads.turn90 import Turn90
from backend.source.objects.components.cells.rock import Rock
from backend.source.objects.type_to_class import type_to_class
from backend.source.observer import Observer
from backend.source.repo import Repo
from backend.source.socket_helpers import read_variable_size, write_variable_size


class Notifications(Thread):

    def __init__(self, sock, username: str, observer: Observer):
        super().__init__()
        self.sock = sock
        self.username: str = username
        self.observer: Observer = observer

        self.current = 0
        self.notexit = True

    def run(self):
        while True:
            view_id = self.observer.wait(self.username)

            if view_id is not None:
                print("Sending notification")
                object = Map.objects.get(id=view_id)
                object.save()
                new_state = object.draw()
                write_variable_size(self.sock, new_state)


class Replies(Thread):

    def __init__(self, sock, username: str, repo: Repo):
        super().__init__()
        self.sock = sock
        self.username: str = username
        self.repo: Repo = repo

    def run_command(self, decoded_input: dict) -> str:
        if "id" in decoded_input:
            id = decoded_input["id"]
            type = Object
            if "type" in decoded_input:
                type = {
                    "component": Component,
                    "map": Map,
                    "car": Car
                }[decoded_input["type"]]
            object = type.objects.get(id=id)
            object.save()
            if type is Component:
                object = type_to_class[object.type].objects.get(id=id)
                object.save()
        elif "component_factory" in decoded_input:
            object = self.repo.components
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


def agent(connection: ServerConnection):
    peer = connection.remote_address
    print("Connected by", peer)

    username = connection.recv()

    try:
        while True:
            input = connection.recv()
            # you can reply by connection.send(str)
    except ConnectionClosedOK:
        # peaceful termination
        pass
    except ConnectionClosedError:
        # client generated an error
        pass

    connection.close()


def main() -> None:
    if len(argv) != 3:
        print("usage: ", argv[0], "--port", "[PORT]")
        exit(-1)

    HOST = ""
    PORT = int(argv[2])

    repo = Repo()
    repo.components.register("car", Car)
    repo.components.register("diagonal", Diagonal)
    repo.components.register("straight", Straight)
    repo.components.register("turn90", Turn90)
    repo.components.register("booster", Booster)
    repo.components.register("fuel", Fuel)
    repo.components.register("rock", Rock)

    server = serve(agent, HOST, PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
