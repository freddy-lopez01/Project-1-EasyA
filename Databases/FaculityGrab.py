import sqlite3
import argparse

def create_database():
    # Connect to SQLite database or create if not exists
    conn = sqlite3.connect('FacDatabase.sqlite')
    cursor = conn.cursor()

    # Create a table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            department TEXT,
            name TEXT
        )
    ''')

    # Commit and close the connection
    conn.commit()
    conn.close()

def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()

    # Process and return the data
    return [line.strip() for line in data]

def insert_data_to_database(data):
    conn = sqlite3.connect('FacDatabase.sqlite')
    cursor = conn.cursor()

    for department, names in data.items():
        for name in names:
            cursor.execute('INSERT INTO faculty VALUES (?, ?)', (department, name))

    # Commit and close the connection
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='Script to populate SQLite database with faculty data.')
    parser.add_argument('-f', action='store_true', help='Pull data from file (FacData.txt in DataFiles directory).')
    parser.add_argument('-i', action='store_true', help='Run WebscrapFac script and pull data from the file, adding changes to the database.')

    args = parser.parse_args()

    if args.f:
        # Pull data from file
        file_path = 'DataFiles/FacData.txt'
        data = read_data_from_file(file_path)
    elif args.i:
        # Run WebscrapFac script (placeholder)
        # Insert your code to run the WebscrapFac script here
        # For now, let's assume WebscrapFac creates a file named WebscrapFacData.txt
        # Replace this placeholder code with actual WebscrapFac integration
        with open('WebscrapFacData.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()

    # Organize data by department
    department_data = {}
    current_department = ''
    for line in data:
        if line.strip().endswith(':'):
            current_department = line.strip()[:-1]
            department_data[current_department] = []
        else:
            department_data[current_department].append(line.strip())

    # Create or connect to the database
    create_database()

    # Insert data into the database
    insert_data_to_database(department_data)

if __name__ == "__main__":
    main()