# from dotenv import load_dotenv
# import os
# import sqlalchemy as db
# from sqlalchemy import create_engine
# from sqlalchemy_utils import create_database, database_exists
# from sqlalchemy import Table, Column, Integer, String, MetaData, inspect
# import pymysql
# pymysql.install_as_MySQLdb()
# load_dotenv()


# def create(user, pwd, host, port, database_name):
#     # user = os.getenv('MYSQL_USER')
#     # pwd = os.getenv('MYSQL_PASSWORD')
#     # host = '127.0.0.1'
#     # port = '3307'
#     # dbname = os.getenv('MYSQL_DATABASE')
#     conn_str = 'mysql://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8'.format(
#         user=user,
#         pwd=pwd,
#         host=host,
#         port=port,
#         dbname=database_name
#     )

#     try:
#         engine = create_engine(conn_str)
#         if not database_exists(engine.url):
#             create_database(engine.url)

#         meta = MetaData()
#         commit = Table(
#             'commit', meta,
#             Column('cid', Integer, primary_key=True),
#             Column('version', String(25)),
#             Column('last_version', String(125)),
#             Column('upgrade', String(125)),
#             Column('downgrade', String(125)),
#             Column('msg', String(12)),
#         )

#         user = Table(
#             'user', meta,
#             Column('uid', String(125), primary_key=True),
#             Column('name', String(125)),
#             Column('email', String(125)),
#             Column('current_version', String(25)),
#             Column('current_branch', String(25))
#         )

#         merge = Table(
#             'merge', meta,
#             Column('mid', Integer, primary_key=True),
#             Column('version', String(25)),
#             Column('merge_from', String(25))
#         )

#         branch = Table(
#             'branch', meta,
#             Column('bid', Integer, primary_key=True),
#             Column('name', String(25)),
#             Column('head', String(25))
#         )

#         with engine.connect() as conn:
#             meta.create_all(engine)


#     except Exception as e:
#         print(e)


# if __name__ == '__main__':
#     create()


import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

def create(user, pwd, host, port):
    try:
        # connect to vcdb ip address 127.0.0.1 & port 3306 (currently using local, then switch to remote computer)
        connection1 = mysql.connector.connect(
            user=user, password=pwd, database="vcdb", host=host, port=port)

        vc_cursor = connection1.cursor()
        # vc_cursor.execute("CREATE DATABASE vcdb;")

        # creating tables for vcdb: branch, commit, user, merge
        creating_table = '''CREATE TABLE branch(
            bid int not null AUTO_INCREMENT,
            name varchar(125) not null,
            tail varchar(500),
            PRIMARY KEY (bid));'''
        vc_cursor.execute(creating_table)
        connection1.commit()


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
        connection1.commit()


        creating_table = '''CREATE TABLE user(
            uid varchar(500) not null,
            name varchar(125) not null,
            email varchar(125) not null,
            current_version varchar(500),
            current_bid int not null,
            PRIMARY KEY (uid),
            CONSTRAINT FK_UserCommit FOREIGN KEY (current_version)
            REFERENCES commit(version),
            CONSTRAINT FK_UserBranch FOREIGN KEY (current_bid)
            REFERENCES branch(bid));'''
        vc_cursor.execute(creating_table)
        connection1.commit()


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
        connection1.commit()

        vc_cursor.execute('show tables;')
        vc_alltables = vc_cursor.fetchall()
        print(vc_alltables)
        print("Successfully created vcdb & tables.")
    
    except Exception as e:
        print("error occurs when creating vcdb:")
        print(e)