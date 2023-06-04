from diff import read_sql_file ,parse_sql_script

# Read sql file for two branch tail
commit1 = read_sql_file("testcase/test1.sql")
commit2 = read_sql_file("testcase/test2.sql")

# Parse sql scripts into dictionary
commit1_dict = parse_sql_script(commit1)
commit2_dict = parse_sql_script(commit2)

# Check if there is any conflict
def check_conflict(commit1_dict,commit2_dict):
    all_tables = set(commit1_dict.keys()).union(commit2_dict.keys())
    constraint_keywords = {'PRIMARY KEY', 'CONSTRAINT_FOREIGN KEY', 'CONSTRAINT_CHECK', 'UNIQUE KEY'}
    
    for table_name in all_tables:
        if table_name not in commit1_dict:
            # Table only in commit 2
            pass
        elif table_name not in commit2_dict:
            # Table only in commit 1
            pass
        else:
            # Table name in both commits
            pass




    # Check if there is any missing dependency (FK constraint)

# Merge if there is no conflict

# Show conflict if there is any



# this function is for 2 branch merges
import mysql.connector
import uuid
import datetime
import diff
import time


def merge(mainBranchName, targetBranchName):
    # Read sql file by dump.py, then translate to json by diff.py
    # assume each branch's tail schema is stored in the following file name: {branchName}.sql
    file1 = open(f"./branch_tail_schema/{mainBranchName}.sql", 'r')
    mainSchema = file1.read()
    file2 = open(f"./branch_tail_schema/{targetBranchName}.sql", 'r')
    targetSchema = file2.read()

    file1.close()
    file2.close()

    # check if 2 branch exists
    query = "SELECT name FROM branch;"
    cursor.execute(query)
    allBranchNames = cursor.fetchall()
    allBranchNames = ["%s" % x for x in allBranchNames]
    flag1, flag2 = False
    if mainBranchName in allBranchNames:
        flag1 = True
    if targetBranchName in allBranchNames:
        flag2 = True
    if flag1 & flag2 == False:
        print("Cannot merge branches that does not exist.")

    # if conflict exists: show conflicts
    checkConflict = diff.showConflict(mainSchema, targetSchema)
    if checkConflict == 1:
        print("Schema conflict exists between 2 branches as follows:")
        print(checkConflict)
    
    # if conflict doesn't exist
        # update commit table: target merged into main.
    else:
        downgrade = diff.get_diff(mainSchema, targetSchema)
        upgrade = diff.get_diff(targetSchema, mainSchema)
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
        unixtime = time.mktime(now.timetuple())
        insert = "INSERT INTO commit (cid, version, last_version, branch, upgrade, downgrade, time, msg) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)"
        val = (version, last_version, branchID, upgrade, downgrade, unixtime, msg)
        cursor.execute(insert, val)

        # update branch table
        update = f"UPDATE branch SET tail = (%s) WHERE bid = {branchID};"
        val = version
        cursor.execute(update, val)

        print(f"Successfully merged {targetBranchName} into {mainBranchName}!")
    return



if __name__ == '__main__':
    merge("func1", "func2")


