import sqlite3
import ast
import re
import time
import WebScrapFac

'''
Production Note:
imports Scrapper and updates the database into one complete data base.
'''

'''DEBUG---------------------------------------------------------------'''
#debug aids
debug =True
start_time = time.time()
'''----------------------------------------------------------------'''


#definfed by folder structure
initData_file = "DataFiles/FacData.txt"
database_name = "CompleteDatabase.sqlite"
url_file = "DataFiles/url.txt"

def populate_database(parsed_data):
    try:
        # Connect to SQLite database GradeDatabase due to design change
        grade_conn = sqlite3.connect('GradeDatabase.sqlite')
        grade_cursor = grade_conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to GradeDatabase: {e}")
        return

    try:
        # Connect to SQLite database FacDatabase
        fac_conn = sqlite3.connect(database_name)
        fac_cursor = fac_conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to FacDatabase: {e}")
        grade_conn.close()
        return

    # Clear existing data
    fac_cursor.execute('DELETE FROM FacultyByDepartment')

    # Create a table of data FacultyByDepartment with all data collected
    fac_cursor.execute('''
            CREATE TABLE IF NOT EXISTS FacultyByDepartment (
                instructor TEXT,
                group_code TEXT,
                term_desc TEXT,
                aprec REAL,
                bprec REAL,
                cprec REAL,
                dprec REAL,
                fprec REAL,
                crn TEXT,
                dept_name TEXT DEFAULT 'NONE',
                fac_type TEXT DEFAULT 'NONE'
            )
        ''')

    # Populate data from GradeDatabase
    try:
        grade_cursor.execute('SELECT * FROM course_data')
        grade_data = grade_cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error executing SELECT query on GradeDatabase: {e}")
        grade_conn.close()
        fac_conn.close()
        return

    for course in grade_data:
        # Insert data into FacultyByDepartment table
        fac_cursor.execute('INSERT INTO FacultyByDepartment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (course[8], course[0], course[1], course[2], course[3], course[4], course[7],
                            course[6], course[5], 'NONE', 'NONE'))

    # Populate data from parsed_data
    for dept_name, faculty_list in parsed_data.items():
        for faculty in faculty_list:
            faculty_name = faculty[0]
            fac_type = faculty[1]
            # Split faculty name into first and last name
            split_name = faculty_name.split()
            last_name = split_name[-1]
            first_name = ' '.join(split_name[:-1])
            # Check if the faculty member exists in the FacultyByDepartment table
            fac_cursor.execute(
                'SELECT * FROM FacultyByDepartment WHERE LOWER(instructor) LIKE ? AND LOWER(instructor) LIKE ?',
                (f'%{last_name.lower()}, {first_name.lower()}%', f'%{first_name.lower()}%'))
            matching_faculty = fac_cursor.fetchall()
            if not matching_faculty:
                # If faculty not found, insert new record
                fac_cursor.execute('INSERT INTO FacultyByDepartment (instructor, dept_name, fac_type) VALUES (?, ?, ?)',
                                   (faculty_name, dept_name, fac_type))
            else:
                # If faculty found, update dept_name and fac_type
                for row in matching_faculty:
                    fac_cursor.execute(
                        'UPDATE FacultyByDepartment SET dept_name = ?, fac_type = ? WHERE instructor = ?',
                        (dept_name, fac_type, row[0]))

    # Commit the changes and close the connections
    fac_conn.commit()
    fac_conn.close()
    grade_conn.close()

def main():
    global initData_file
    global database_name
    global url_file
    global debug

    start_time = time.time()
    user_input = input("Do you want to update the database? (y/n): ")

    if user_input.lower() == 'y':
        # Execute the web scraper script to update the data
        # Prompt the user for a valid URL
        url_input = input("Please enter a valid URL: ")
        # Define a regex pattern for the expected URL structure
        expected_pattern = re.compile(r'https://web.archive.org/web/\d{14}/http://catalog.uoregon.edu/arts_sciences/')
        # Validate the URL format using the regex pattern
        while not expected_pattern.match(url_input):
            print("Invalid URL format.")
            url_input = input(
                "Please enter a valid URL: https://web.archive.org/web/**************/http://catalog.uoregon.edu/arts_sciences/.")

        with open(url_file, 'w') as url_file:
            print("Writing to file")
            url_file.write(url_input)

        print("Starting subprocess. Estimated wait time is 8 minutes. Script will notify when complete.")
        WebScrapFac.main()
        print("Data Scrap completed.")

        # After updating the data, populate the database
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

        populate_database(parsed_data)

        print("DATABASE IS UP TO DATE. SCRIPT COMPLETED")
        end_time = time.time()
        execution_time = end_time - start_time
        # timing stuff
        minutes = int(execution_time // 60)
        seconds = execution_time % 60
        if debug:
            print(f"Execution time: {minutes} minutes and {seconds:.2f} seconds")


    elif user_input.lower() == 'n':
        # Open the file stored form last webscrape and parse the data
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

        populate_database(parsed_data)

        print("DATABASE IS UP TO DATE. SCRIPT COMPLETED")
        end_time = time.time()
        execution_time = end_time - start_time
        # timing stuff
        minutes = int(execution_time // 60)
        seconds = execution_time % 60
        if debug:
            print(f"Execution time: {minutes} minutes and {seconds:.2f} seconds")
    else:
        print("Invalid input. Please enter 'y' or 'n' And try again.")


if __name__ == "__main__":
    main()