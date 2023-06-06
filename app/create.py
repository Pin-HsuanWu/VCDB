import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

def create(user, pwd, host, port):
    try:
        # connect to vcdb ip address 127.0.0.1 & port 3306 (currently using local, then switch to remote computer)
        vc_connect = mysql.connector.connect(
            user=user, password=pwd, database="vcdb", host=host, port=port)

        vc_cursor = vc_connect.cursor()
        # vc_cursor.execute("CREATE DATABASE vcdb;")

        # creating tables for vcdb: branch, commit, user, merge
        creating_table = '''CREATE TABLE branch(
            bid int not null AUTO_INCREMENT,
            name varchar(125) not null,
            tail varchar(500),
            PRIMARY KEY (bid));'''
        vc_cursor.execute(creating_table)
        vc_connect.commit()


        creating_table = '''CREATE TABLE commit(
            version varchar(500) not null,
            bid int not null,
            last_version varchar(500),
            upgrade varchar(5000) not null,
            downgrade varchar(5000) not null,
            time datetime not null,
            uid varchar(500) not null,
            msg varchar(500),
            PRIMARY KEY (version));'''
        vc_cursor.execute(creating_table)
        vc_connect.commit()


        creating_table = '''CREATE TABLE user(
            uid varchar(500) not null,
            name varchar(125) not null,
            email varchar(125) not null,
            current_version varchar(500),
            current_bid int not null,
            PRIMARY KEY (uid),
            CONSTRAINT FK_UserBranch FOREIGN KEY (current_bid)
            REFERENCES branch(bid));'''
        vc_cursor.execute(creating_table)
        vc_connect.commit()


        creating_table = '''CREATE TABLE merge(
            merged_version varchar(500) not null,
            main_branch_version varchar(500) not null,
            target_branch_version varchar(500) not null,
            PRIMARY KEY (merged_version),
            CONSTRAINT FK_MergeCommit1 FOREIGN KEY (merged_version)
            REFERENCES commit(version),
            CONSTRAINT FK_MergeCommit2 FOREIGN KEY (main_branch_version)
            REFERENCES commit(version),
            CONSTRAINT FK_MergeCommit3 FOREIGN KEY (target_branch_version)
            REFERENCES commit(version));'''
        vc_cursor.execute(creating_table)
        vc_connect.commit()

        vc_cursor.execute('show tables;')
        vc_alltables = vc_cursor.fetchall()
        print(vc_alltables)
        print("Successfully created vcdb & tables.")
    
    except Exception as e:
        print("error occurs when creating vcdb:")
        print(e)