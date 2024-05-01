from dotenv import load_dotenv
import os

load_dotenv()

username = os.environ.get("username")
password = os.environ.get("password")
host = os.environ.get("host")
port = os.environ.get("port")
database_name = os.environ.get("database_name")
