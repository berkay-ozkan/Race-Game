from threading import Thread
import socket_helpers
from socket import socket, AF_INET, SOCK_STREAM
from repo import Repo


class ClientServer(Thread):
    def __init__(self, connection, address, repo):
        super().__init__()
        self.connection = connection
        self.address = address
        self.repo = repo

    def run(self):
        try:
            while True:
                message = socket_helpers.read_variable_size(self.connection)
                message = message.decode()
                message_parts_list = message.split()
                command = message_parts_list[0]
                args = message_parts_list[1 :]
                response = socket_helpers.command_handler(command, args, self.repo, "")
                socket_helpers.write_variable_size(self.connection, response)

        except Exception as e:
            print(f'Error occured with the client {self.address}: {e}')
        finally:
            self.connection.close()
            print(f'Connection to the address {self.address} is clised')



def start_server(host, port):
    repo = Repo() 
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server started on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            print(f'connected by {addr}')
            handler = ClientServer(conn, addr, repo)
            handler.start()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3 or sys.argv[1] != "--port":
        print("Usage: python server.py --port <PORT>")
        sys.exit(1)

    HOST = "0.0.0.0"
    PORT = int(sys.argv[2])
    start_server(HOST, PORT)