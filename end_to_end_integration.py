from django.http import HttpRequest
from websockets.sync.client import connect

HOST = "localhost"
PORT = 12345


def write_to_backend(request: HttpRequest, command: str) -> str:
    with connect(f"ws://{HOST}:{PORT}") as websocket:
        websocket.send(command)
        reply: str = websocket.recv()
        return reply
