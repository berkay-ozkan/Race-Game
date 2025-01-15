from django import setup
from json import dumps, loads
from os import environ
from subprocess import Popen, PIPE
from sys import argv, exit, path
from threading import Thread
from websockets.sync.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedOK

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


class Notifications(Thread):

    def __init__(self, connection: ServerConnection, username: str,
                 observer: Observer) -> None:
        super().__init__()
        self.connection: ServerConnection = connection
        self.username: str = username
        self.observer: Observer = observer

    def run(self):
        while True:
            view_id = self.observer.wait(self.username)

            if view_id is not None:
                print("Sending notification")
                object = Map.objects.get(id=view_id)
                object.save()
                new_state = object.draw()
                self.connection.send(new_state)


class Replies:

    def __init__(self, connection: ServerConnection, username: str,
                 repo: Repo) -> None:
        self.connection: ServerConnection = connection
        self.username: str = username
        self.repo: Repo = repo

    def run_command(self, decoded_input: dict) -> str:
        try:
            object: Repo | ComponentFactory | Object
            if "id" in decoded_input:
                id = decoded_input["id"]
                type = Object
                if "type" in decoded_input:
                    type = {
                        "component": Component,
                        "map": Map,
                        "view": Map.View,
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
                return result
            return "Command executed"
        except Exception as exception:
            return str(exception)

    def run(self):
        try:
            while True:
                encoded_input = self.connection.recv()
                input = loads(encoded_input)
                result = self.run_command(input)
                self.connection.send(
                    dumps({
                        "command": {
                            "type": input.get("type"),
                            "function_name": input["function_name"]
                        },
                        "result": result
                    }))
        except ConnectionClosedOK:
            pass

        print(self.username, "closed the connection.")
        self.connection.close()

    @staticmethod
    def is_internal(function_name: str) -> bool:
        if function_name.startswith("__") and function_name.endswith("__"):
            return False
        return function_name.startswith('_')


class Agent:

    def __init__(self, observer: Observer, repo: Repo) -> None:
        self.observer: Observer = observer
        self.repo: Repo = repo

    def handle(self, connection: ServerConnection) -> None:
        peer = connection.remote_address
        print("Connected by", peer)

        username = "Placeholder"

        Replies(connection, username, self.repo).run()


def main() -> None:
    if len(argv) != 3:
        print("usage: ", argv[0], "--port", "[PORT]")
        exit(-1)

    HOST = ""
    PORT = int(argv[2])

    observer = Observer()
    repo = Repo()

    repo.components.register("car", Car)
    repo.components.register("diagonal", Diagonal)
    repo.components.register("straight", Straight)
    repo.components.register("turn90", Turn90)
    repo.components.register("booster", Booster)
    repo.components.register("fuel", Fuel)
    repo.components.register("rock", Rock)

    agent = Agent(observer, repo)
    with serve(agent.handle, HOST, PORT) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
