import sqlite3
import ast
import re
import subprocess
'''---------------------------------------------------------------'''
#debug aids
debug =True
'''----------------------------------------------------------------'''

#definfed by folder structure
initData_file = "DataFiles/FacData.txt"
database_name = "FacDatabase.sqlite"
url_file = "DataFiles/url.txt"

# Prompt the user for input
user_input = input("Do you want to update the database? (y/n): ")

if user_input.lower() == 'y':
    #keep promtping user until valid input is given
    while True:
        # Execute the web scraper script to update the data
        # Prompt the user for a valid URL
        url_input = input("Please enter a valid URL: ")
        # Define a regex pattern for the expected URL structure
        expected_pattern = re.compile(r'https://web.archive.org/web/\d{14}/http://catalog.uoregon.edu/arts_sciences/')
        # Validate the URL format using the regex pattern
        if expected_pattern.match(url_input):
            # Write the valid URL to the url.txt file
            with open(url_file, 'w') as url_file:
                url_file.write(url_input)
        # Execute the web scraper script to update the data
            subprocess.run(["python", "WebScrapFac.py"])
            #loop escape
            break
        else:
            print("Invalid URL format. Please enter a valid URL format: https://web.archive.org/web/**************/http://catalog.uoregon.edu/arts_sciences/.")
elif user_input.lower() == 'n':
    # Open the file and parse the data
    with open(initData_file, 'r') as file:
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
else:
    print("Invalid input. Please enter 'y' or 'n'.")