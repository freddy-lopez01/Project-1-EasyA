import mechanicalsoup
from bs4 import BeautifulSoup
from collections import namedtuple

# Define a namedtuple to store department and faculty data for future use
DeptFac = namedtuple('DeptFac', ['name', 'faculty'])

def scrape_DeptFac_data():
    url = 'https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/'
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)

    # Extract department links form the html (you will need to inspect the page to see how it is listed)
    # These links are in the following format:
    # <ul id"/art_science/" class="nav">
    # <a href="/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/africanstudies/">African Studies</a> </ul>
    department_links = browser.page.select('ul.nav#arts_sciences a')
    
    # create an empty list to return the data
    DeptFac_list = []
    print('DeptFac_list after initialization:', DeptFac_list)

    # for each link in the links pulled from above save the name and url.
    for department_link in department_links:
        department_name = department_link.text
        department_url = department_link['href']

        # Get faculty in each singular department by calling separate function that grabs FAC names as a list.
        faculty = scrape_fac_in_dept(department_url)

        # Create DeptFac namedtuple and append to the list
        add_person = DeptFac(name=department_name, faculty=faculty)
        DeptFac_list.append(add_person)

    print('DeptFac_list after scraping:', DeptFac_list)
    return DeptFac_list

def scrape_fac_in_dept(department_url):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(department_url)

    # Extract faculty names
    faculty_list = []
    for faculty_elem in browser.page.select('div#facultytextcontainer p.facultylist'):
        faculty_list.append(faculty_elem.text.strip())

    print('faculty_list:', faculty_list)
    return faculty_list
