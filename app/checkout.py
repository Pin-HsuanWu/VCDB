# description
# 1. new == False:
#     update user table
#     check if tail == current schema
#     if not: warn, exit
#     directly change userdb's schema: drop + create
# 2. new == True:
#     update user table
#     since creating new branch does not require a commit, we don't update branch table

import os
import mysql.connector
from dump import dump
from diff import *
import globals



# function
# def checkout(newBranchName, new=False):
#     print(globals.database_name)

#     print("start checking out.")
#     connection1 = mysql.connector.connect(
#         user="myuser", password="mypassword", host='127.0.0.1', port="3306", database='vcdb')
#     print("VCDB connected.")
#     vc_cursor = connection1.cursor()

#     connection2 = mysql.connector.connect(
#     user="myuser", password="mypassword", host='127.0.0.1', port="3306", database='userdb')
#     print("user DB connected.")
#     user_cursor = connection2.cursor()

#     # get user's current branch name.
#     # assume userid is global variable

#     query = "SELECT current_branch FROM vcdb.user where uid = %s;"
#     vc_cursor.execute(query, [current_uid])
#     currentBranchName = vc_cursor.fetchone()[0]
    
#     try:
#         if new == False:
#             # error check: whether the specified branch name exists in the branchname list
#             query = "SELECT name FROM vcdb.branch;"
#             vc_cursor.execute(query)
#             allBranchNames = vc_cursor.fetchall()
#             allBranchNames = ["%s" % x for x in allBranchNames]
#             if newBranchName not in allBranchNames:
#                 print("The specified branch name does not exists.")
#                 return

#             # check if tail == current schema
#             # dump current userdb's schema
#             dump.dump(user_cursor)
#             # check differences
#             userCurrentSchema = diff.read_sql_file(f"./tmpfile.sql")
#             currentBranchTail = diff.read_sql_file(f"./branch_tail_schema/{currentBranchName}.sql")
#             result = diff.get_diff(currentBranchTail, userCurrentSchema)
#             if result != "":
#                 print("Please commit before checking out to another branch.")
#                 return
#             # directly change userdb's schema: drop whole schema + import newBranch schema to it
#             query = 'drop schema userdb;'
#             user_cursor.execute(query)
#             targetBranchTailCommands = diff.read_sql_file(f"./branch_tail_schema/{newBranchName}.sql")
#             user_cursor.execute("create database userdb;")
#             user_cursor.execute("use userdb;")
#             for statement in targetBranchTailCommands.split(';'):
#                 if len(statement.strip()) > 0:
#                     user_cursor.execute(statement + ';')
#             # update user table: current_branch, current_version
#             # if checking out to an existing branch, the user will be on the latest commit of the target branch
#             query = "SELECT tail FROM vcdb.branch where name = %s;"
#             vc_cursor.execute(query, [newBranchName])
#             newBranchTail = vc_cursor.fetchone()[0]
#             vc_cursor.execute("use vcdb;")
#             query = "UPDATE user SET current_branch=%s, current_version=%s WHERE uid = %s;"
#             vc_cursor.execute(query, [newBranchName, newBranchTail, "testtt"])
#             connection1.commit()
#             # delete tmpfile.sql
#             os.remove("tmpfile.sql")

#         else:
#             # error check: whether the specified branch name exists in the branchname list
#             query = "SELECT name FROM vcdb.branch;"
#             vc_cursor.execute(query)
#             allBranchNames = vc_cursor.fetchall()
#             allBranchNames = ["%s" % x for x in allBranchNames]
#             if newBranchName in allBranchNames:
#                 print("Please create a branch name that is not identical to the existing ones.")
#                 return

#             # update branch table
#             vc_cursor.execute("use vcdb;")       
#             query = "insert into `branch` (name, tail) values(%s, %s);"
#             vc_cursor.execute(query, [newBranchName, " "])
#             connection1.commit()


#         #update user table: current_branch, current_version
#         vc_cursor.execute("use vcdb;")
#         query = "UPDATE user SET current_branch = %s WHERE uid = %s;"
#         vc_cursor.execute(query, [newBranchName, "testtt"])
#         connection1.commit()
#         query = "UPDATE `user` SET current_branch = %s WHERE uid = %s;"
#         vc_cursor.execute(query, [newBranchName, "testtt"])
#         connection1.commit()


#         #print success message
#         print(f"Successfully checked out to branch {newBranchName}.")
#         connection1.close()
#         connection2.close()
#         return

#     except Exception as e:
#         print(e)


# checkout("func2", False)
