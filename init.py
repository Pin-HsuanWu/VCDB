# description
    # run create.py to create VCDB
    # create global variables: VCDB connection



# import packages
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
import back.checkout as checkout2


connection1 = mysql.connector.connect(
    user="myuser", password="mypassword", host='mysql', port="3306", database='vcdb')  
print("DB connected.")
vc_cursor = connection1.cursor()
vc_cursor.execute('show tables;')
students = vc_cursor.fetchall()
print(students)


connection2 = mysql.connector.connect(
    user="myuser", password="mypassword", host='mysql', port="3306", database='userdb')  
user_cursor = connection2.cursor()
user_cursor.execute('show tables;')
alls = user_cursor.fetchall()
print(alls)


