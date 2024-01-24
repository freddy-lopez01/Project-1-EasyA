import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import time


''' Change bool as info is needed
DEBUGING==========================================================================================================================================================='''
debug_main = True
#debug function
debug_Fac = False
#debug sort
debug_sort = False
#more info if needed
verbose = False
'''============================================================================================================================================================'''


# Interative function to open link and pull name data
def Scrape_FacinDept(department_link):
    #sleep added to prevent web denial
    time.sleep(2)
    # Make a request for the department link
    # slow time to ensure connection
    time.sleep(15)
    department_response = requests.get(department_link)
    # Debug message after making the request
    if debug_Fac:
        print(f"Status Code for {department_link}: {department_response.status_code}")

    # Check if the request was successful (status code 200)
    if department_response.status_code == 200:
        department_soup = BeautifulSoup(department_response.text, 'html.parser')

        # Formated html file code format that has data needed
        #<div id="facultytextcontainer" class="tab_content">
		#		<h3>Participating Faculty</h3>
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
            filtered_faculty_paragraphs = [p for p in filtered_faculty_paragraphs  if not p.find('em')]

            # Find any <h3> element to start marking temporary faculty
            participating_header = faculty_container.find('h3')

            # Determine if the faculty member is permanent ('p') or temporary ('t')
            is_temporary = False

            # Initialize a list to store faculty names and status
            faculty_names = []

            # Initialize the faculty type as 'P' by default
            faculty_type = 'P'

            # Iterate over each <p> tag within faculty_container
            for faculty_paragraph in filtered_faculty_paragraphs:
                #seperate all values not need form scrap
                faculty_name = faculty_paragraph.text.split(',')[0].strip()

                #Check if the previous <h3> header contains "Faculty"
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

            # Return the faculty names as a list close connection)
            # Sort the names alphabetically
            sorted_names = sorted(faculty_names, key=lambda x: (x[0].split()[-1], x[0].split()[0], x[0]))

            # Debug message for sorted faculty names and types
            if debug_sort:
                print(f"Faculty Names and Types SORTED for {department_link}:")
                formatted_string = '\n'.join([f"{name} ({faculty_type})" for name, faculty_type in sorted_names])
                print(formatted_string)

            return sorted_names

            # Debug message for faculty name
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
            print(f"Failed to retrieve data for {department_link} closing connection. Status Code:", department_response.status_code)
        return None


#def scrape_DeptFac_data():
# Define a namedtuple to store department and faculty data for future use
DeptFac = namedtuple('DeptFac', ['dept', 'fac'])
# create an empty list to return the data tuples
DeptFac_list = []

url = 'https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/'
# Debug message before making the request
if debug_main:
    print(f"Connecting to: {url}")

try:
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
    #<ul id="/art_sciences/" class="nav"
    # <li><a href="/web/20141107201343/http://catalog.uoregon.edu/arts_sciences/africanstudies/">African Studies</a></li>
    # Find the <ul> element with class "nav" and id "/arts_sciences/"
    department_elements = soup.find('ul', {'class': 'nav', 'id': '/arts_sciences/'})

    #Find all <a> tags within department_elements
    department_elements = department_elements.find_all('a')
    # closes web connection no longer need data is local now
    response.close()

    #initialize lists to hold data
    department_names = []
    department_links = []

    # debug check to see if element is found
    if verbose:
        print(f"elements pulled: {department_elements}")

    if department_elements:
        #Iterate over each <a> tag in the department_elements
        for department_element in department_elements:
            #Retrieve the text content of the current <a> tag and append it to the departments list
            department_name = department_element.text
            # Retrieve the value of the href attribute of the current <a> tag
            department_link =  "https://web.archive.org/" + department_element.get('href')
            # try to Call the function to scrape additional data for each department link broken up for clarity
            try:
                faculty_names = Scrape_FacinDept(department_link)
            except requests.exceptions.RequestException as e:
                # Handle connection error
                print(f"Connection error for {department_link}: {e}")
                faculty_names = None

            # Do something with the returned data, for example, store it in a list
            if faculty_names:
            #Store data in list if data was pulled else emtpy string
                DeptFac_list.append(DeptFac(department_name, faculty_names))
            elif faculty_names is None:
                DeptFac_list.append(DeptFac(department_name, ''))
                print(f"Missing data due to connection failure, please run again: {department_name}")

            #debug indiviual data types Saved if need
            if verbose:
                print("you may need to toubleshoot each data type look to line 116")
                #department_links.append(department_link)
                #department_names.append(department_name)


        #debug formating data
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

        print(f"FacData.txt file saved in {data_directory}. SCRIPT END")

    else:
            if debug_main:
                print("No department list found on the webpage.")
else:
    if debug_main:
        print("Failed to retrieve the webpage. Status Code:", response.status_code)

#note conecton is ened after data is local
