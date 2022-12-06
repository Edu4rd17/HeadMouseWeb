import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('LOCALHOST'),
    user=os.getenv('LOCALHOST_USER'),
    password=os.getenv('LOCALHOST_PASS'),
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE headmouseweb")
