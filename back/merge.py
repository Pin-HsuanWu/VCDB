# this function is for 2 branch merges
import mysql.connector
import uuid
import datetime

def merge(mainBranchName, targetBranchName):
    # Read sql file by dump.py, then translate to json by diff.py
    # assume each branch's tail schema is stored in the following file name: {branchName}.sql
    file1 = open(f"./latestSchema/{mainBranchName}.sql", 'r')
    mainSchema = file1.read()
    file2 = open(f"./latestSchema/{targetBranchName}.sql", 'r')
    targetSchema = file2.read()

    # check if 2 branch exists
    query = "SELECT name FROM branch;"
    cursor.execute(query)
    allBranchNames = cursor.fetchall()
    flag1, flag2 = False
    if mainBranchName in allBranchNames:
        flag1 = True
    if targetBranchName in allBranchNames:
        flag2 = True
    if flag1 & flag2 == False:
        print("Cannot merge branches that does not exist.")

    # if conflict exists: show conflicts
    checkConflict = generate_sql_diff(parse_sql_script(mainSchema), parse_sql_script(targetSchema))
    if checkConflict != 0:
        print("Schema conflict exists between 2 branches as follows:")
        print(checkConflict)
    
    # if conflict doesn't exist
        # update commit table: target merged into main.
    else:
        downgrade = generate_sql_diff(parse_sql_script(mainSchema), parse_sql_script(targetSchema))
        upgrade = generate_sql_diff(parse_sql_script(targetSchema), parse_sql_script(mainSchema))
        msg = f"Merge {targetBranchName} into {mainBranchName}"
        version = str(uuid.uuid4()) 
        query = "SELECT * FROM branch WHERE bid = 'branchID'"
        cursor.execute(query)
        branchInfo = cursor.fetchall()
        last_version = branchInfo[2]
        query = f"SELECT * FROM branch WHERE name = '{mainBranchName}'"
        cursor.execute(query)
        branchInfo = cursor.fetchall()
        branchID = branchInfo[0]
        now = datetime.datetime.now()
        insert = "INSERT INTO commit (cid, version, last_version, branch, upgrade, downgrade, time, msg) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)"
        val = (version, last_version, branchID, upgrade, downgrade, now.strftime("%Y%m%d_%H%M"), msg)
        cursor.execute(insert, val)

        # update branch table
        update = f"UPDATE branch SET tail = (%s) WHERE bid = {branchID};"
        val = version
        cursor.execute(update, val)

        print(f"Successfully merged {targetBranchName} into {mainBranchName}!")
    return

if __name__ == '__main__':
    merge(func1, func2)
    


