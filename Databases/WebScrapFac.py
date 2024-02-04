import os
import sys
import time
import requests
import random
from bs4 import BeautifulSoup
from collections import namedtuple
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

'''
Filename:WebScrapFac.py
Author: Willard, Daniel
Date Created: 16 JAN 2024
Date Last Modified: 03 FEB 2024
Description: this code will be run though update. but can be run seperatly. This code goes to the landing website and collects the links and departments for the uo
then it iterates trough that names website and grabs all the faculty name on the website and stroes it in a tuple that is piped to a .txt file
that then update reads form to update the database.
see code comments for more info

'''

''' Change bool as info is needed
DEBUGING==========================================================================================================================================================='''
debug_main = True
# debug function
debug_Fac = False
# debug sort
debug_sort = False
# more info if needed
verbose = False
# run time
start_time = time.time()
'''============================================================================================================================================================'''

# Define a namedtuple to store department and faculty data for future use
DeptFac = namedtuple('DeptFac', ['dept', 'fac'])
# create an empty list to return the data tuples
DeptFac_list = []
# directory for update and write files
data_directory = "DataFiles"

# Function to create a session with retry mechanism format form stackoverflow
def create_session():
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
# Interative function to open link and pull name data form the archive website
def Scrape_FacinDept(department_link, session):
    # sleep added to prevent web denial
    # Make a request for the department link
    # slow time to ensure connection
    time.sleep(random.uniform(0, 1))
    try:
        department_response = session.get(department_link)
    except requests.exceptions.RequestException as e:
        # Handle connection error
        print(f"Connection error for {department_link}: {e}")
        return None
    # Debug message after making the request
    if debug_Fac:
        print(f"Status Code for {department_link}: {department_response.status_code}")

    # Check if the request was successful (status code 200)
    if department_response.status_code == 200:
        department_soup = BeautifulSoup(department_response.text, 'html.parser')

        # Formatted html file code format that has data needed
        # <div id="facultytextcontainer" class="tab_content">
        #       <h3>Participating Faculty</h3>
        #        <p>Lindsay F. Braun, history</p>
        #        <p class="facultylist">Yvonne A. Braun, women’s and gender studies</p>
        #
        # Find the <div> element with id "facultytextcontainer"
        faculty_container = department_soup.find('div', {'id': 'facultytextcontainer'})
        # Check if the faculty_container is found
        # connect no longer needed data is now local
        department_response.close()
        if faculty_container:
            # Check for the <h3> tag with text "Faculty" since pages add other data that I was pulling form the container facultylist

            filtered_faculty_paragraphs = faculty_container.find_all('p', {'class': ['facultylist', None]})

            # Exclude paragraphs that contain specific elements
            filtered_faculty_paragraphs = [p for p in filtered_faculty_paragraphs if not p.find('em')]


            # Initialize a list to store faculty names and status
            faculty_names = []

            # Iterate over each <p> tag within faculty_container
            for faculty_paragraph in filtered_faculty_paragraphs:
                # separate all values not need form scrap
                faculty_name = faculty_paragraph.text.split(',')[0].strip()

                # Check if the previous <h3> header contains "Faculty" to cheack facultiy type
                #this doesnt work as planned but it is a feature now not a bug works as inteneded.
                previous_h3 = faculty_paragraph.find_previous('h3')
                if previous_h3 and ('Faculty' or 'None' in previous_h3.text):
                    faculty_type = 'P'
                else:
                    faculty_type = 'T'
                if verbose:
                    print(f" H3 Headerer above: {previous_h3} and Type = {faculty_type} ")
                faculty_names.append((faculty_name, faculty_type))

            # Debug message for faculty names
            if debug_Fac:
                print(f"Faculty Names and Types for {department_link}:")
                for faculty_name, faculty_type in faculty_names:
                    print(f"{faculty_name} ({faculty_type})")

            # Return the faculty names as a list close connection
            # Sort the names alphabetically
            sorted_names = sorted(faculty_names, key=lambda x: (x[0].split()[-1], x[0].split()[0], x[0]))

            # Debug message for sorted faculty names and types
            if debug_sort:
                print(f"Faculty Names and Types SORTED for {department_link}:")
                formatted_string = '\n'.join([f"{name} ({faculty_type})" for name, faculty_type in sorted_names])
                print(formatted_string)

            return sorted_names

        # THIS IS ERROR CHECKING _____________________________________________________________________________________________________________________________
        else:
            if debug_Fac:
                print(f"No faculty information found for {department_link} closing connection.")
            data = "NONE"
            return data

    else:
        if debug_Fac:
            print(f"Failed to retrieve data for {department_link} closing connection. Status Code:",
                  department_response.status_code)
        return None

def main():
    global start_time
    global DeptFac_list
    global data_directory
    # output for when run form update
    print("Connected To Subprocess WEBSCRAP")
    fileURL_path = os.path.join(data_directory, "url.txt")
    with open(fileURL_path, 'r') as file:
        url = file.read().strip()
    print("URL pulled form File url.txt")
    # Debug message before making the request
    if debug_main:
        print(f"Connecting to: {url}")

    try:
        session = create_session()
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        # Handle connection error
        print(f"Connection error for {url}: {e}")
        sys.exit()

    # Debug message after making the request
    if debug_main:
        print(f"Status Code: {response.status_code}")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Must find the element to pull form the website the deptments are in the ntml elements
        # Found:
        # <ul id="/art_sciences/" class="nav"
        # <li><a href="/web/20141107201343/http://catalog.uoregon.edu/arts_sciences/africanstudies/">African Studies</a></li>
        # Find the <ul> element with class "nav" and id "/arts_sciences/"
        department_elements = soup.find('ul', {'class': 'nav', 'id': '/arts_sciences/'})

        # Find all <a> tags within department_elements
        department_elements = department_elements.find_all('a')
        # closes web connection no longer need data is local now
        response.close()

        # initialize lists to hold data
        department_names = []
        department_links = []

        # debug check to see if element is found
        if verbose:
            print(f"elements pulled: {department_elements}")

        if department_elements:
            # Iterate over each <a> tag in the department_elements
            # track progress info
            total_departments = len(department_elements)
            current_department = 0
            print("Progress: 0.00%")
            for department_element in department_elements:
                # Increase the current_department count
                current_department += 1
                # Retrieve the text content of the current <a> tag and append it to the departments list
                department_name = department_element.text
                # Retrieve the value of the href attribute of the current <a> tag
                department_link = "https://web.archive.org/" + department_element.get('href')
                # try to Call the function to scrape additional data for each department link broken up for clarity
                try:
                    faculty_names = Scrape_FacinDept(department_link, session)
                except requests.exceptions.RequestException as e:
                    # Handle connection error
                    print(f"Connection error for {department_link}: {e}")
                    faculty_names = None
                finally:
                    # Close the session to release resources
                    if 'session' in locals():
                        session.close()

                # Print progress
                progress = (current_department / total_departments) * 100
                print(f"Progress: {progress:.2f}%")

                # Do something with the returned data, for example, store it in a list
                if faculty_names:
                    # Store data in list if data was pulled else emtpy string
                    DeptFac_list.append(DeptFac(department_name, faculty_names))
                elif faculty_names is None:
                    DeptFac_list.append(DeptFac(department_name, ''))
                    print(f"Missing data due to connection failure, please run again: {department_name}")

                # debug indiviual data types Saved if need
                if verbose:
                    print("you may need to toubleshoot each data type look to line 116")
                    department_links.append(department_link)

            # debug formating data
            if debug_main:
                print("List of Departments:")
                for Fac in DeptFac_list:
                    print(Fac)

            # debug formating data
            if verbose:
                print("List of Departments & URLS:")
                for department, link in zip(department_names, department_links):
                    print(f"{department}: {link}")

            # Write data to a file to Data File Directory
            # Ensure the "DataFiles" directory exists
            data_directory = "DataFiles"
            os.makedirs(data_directory, exist_ok=True)

            file_path = os.path.join(data_directory, "FacData.txt")

            with open(file_path, "w") as file:
                for dept_fac in DeptFac_list:
                    file.write(f"{dept_fac.dept}:\n")
                    for faculty in dept_fac.fac:
                        file.write(f"\t{faculty}\n")

        else:
            if debug_main:
                print("No department list found on the webpage.")
    else:
        if debug_main:
            print("Failed to retrieve the webpage. Status Code:", response.status_code)

    end_time = time.time()
    execution_time = end_time - start_time
    # timeing stuff for analytics
    minutes = int(execution_time // 60)
    seconds = execution_time % 60
    if debug_main:
        print(f"Execution time: {minutes} minutes and {seconds:.2f} seconds")
    print(f"FacData.txt file saved in {data_directory}. SCRIPT END")




if __name__ == "__main__":
    main()