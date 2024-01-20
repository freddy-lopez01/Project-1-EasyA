import sqlite3

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
    else:
        parsed_data[current_dept].append(line)

print(f'This is the parsed_data{parsed_data}')

# Connect to SQLite database gradedatatbase
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# Create a table of data course_data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS FacultyByDepartment (
        dept_name TEXT,
        fac_list TEXT
    )
''')

# Insert and parse data into table (this code assume that data has a key then fallowing a list of name)
for dept_name, names in parsed_data.items():
    for name in names:
        cursor.execute('INSERT INTO FacultyByDepartment VALUES (?, ?)', (dept_name, name))

# Commit the changes and close the connection
conn.commit()
conn.close()
