import mysql.connector
import init

# 服務user的function. user執行checkout, 就會直接更換本地端的total schema.


def checkout(newBranch, b=None):
    # if checking out to an existing branch
    if b == None:
        # check if the specified branch name exists in the branchname list
        query = "SELECT name FROM branch;"
        cursor.execute(query)
        allBranchNames = cursor.fetchall()
        if newBranch not in allBranchNames:
            print("The specified branch name does not exists.")
            return
        updateUserQuery = "update user set current_branch = (%s);"
        cursor.execute(updateUserQuery, newBranch)

    else:
        # check if the specified branch name does not exist in the branchname list
        query = "SELECT name FROM branch;"
        cursor.execute(query)
        allBranchNames = cursor.fetchall()
        if newBranch in allBranchNames:
            print("Please create a branch name that is not identical to the existing ones.")
            return
        insertBranchQuery = "insert into branch (name) values (%s);"
        cursor.execute(insertBranchQuery, newBranch)
        updateUserQuery = "update user set current_branch = (%s);"
        cursor.execute(updateUserQuery, newBranch)

    # print success message
    print(f"Checked out to branch {newBranch}.")
    return 


if __name__ == '__main__':
    newBranch = 'new_function'
    checkout(newBranch)