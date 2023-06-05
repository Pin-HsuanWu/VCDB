import mysql.connector

connection1 = mysql.connector.connect(
    user="myuser", password="mypassword", host='127.0.0.1', port="3306", database='vcdb')  
print("DB connected.")
vc_cursor = connection1.cursor()


connection2 = mysql.connector.connect(
    user="myuser", password="mypassword", host='127.0.0.1', port="3306", database='userdb')  
user_cursor = connection2.cursor()


# creating tables for vcdb
creating_table = '''CREATE TABLE branch(
    bid int not null AUTO_INCREMENT,
    name varchar(125) NOT NULL,
    tail varchar(500) not null,
    PRIMARY KEY (`bid`));'''
vc_cursor.execute(creating_table)
connection1.commit()


creating_table = '''CREATE TABLE commit(
    version varchar(500) not null,
    branch varchar(500) not null,
    last_version varchar(500),
    upgrade varchar(5000) not null,
    downgrade varchar(5000) not null,
    time varchar(500) not null,
    user_id varchar(500) not null,
    msg varchar(500),
    PRIMARY KEY (`version`)
)'''
vc_cursor.execute(creating_table)
connection1.commit()


creating_table = '''CREATE TABLE user(
    uid varchar(500) not null,
    name varchar(125) not null,
    email varchar(125) not null,
    current_version varchar(500) not null,
    current_branch varchar(500) not null,
    PRIMARY KEY (`uid`)
)'''
vc_cursor.execute(creating_table)
connection1.commit()


creating_table = '''CREATE TABLE merge(
    merge_version varchar(500) not null,
    main_branch_version varchar(500) not null,
    target_branch_version varchar(500) not null,
    PRIMARY KEY (`mid`)
);'''
vc_cursor.execute(creating_table)
connection1.commit()


vc_cursor.execute('show tables;')
vc_alltables = vc_cursor.fetchall()
print(vc_alltables)


