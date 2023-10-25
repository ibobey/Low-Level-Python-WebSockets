import socket
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")

HOST: str = getenv("HOST", socket.gethostbyname(socket.gethostname()))
PORT: int = int(getenv("PORT", 55000))
ADDR: tuple[str, int] = (HOST, PORT)
BUFFER_SIZE: int = int(getenv("BUFFER_SIZE", 1024))
FORMAT: str = getenv("FORMAT", 'utf-8')

