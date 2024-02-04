import sqlite3

'''
Filename:compareDB.py
Author:Willard, Daniel 
Date Created: 26 JAN 2024
Date Last Modified: 03 FEB 2024
Description: this code connects to a older version of our database check for testing and the new version and shows the diffferance in
faculty type and Departments for de bug purposes
see code comments for more info
'''

def compare_databases(db1_path, db2_path):
    # Connect to the databases
    conn1 = sqlite3.connect(db1_path)
    conn2 = sqlite3.connect(db2_path)

    # Create cursors
    cursor1 = conn1.cursor()
    cursor2 = conn2.cursor()

    # Query the first database for distinct faculty types, department names, and their corresponding faculty lists
    cursor1.execute("SELECT DISTINCT fac_type, dept_name, instructor FROM FacultyByDepartment")
    db1_results = cursor1.fetchall()

    # Query the second database for distinct faculty types, department names, and their corresponding faculty lists
    cursor2.execute("SELECT DISTINCT fac_type, dept_name, fac_list FROM FacultyByDepartment")
    db2_results = cursor2.fetchall()

    # Close connections
    conn1.close()
    conn2.close()

    # Compare the results
    for result1 in db1_results:
        for result2 in db2_results:
            if result1[0] != result2[0] and result1[1] == result2[1] and result1[2] == result2[2]:
                print("Match found for faculty:", result1[2], result2[2])
                print("Faculty Type in Completedatabase:", result1[0])
                print("Faculty Type in FacultyByDepartment:", result2[0])
                print("Faculty DEPT in Completedatabase:", result1[1])
                print("Faculty DEPT in FacultyByDepartment:", result2[1])
                print("-----------------------------")





# Paths to the databases
db1_path = "CompleteDatabase.sqlite"
db2_path = "FacDatabase.sqlite"

# Call the function to compare the databases
compare_databases(db1_path, db2_path)
