from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

name = input("name : ")
price = input("price : ")
image_url = input("image url : ")
description = input("description : ")

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)
    
cursor = db.cursor()

sql = "INSERT INTO products(name, price, image_url, description) VALUES (%s, %s, %s, %s)"
values =(name, price, image_url, description)

cursor.execute(sql, values)

try:
    db.commit()
except mysql.connector.Error as err:
    print("error : ", err)
finally:
    db.close()
    print("Database connection closed")
