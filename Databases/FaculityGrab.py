import sqlite3
import ast
'''---------------------------------------------------------------'''
#debug aids
debug =True
'''----------------------------------------------------------------'''

#definfed by folder structure
file_path = "DataFiles/FacData.txt"
database_name = "FacDatabase.sqlite"

# Open to the file and parse the data
with open(file_path, 'r') as file:
    data = file.readlines()

parsed_data = {}
current_dept = None

for line in data:
    line = line.strip()
    if line.endswith(':'):
        current_dept = line[:-1]
        parsed_data[current_dept] = []
    if line.endswith(')'):
        # Parse faculty data
        # Use eval to convert the string to a tuple
        faculty_data = ast.literal_eval(line)
        parsed_data[current_dept].append(faculty_data)
    else:
        continue
if debug:
    print("This is the parsed_data:")
    for dept_name, faculty_list in parsed_data.items():
        for faculty in faculty_list:
            print(f"Department: {dept_name}, Faculty Name: {faculty[0]}, Faculty Type: {faculty[1]} \n")

# Connect to SQLite database FacDatatbase
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# Create a table of data course_data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS FacultyByDepartment (
        dept_name TEXT,
        fac_list TEXT,
        fac_type TEXT
    )
''')

# Insert and parse data into table (this code assume that data has a key then fallowing a list of name)
for dept_name, faculty_list in parsed_data.items():
    for faculty in faculty_list:
        cursor.execute('INSERT INTO FacultyByDepartment VALUES (?, ?, ?)', (dept_name, faculty[0], faculty[1]))

# Commit the changes and close the connection
conn.commit()
conn.close()
