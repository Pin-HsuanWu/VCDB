import mysql.connector

# first we declare that we will need these global vars in all other files
def globalvarinit():
    global userdb_name
    global db_connect
    global db_cursor
    global current_version
    global current_branch
    global connection1
    global connection2
    global vc_cursor
    global user_cursor

    userdb_name = None
    global db_connect
    global db_cursor
    global current_version
    global current_branch
    global connection1
    global connection2
    global vc_cursor
    global user_cursor

    # connection1 = mysql.connector.connect(
    # user="myuser", password="mypassword", host='127.0.0.1', port="3306", database='vcdb')
    # print("VCDB connected.")
    # vc_cursor = connection1.cursor()



globalvarinit()
print(userdb_name)

# get user db infos from GUI.py's init_database()
db_user, pwd, host, port
