from diff import read_sql_file ,parse_sql_script, generate_attribute_string, generate_sql_diff, get_diff
import mysql.connector
import uuid
import datetime
import time

"""
Database setup for test
"""
vcdb_connection = mysql.connector.connect(
    user="root", password="dbcourse", host='127.0.0.1', port="3306", database='vcdb')
print("VCDB connected.")
vc_cursor = vcdb_connection.cursor()

userdb_connection = mysql.connector.connect(
user="root", password="dbcourse", host='127.0.0.1', port="3306", database='userdb')
print("user DB connected.")
user_cursor = userdb_connection.cursor()




# Add branch format for sql script in different branch
def branch_format(branch_list, branch_name):
    if branch_list[0].startswith(", \n"):
        branch_list[0] = branch_list[0][3:]
    
    branch_list.insert(0, f"/* {branch_name} */")
    branch_list.append("/************/\n")
    
    sql_script = '\n'.join(branch_list)
    return sql_script

# Generate attribute string for column definition
def check_table_conflicts(is_conflict, table_name, branch1_name, table1, branch2_name, table2):
    sql_script = ""
    
    conflicts = []
    attribute_str = ""
    nonconflict_attr_dict = {}

    # Change the order of two_tables
    two_tables = set(table1.keys()).union(table2.keys())
    constraint_keywords = ['PRIMARY KEY', 'CONSTRAINT_FOREIGN KEY', 'UNIQUE KEY', 'CONSTRAINT_CHECK']
    
    two_tables_without_keywords = set(table1.keys()).union(table2.keys())
    for keyword in constraint_keywords:
        two_tables_without_keywords.discard(keyword)
    
    two_tables_with_keywords = two_tables.difference(two_tables_without_keywords)
    two_tables_in_order = list(two_tables_without_keywords) + list(two_tables_with_keywords)

    # Check conflicts in column definitions
    for column_name in two_tables_in_order:
        # Column created
        if column_name not in table1:
            nonconflict_attr_dict.update({column_name: table2[column_name]})
        # Column deleted
        elif column_name not in table2:
            is_conflict = True
            attribute_str += branch_format([generate_attribute_string({column_name: table1[column_name]})], branch1_name)
            attribute_str += branch_format([''], branch2_name)
        # Column exists in both tables, check for conflicts
        else:
            # Column updated
            if table1[column_name] != table2[column_name]:
                is_conflict = True
                attribute_str += branch_format([generate_attribute_string({column_name: table1[column_name]})], branch1_name)
                attribute_str += branch_format([generate_attribute_string({column_name: table2[column_name]})], branch2_name)
            # Column remains the same
            else:
                nonconflict_attr_dict.update({column_name: table1[column_name]})
                
    if attribute_str:
        attribute_str = generate_attribute_string(nonconflict_attr_dict) +',\n'+ attribute_str
    else:
        attribute_str = generate_attribute_string(nonconflict_attr_dict)
    sql_script += f"CREATE TABLE `{table_name}` (\n{attribute_str});\n"
    return is_conflict, sql_script


# Check if there in any conflict when merging different branches
def check_branch_conflicts(branch1_name, branch1, branch2_name, branch2):
    is_conflict = False
    sql_script = ""
    all_tables = set(branch1.keys()).union(branch2.keys())
    
    # Check table conflicts
    for table_name in all_tables:
        # Table created
        if table_name not in branch1.keys():
            sql_script += generate_sql_diff({}, {table_name: branch2[table_name]})
            
        # Table deleted
        elif table_name not in branch2.keys():
            sql_script += branch_format([generate_sql_diff({}, {table_name: branch1[table_name]})], branch1_name)
            sql_script += branch_format([''], branch2_name)
            is_conflict = True
        
        # Table updated -> Check conflicts in table definitions
        else:
            if branch1[table_name] == branch2[table_name]:
                sql_script += generate_sql_diff({}, {table_name: branch1[table_name]})
            else:
                table_conflict = check_table_conflicts(is_conflict, table_name, branch1_name, branch1[table_name], branch2_name, branch2[table_name])
                is_conflict = table_conflict[0]
                sql_script += table_conflict[1]
        
    return is_conflict, sql_script


def merge_schema(commit1_dict, commit2_dict):
    merged_schema = {}

    # Merge tables from commit1
    for table_name, schema in commit1_dict.items():
        merged_schema[table_name] = schema

    # Merge tables from commit2
    for table_name, schema in commit2_dict.items():
        if table_name in merged_schema:
            # Table already exists, merge the schema
            merged_schema[table_name].update(schema)
        else:
            # Table doesn't exist, add it to the merged commit
            merged_schema[table_name] = schema

    return merged_schema




def merge(main_branch_name, target_branch_name, current_uid):
    
    # Check if 2 branches exist
    query = "SELECT name, tail FROM branch WHERE name = (%s);"
    vc_cursor.execute(query, (main_branch_name, ))
    main_branch_existed = vc_cursor.fetchall()
    print(main_branch_existed)
    if not main_branch_existed:
        print(f"Branch {main_branch_name} does not exist.")
        return
    main_branch_version = main_branch_existed[0][1]

    vc_cursor.execute(query, (target_branch_name,))
    target_branch_existed = vc_cursor.fetchall()
    if not target_branch_existed:
        print(f"Branch {target_branch_name} does not exist.")
        return
    target_branch_version = target_branch_existed[0][1]

    # Read main branch tail and target branch tail sql file
    main_branch_path = f"../branch_tail_schema/{main_branch_name}.sql"
    target_branch_path = f"../branch_tail_schema/{target_branch_name}.sql"
    main_schema = read_sql_file(main_branch_path)
    target_schema = read_sql_file(target_branch_path)
    # Parse sql scripts into dictionary
    main_schema_dict = parse_sql_script(main_schema)
    target_schema_dict = parse_sql_script(target_schema)

    # Check if there is any conflict between 2 branches
    is_conflict = check_branch_conflicts(main_branch_name, main_schema_dict, target_branch_name, target_schema_dict)
    # if conflict exists: show conflicts
    if is_conflict[0]:
        print("Schema conflict exists between 2 branches as follows:")
        conflict_sql_script = is_conflict[1]
        print(conflict_sql_script)
        return conflict_sql_script
    # if there is no conflict: merge 2 branches
    else:
        # Merged schema
        merged_schema_dict = merge_schema(main_schema_dict, target_schema_dict)
        downgrade = generate_sql_diff(main_schema_dict, merged_schema_dict)
        upgrade = generate_sql_diff(merged_schema_dict, main_schema_dict)


        msg = f"Merge {target_branch_name} into {main_branch_name}"
        merged_version = str(uuid.uuid4())[:8]

        # Get branch info
        query = f"SELECT * FROM branch WHERE name = '{main_branch_name}'"
        vc_cursor.execute(query)
        branchInfo = vc_cursor.fetchall()[0]
        last_version = branchInfo[2]
        branchID = branchInfo[0]

        # Insert into commit table
        now = datetime.datetime.now()
        insert = "INSERT INTO commit (version, branch, last_version, upgrade, downgrade, time, uid, msg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (merged_version, branchID, last_version, upgrade, downgrade, now.strftime("%Y-%m-%d %H:%M:%S"), current_uid, msg)
        vc_cursor.execute(insert, val)

        # Update branch table
        update = "UPDATE branch SET tail = %s WHERE bid = %s;"
        val = (merged_version, branchID)
        vc_cursor.execute(update, val)

        # Insert into merge table
        insert = "INSERT INTO merge (merged_version, main_branch_version, target_branch_version) VALUES (%s, %s, %s)"
        val = (merged_version, main_branch_version, target_branch_version)
        vc_cursor.execute(insert, val)

        # Update user table
        update = "UPDATE user SET current_version = %s, current_branch = %s WHERE uid = %s;"
        val = (merged_version, main_branch_name, current_uid)
        vc_cursor.execute(update, val)

        vcdb_connection.commit()

        print(f"Successfully merged {target_branch_name} into {main_branch_name}!")
    return msg

if __name__ == '__main__':
    merge('branch1', 'branch2', 'fakeuid')
    


