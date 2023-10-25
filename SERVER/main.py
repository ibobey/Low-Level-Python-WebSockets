import os

from dotenv import load_dotenv
from os import getenv


load_dotenv(".env")

data = os.getenv("PORT", 55000)

print(int(data))