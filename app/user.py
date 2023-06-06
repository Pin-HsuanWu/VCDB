import mysql.connector
import create

def init(user, pwd, host, port, database_name):

    # set DB connection
    global vc_connect
    global vc_cursor
    global user_connect
    global user_cursor
    try:
        user_connect = mysql.connector.connect(host=host, database=database_name, user=user, passwd=pwd)
        user_cursor = user_connect.cursor()

        # create vcdb
        user_cursor.execute("CREATE DATABASE IF NOT EXISTS vcdb")
        user_connect.commit()
        # create table in DBVC
        create.create(user, pwd, host, port)
        vc_connect  = mysql.connector.connect(host=host, database="vcdb", user=user, passwd=pwd)
        vc_cursor = vc_connect.cursor()
        vc_cursor.execute("USE vcdb")
        vc_cursor.execute(f"INSERT INTO branch (name) VALUES ('main')")
        vc_connect.commit()

        print("Im init")

        return vc_connect, vc_cursor, user_connect, user_cursor
    
    except Exception as e:
        print(e)
        print("Im init")
        return None
    
    

def register(vc_connect, vc_cursor, user_name, user_email):

    global current_bid
    # create uuid
    import uuid
    user_uuid = str(uuid.uuid4())

    #Update user table
    vc_cursor.execute("USE vcdb")
    vc_cursor.execute(f"INSERT INTO user (uid, name, email, current_bid) VALUES ('{user_uuid}', '{user_name}', '{user_email}', '1')")
    vc_connect.commit()
    vc_cursor.execute(f"select bid from branch where name = 'main'")
    result = vc_cursor.fetchone()
    current_bid = result
    return current_bid

def login(user, pwd, host,  database_name, user_name, user_email):
    # set DB connection
    global vc_connect
    global vc_cursor
    global user_connect
    global user_cursor

    #set current_version and brench
    global current_uid
    global current_version
    global current_bid

    #get user's version and branch
    try:
        user_connect = mysql.connector.connect(host=host, database=database_name, user=user, passwd=pwd)
        user_cursor = user_connect.cursor()

        # create vcdb
        vc_connect  = mysql.connector.connect(host=host, database="vcdb", user=user, passwd=pwd)
        vc_cursor = vc_connect.cursor()
        vc_cursor.execute("USE vcdb")
        vc_cursor.execute(f"select uid, current_version, current_bid from user where name = '{user_name}' AND email = '{user_email}'")
        result = vc_cursor.fetchone()
        current_uid, current_version, current_bid = result
        # db_cursor.execute(f"select bid from branch where name = '{user_name}' AND email = '{user_email}'")

        return vc_connect, vc_cursor, user_connect, user_cursor, current_uid, current_version, current_bid

    except Exception as e:
        print(e)
        return None