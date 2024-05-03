from dotenv import load_dotenv
import os

load_dotenv()

username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASS")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
database_name = os.environ.get("DB_NAME")
