# Hop: select current branch's all versions except user's version
# Checkout: if "NO" -> select all branchs except user's branch
# Merge: select all branchs except user's branch

import globals

def getAllBranchExceptCurrent():
    query = "select current_bid from vcdb.user where uid = %s;"
    globals.vc_cursor.execute(query, [globals.current_uid])
    result = globals.vc_cursor.fetchone()[0]
    current_bid = result

    # current branch name
    query = f"select name from {globals.vcdb_name}.branch where bid = %s;"
    globals.vc_cursor.execute(query, [current_bid])
    result = globals.vc_cursor.fetchone()[0]
    current_bname = result


    # select all branches and store them in a list
    query = f"select name from {globals.vcdb_name}.branch;"
    globals.vc_cursor.execute(query)
    allbranches = globals.vc_cursor.fetchall()
    allbranches = [x[0] for x in allbranches if x[0] != current_bname]
    
    return allbranches


def getCurrentBranchAllVersionsExceptCurrent():
    query = f"select current_bid, current_version from {globals.vcdb_name}.user where uid = %s;"
    globals.vc_cursor.execute(query, [globals.current_uid])
    result = globals.vc_cursor.fetchall()[0]
    current_bid = result[0]
    current_version = result[1]

    # get current branch all versions, sort allVersions by datetime
    query = f"select version from {globals.vcdb_name}.commit where bid = %s;"
    globals.vc_cursor.execute(query, [current_bid])
    allVersions = globals.vc_cursor.fetchall()
    allVersions = sorted([x[0] for x in allVersions if x[0] != current_version])

    return allVersions