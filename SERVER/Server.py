from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR
import socket
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")

HOST: str = getenv("HOST", socket.gethostbyname(socket.gethostname()))
PORT: int = int(getenv("PORT", 55000))
ADDR: tuple[str, int] = (HOST, PORT)
BUFFER_SIZE: int = int(getenv("BUFFER_SIZE", 1024))
FORMAT: str = getenv("FORMAT", 'utf-8')
MAX_CLIENT: int = int(getenv("MAX_CLIENT", 5))


class Server:

    __clients: list
    active_connection: int
    __server: socket
    __signal: bool

    @property
    def SIGNAL(self):
        return self.__signal

    def __init__(self):
        self.__clients = list()
        self.active_connection = 0
        self.__signal = False

    def run_server(self):
        self.__server = socket.socket(AF_INET, SOCK_STREAM)
        self.__server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            self.__server.bind(ADDR)
            self.__server.listen(MAX_CLIENT)
            print("[Server is Running]")
            self.__signal = True
        except Exception as E:
            print(E)

    def __broadcast(self, message: bytes):
        for client in self.__clients:
            client.send(message)

    def receive(self):
        while self.__signal:
            print("[Server have listening ...]")
            client, address = self.__server.accept()
            print(f"[{address} connected to server] ")
            self.__add_client(client=client)
            client.send(f"[Connection Successful]".encode(FORMAT))

            thread_handle_client = Thread(target=self.__handle_client, args=(client,))
            thread_handle_client.start()

    def __handle_client(self, client):
        signal: bool = True
        while signal:
            try:
                message = client.recv(BUFFER_SIZE)
                self.__broadcast(message)

            except Exception as E:
                self.__clients.remove(client)
                client.close()
                self.__broadcast(f"{client} disconnected".encode(FORMAT))
                signal = False

    def __add_client(self, client):
        if client not in self.__clients:
            self.__clients.append(client)


