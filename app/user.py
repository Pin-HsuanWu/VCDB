import mysql.connector
from create import create

def init(user, pwd, host, port, database_name):

    # set DB connection
    global db_connect
    global db_cursor
    try:
        db_connect = mysql.connector.connect(host=host, user=user, passwd=pwd)
        db_cursor = db_connect.cursor()

        # create DBVC
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS " + database_name)
        db_cursor.execute("USE " + database_name)

        # create table in DBVC
        create(user, pwd, host, port, database_name)

        print("Im init")

        return db_connect, db_cursor
    
    except Exception as e:
        print(e)
        print("Im init")
        return None
    
    

def register(db_connect, db_cursor, database_name, user_name, user_email):

    # create uuid
    import uuid
    user_uuid = uuid.uuid4

    #Update user table
    db_cursor.execute("USE " + database_name)
    db_cursor.execute(f"INSERT INTO user (uid, name, email) VALUES ('{user_uuid}', '{user_name}', '{user_email}')")
    db_connect.commit()

def login(db_cursor, database_name, user_name, user_email):

    #set current_version and brench
    global current_version
    global current_branch

    #get user's version and branch
    try:
        db_cursor.execute("USE " + database_name)
        db_cursor.execute(f"select current_version, current_branch from user where name = '{user_name}' AND email = '{user_email}'")
        result = db_cursor.fetchone()
        current_version, current_branch = result
        return current_version, current_branch

    except Exception as e:
        print(e)
        return None