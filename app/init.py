<<<<<<< HEAD
=======
# description


# import packages
>>>>>>> checkout
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
<<<<<<< HEAD


if __name__ == '__main__':
    user = os.getenv('MYSQL_USER')
    pwd = os.getenv('MYSQL_PASSWORD')

    connection1 = mysql.connector.connect(
        user="root", password="mypassword", host='mysql', port="3306", database='vcdb')  
    print("DB connected")
    cursor = connection1.cursor()
    cursor.execute('show tables;')
    students = cursor.fetchall()
    print(students)

    connection2 = mysql.connector.connect(
        user="root", password="mypassword", host='mysql', port="3306", database='userdb')  #壹定要用root為user to 33062
    cursor = connection2.cursor()
    cursor.execute('show tables;')
    alls = cursor.fetchall()
    print(alls)

    connection1.close()
    connection2.close()
=======
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


>>>>>>> checkout
