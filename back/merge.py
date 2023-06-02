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




