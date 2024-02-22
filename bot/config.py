import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db_host = os.getenv('MY_DB_HOST')
db_port = os.getenv('MY_DB_PORT')
db_user = os.getenv('MY_DB_USER')
db_password = os.getenv('MY_DB_PASSWORD')
db_database = os.getenv('MY_DB_DATABASE')

headers = os.getenv('HEADERS')
cookies = os.getenv('COOKIES')
