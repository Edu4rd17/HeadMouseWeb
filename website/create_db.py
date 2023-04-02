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

# delete database if exists already and create new one

my_cursor.execute("DROP DATABASE IF EXISTS headmouseweb")
my_cursor.execute("CREATE DATABASE headmouseweb")

print("Database created")
