from dotenv import load_dotenv
import os
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import Table, Column, Integer, String, MetaData, inspect
import pymysql
pymysql.install_as_MySQLdb()
load_dotenv()


def create():
    user = os.getenv('MYSQL_USER')
    pwd = os.getenv('MYSQL_PASSWORD')
    host = '127.0.0.1'
    port = '3307'
    dbname = os.getenv('MYSQL_DATABASE')
    conn_str = 'mysql://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8'.format(
        user=user,
        pwd=pwd,
        host=host,
        port=port,
        dbname=dbname
    )

    try:
        engine = create_engine(conn_str)
        if not database_exists(engine.url):
            create_database(engine.url)

        meta = MetaData()
        commit = Table(
            'commit', meta,
            Column('cid', Integer, primary_key=True),
            Column('version', String(25)),
            Column('last_version', String(125)),
            Column('upgrade', String(125)),
            Column('downgrade', String(125)),
            Column('msg', String(12)),
        )

        user = Table(
            'user', meta,
            Column('uid', String(125), primary_key=True),
            Column('name', String(125)),
            Column('email', String(125)),
            Column('current_version', String(25)),
            Column('current_branch', String(25))
        )

        merge = Table(
            'merge', meta,
            Column('mid', Integer, primary_key=True),
            Column('version', String(25)),
            Column('merge_from', String(25))
        )

        branch = Table(
            'branch', meta,
            Column('bid', Integer, primary_key=True),
            Column('name', String(25)),
            Column('head', String(25))
        )

        with engine.connect() as conn:
            meta.create_all(engine)


    except Exception as e:
        print(e)


if __name__ == '__main__':
    create()


