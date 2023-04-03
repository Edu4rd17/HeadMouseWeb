import mysql.connector
import datetime
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('LOCALHOST'),
    user=os.getenv('LOCALHOST_USER'),
    password=os.getenv('LOCALHOST_PASS'),
    database=os.getenv('DB_NAME')
)

mycursor = mydb.cursor()

# empty the database before adding new users
mycursor.execute("DELETE FROM user")

sql = "INSERT INTO user (email, password, firstName, lastName, country, gender, registrationDate, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

# hash the user password before adding it to the database
password = "1111111"
hashed_password = generate_password_hash(password, method='sha256')


val = [
    ('admin@headmouseweb.com', hashed_password, 'Admin', 'Admin',
     'Ireland', 'Male', datetime.datetime.now(), 1),
    ('eduard2001@gmail.com', hashed_password, 'Eduard', 'Iacob',
     'Romania', 'Male', datetime.datetime.now(), 0),
    ('johnny@gmail.com', hashed_password, 'John', 'Smith',
     'USA', 'Male', datetime.datetime.now(), 0)
]

mycursor.executemany(sql, val)
mydb.commit()

print(mycursor.rowcount, "record was inserted.")
