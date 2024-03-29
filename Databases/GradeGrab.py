import sqlite3
import json

'''
Production Note:
This is a start up script and must be done only once at the beginning. 
User should know howto format file if they want to change the database
This only overwrites the data if the user wanted to append it should have been in the design docuemntation 
'''
# Read data from the reduced JavaScript file that form: https://emeraldmediagroup.github.io/grade-data/gradedata.js
# loads data form file into emd_data_js
with open('gradedata-only.js', 'r') as file:
    emd_data_js = file.read()

# Modify JavaScript code form reduced file to be a valid Python dictionary literal
emd_data_js = emd_data_js.replace('var groups =', '').replace(';', '')

# This line of code is using the json.loads() method to load and parse a JSON-formatted string (emd_data_js) into a Python dictionary (groups_data).
# pulled  
groups_data = json.loads(emd_data_js)

# Connect to SQLite database gradedatatbase 
conn = sqlite3.connect('GradeDatabase.sqlite')
cursor = conn.cursor()

# Create a table of data course_data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS course_data (
        group_code TEXT,
        term_desc TEXT,
        aprec REAL,
        bprec REAL,
        cprec REAL,
        crn TEXT,
        dprec REAL,
        fprec REAL,
        instructor TEXT
    )
''')

# Insert data into the table iteratively over each course takes all data in the same order as in grade_data_only.js
# format pulled form sqlite documentation of interations
for group_code, courses in groups_data.items():
    for course in courses:
        cursor.execute('''
            INSERT INTO course_data (group_code, term_desc, aprec, bprec, cprec, crn, dprec, fprec, instructor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            group_code,
            course.get('TERM_DESC', ''),
            float(course.get('aprec', 0.0)),
            float(course.get('bprec', 0.0)),
            float(course.get('cprec', 0.0)),
            course.get('crn', ''),
            float(course.get('dprec', 0.0)),
            float(course.get('fprec', 0.0)),
            course.get('instructor', '')
        ))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into the SQLite database.")