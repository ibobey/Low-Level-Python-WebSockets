import os
from Server import *
from dotenv import load_dotenv
from os import getenv


if __name__ == "__main__":
    server = Server()
    server.run_server()
    server.receive()

