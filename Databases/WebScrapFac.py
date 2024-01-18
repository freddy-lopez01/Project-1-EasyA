import os
import requests
from bs4 import BeautifulSoup
from collections import namedtuple

''' Change bool as info is needed
DEBUGING==========================================================================================================================================================='''
debug_main = True
#debug function
debug_Fac = True
#more info if needed
verbose = False
'''============================================================================================================================================================'''


# Interative function to open link and pull name data
def Scrape_FacinDept(department_link):
    # Make a request for the department link
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
        # Find the <div> element with id "facultytextcontainer"
        faculty_container = department_soup.find('div', {'id': 'facultytextcontainer'})
        # Check if the faculty_container is found
        if faculty_container:
            # Extract the text content of the <p> tags within faculty_container
            faculty_paragraphs = faculty_container.find_all('p', {'class': ['facultylist', None]})
            #connect no longer needed data is now local
            department_response.close()

            # Initialize a list to store faculty names
            faculty_names = []

            # Iterate over each <p> tag within faculty_container
            for faculty_paragraph in faculty_paragraphs:
                faculty_name = faculty_paragraph.text.split(',')[0].strip()
                faculty_names.append(faculty_name)

            # Debug message for faculty names
            if debug_Fac:
                print(f"Faculty Names for {department_link}:")
                for faculty_name in faculty_names:
                    print(faculty_name)

            # Return the faculty names as a list close connection)
            return faculty_names

        else:
            if debug_Fac:
                print(f"No faculty information found for {department_link} closing connection.")
            return None

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
response = requests.get(url)

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
            # Call the function to scrape additional data for each department link broken up for clarity
            faculty_names = Scrape_FacinDept(department_link)

            # Do something with the returned data, for example, store it in a list
            if faculty_names:
            # Assuming you have a list to store the data
                DeptFac_list.append(DeptFac(department_name, faculty_names))

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
