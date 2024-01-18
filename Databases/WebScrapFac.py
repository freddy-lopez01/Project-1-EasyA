import requests
from bs4 import BeautifulSoup
from collections import namedtuple

# Set debug to True to enable debug messages
debug = True
verbose = True


# Define a namedtuple to store department and faculty data for future use
DeptFac = namedtuple('DeptFac', ['dept', 'fac'])

#def scrape_DeptFac_data():

url = 'https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/'
# Debug message before making the request
if debug:
    print(f"Connecting to: {url}")
response = requests.get(url)

# Debug message after making the request
if debug:
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
            #department_links.append(department_link)
            department_names.append(department_name)
            #add function to pull facultiy

        #debug formating data
        if debug:
            print("List of Departments:")
            for department in department_names:
                    print(department)

        # debug formating data
        if debug:
            print("List of Departments URLS:")
            for link in department_links:
                    print(link)

    else:
            if debug:
                print("No department list found on the webpage.")
else:
    if debug:
        print("Failed to retrieve the webpage. Status Code:", response.status_code)

#def scrape_FacinDept():