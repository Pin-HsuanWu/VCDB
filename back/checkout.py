# description
    # 1. new == False: 
        # delete old sql file from the user's dir, dump newbranch's schema to user dir, update user table
    # 2. new == True: 
        # delete old sql file from the user's dir, update user table
        # since creating new branch does not require a commit, we don't update branch table


# import packages
import os


# function
def checkout(vc_cursor, newBranchName, new=False):
    print("start checking out.")
    try:
        if new == False:
            # error check: whether the specified branch name exists in the branchname list
            query = "SELECT name FROM vcdb.branch;"
            vc_cursor.execute(query)
            allBranchNames = vc_cursor.fetchall()
            allBranchNames = [ "%s" % x for x in allBranchNames]
            if newBranchName not in allBranchNames:
                return "The specified branch name does not exists."

            # dump newbranch's schema to user dir
                # first we import newBranchName schema, then we export it to user's desktop folder named "sql"
            fd = open(f"../branch_tail_schema/{newBranchName}.sql", 'r')
            newBranchSchemaFile = fd.read()
            with open(f"{desktopPath}/sql/{newBranchName}.sql", 'w') as f:
                f.write(newBranchSchemaFile)
        
        else:
            # error check: whether the specified branch name exists in the branchname list
            query = "SELECT name FROM vcdb.branch;"
            vc_cursor.execute(query)
            allBranchNames = vc_cursor.fetchall()
            allBranchNames = [ "%s" % x for x in allBranchNames]
            if newBranchName in allBranchNames:
                return "Please create a branch name that is not identical to the existing ones."


        # delete old sql file from the user's dir 
            # first get current user's branchname
            # we assume user put their sql file in their desktop folder named "sql"
        global userid
        query = "SELECT current_branch FROM vcdb.user where uid = %s;"
        vc_cursor.execute(query, userid)
        branchName = vc_cursor.fetchone()[0]
        desktopPath = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        os.remove(f"{desktopPath}/sql/{branchName}.sql")

        # update user table
        query = "UPDATE user SET current_branch = (%s) WHERE uid = %s;"
        vc_cursor.execute(query, [newBranchName, userid])

        # print success message
        return "Successfully checked out to branch {newBranchName}."


    except Exception as e:
        print(e)