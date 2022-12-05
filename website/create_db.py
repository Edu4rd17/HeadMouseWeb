import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host= os.getenv('LOCALHOST'),
    user="root",
    password="Database2001",
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE headmouseweb")

