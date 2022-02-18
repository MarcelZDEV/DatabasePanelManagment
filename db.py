import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="dbpm",
    port="3306"
)

cursor = db.cursor()
