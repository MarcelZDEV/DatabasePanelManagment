import mysql.connector
import time

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="dbpm",
    port="3306"
)

cursor = db.cursor(buffered=True)
