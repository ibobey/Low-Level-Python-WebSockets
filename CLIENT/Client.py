from threading import Thread
from socket import AF_INET, SOCK_STREAM
from socket import socket
from dotenv import load_dotenv
from os import getenv
import socket

load_dotenv(".env")

HOST: str = getenv("HOST", socket.gethostbyname(socket.gethostname()))
PORT: int = int(getenv("PORT", 55000))
ADDR: tuple[str, int] = (HOST, PORT)
BUFFER_SIZE: int = int(getenv("BUFFER_SIZE", 1024))
FORMAT: str = getenv("FORMAT", 'utf-8')


class ConnectServer:
    __server: socket

    def __init__(self):
        pass

    def connect_server(self):
        self.__server = socket.socket(AF_INET, SOCK_STREAM)
        self.__server.connect(ADDR)
        receive_thread = Thread(target=self.__receive_server)
        text_thread = Thread(target=self.__text_message)
        receive_thread.start()
        text_thread.start()

    def __receive_server(self):
        signal = True
        while signal:
            try:
                message: str = self.__server.recv(BUFFER_SIZE).decode(FORMAT)
                print(message)

            except Exception as E:
                print("[SERVER ERROR!]")
                self.__server.close()
                signal = False

    def __text_message(self):
        while True:
            message: str = input(f"Text: ")
            self.__server.send(message.encode(FORMAT))



