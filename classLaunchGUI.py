"""
Filename: classLaunchGUI.py
Author: Freddy Lopez
Date Created: 01/14/2024
Date Last Modified: 02/04/2024
Description: classLaunchGUI.py contains the functionality and structure of the Graphic User Interface regarding the software called EasyA. Upon execution the GUI displays the main landing page which consits of the dropdown options which the user can select in order to submit a query regarding A's or D/F's for a specific class (eg. CIS 422), class Level (eg. CIS 400 (show all CIS 400 level classes)), or grades across an entire department (eg. All CIS classes offered at UO that were not redacted from the source
"""
import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import font, ttk, StringVar, Button, Canvas, messagebox 
from PIL import ImageTk, Image
import array
import webbrowser
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt 
import graphing.graph_gen as graph
import re






############################################################################
# Global variables
############################################################################



color_Mode = True #This represents whether the user chooses the UI to be in light or dark mode. If true light mode, false for darkmode 
classCountSelection = False #Represents if the user wishes to have Class count on or off. False for off, True for on 
is_data = False 
box_state = False
selectedDic = {}

####### Example structure of selectedDic which is the dictionary that is sent to the 

# selectedDic = {
#         "graph_type": "class_level_dept",  # options: single_class, department, class_level_dept
#         "class_code": "CIS330",  # relevant if graph type is single_class; specific class code (e.g., CIS 422)
#         # "department": "Computer Information Science",  # relevant for single_dept and class_level_dept
#         "class_level": "200",  # relevant if graph type is class_level_dept; specific class level (e.g., 100, 200)
#         "instructor_type": "All Instructors",  # other option: "Faculty"
#         "grade_type": "Percent As",  # other option: "Percent Ds/Fs"
#         #"grade_type": "Percent Ds/Fs", # true/false
#         "class_count": False,  # whether to show the number of classes taught by each instructor
#         "xaxis_course": False, # displays courses instead of instructor
#         "light_mode": False # True = light mode, False = dark mode
#         }
selectedList = []
hasGrade = False 
gradeSel = "A"
naturalONLY = True
xaxis = False
currSubject = ""
currCourseLvl = ""
# Color pallete used in GUI
logobg = "#eaddcf"
navbg = "#e3f6f5"
sideBarbg = "#"
#submainbg = "#3f3f46"
submainbg = "#fef6e4"
darksubmainbg = "#282828"
darkslabbg = "#787878"
darklogobg="#242424"
#darksubmainbg = "#242424"
# This section will be dynamically updated based off of user input
# Dependencies:
#               Most recent user selection will dictate database query
#               


############################################################################
# Connecting to the database in order to create dynamic dropdown options
############################################################################


#
# Connction created to the database upon startup in order to populate Courese Options by connecting to the database via the .connect() method from the sqlite3 library
#
courseOPT = []
conn = sqlite3.connect('Databases/CompleteDatabase.sqlite')
print("Connection to Database successful...")
cursor = conn.cursor()
cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
data = cursor.fetchall()
print(data)


cursor.execute("""SELECT dept_name from 'FacultyByDepartment';""")
data = cursor.fetchall()
for sub in data:
    courseName = sub[0]
    if courseName not in courseOPT:
        courseOPT.append(courseName)
    else:
        continue
groupLS = []
cursor.execute("""SELECT group_code from 'FacultyByDepartment';""")
Ccode = cursor.fetchall()
for sub in Ccode:
    code = ""
    counter = 0
    courseCode = sub[0]
    #print(f"courseCode:{courseCode}")
    if courseCode != None: 
        for char in courseCode:
            if char.isdigit():
                break
            else:
                code += char
    if code not in groupLS and (code != ''):
        groupLS.append(code)
    else:
        continue
print(groupLS)

courselvlList = []
# Function to populate courses dropdown 

path = "../DataBases/GradeDatabase.sqlite"
def coursePopulate(Subject, CourseLvl):
    '''
    coursePopulate(Subject, CourseLvl) takes in the subject that the user selected and the courseLvl that was 
    selected and then connects to the /Databases/GradeDatabase.sqlite and fetches the column 'course_data' matching
    the codeTemplate variable obtained from combining the Subject code (eg. CIS) and the first digit of the course
    level (eg. 400) resulting in codeTemplate (eg. CIS4) that will then be used to compare all the classes found
    within the 'course_data'. The process is then repeated for each class in the database and only add classes that match
    the codeTemplate will be added to courselvlList which is used by the courses Combobox. courselvlList is cleared and
    every time a user selects a new subject or course level. 
    '''
    global courselvlList
    courselvlList.clear()
    conn2 = sqlite3.connect('./Databases/GradeDatabase.sqlite')
    cursor2 = conn2.cursor()
    cursor2.execute("""SELECT group_code from 'course_data';""")

    data2 = cursor2.fetchall()
    codeTemplate = str(Subject)+str(CourseLvl[0])
    #print(codeTemplate)
    for sub in data2:
        code = sub[0]
        res = re.findall('(\d+|[A-Za-z]+)', code)
        #print(res)
        #print(codeTemplate) 
        tmp = str(res[0])+str(res[1][0])
        #print(f"code: {code}")
        if codeTemplate == tmp:
            if code not in courselvlList:
                #print(f"sub: {code}")
                courselvlList.append(code)
            else:
                continue
        else:
            continue

    if (len(courselvlList) == 0) and (CourseLvl == "All Courses"):
        courselvlList.append("All "+Subject+" courses selected")
    elif (len(courselvlList) == 0):
        courselvlList.append("No Corresponding Classes")
    print(f"courselvlList: {courselvlList}")


print(courselvlList)
        
############################################################################
# Lists used by combobox
############################################################################

NATURAL_SCIENCE = ['BI Biology', 'CH Chemistry and Biochemistry', 'CIS Computer and Information Science', 'ERTH Earth Sciences', 'HPHY Human Physiology', 'MATH Mathematics', 'PHYS Physics', 'PSY Psychology']

TEMP_OPT = ["100", "200", "300", "400", "500", "600", "All Courses"]
TEMP_SUB = ['BI Biology', 'CH Chemistry',
            'CIS Computer and Information Science',
            'CRWR Creative Writing', 'EALL East Asian Languages and Literatures', 'EC Economics',
            'ENG English', 'ENVS Environmental Studies', 'ES Ethnic Studies', 'EURO European Studies',
            'FLR Folklore', 'GEOG Geography', 'GEOL Geological Sciences', 'GER German', 'HIST History',
            'HPHY Human Physiology', 'HUM Humanities', 'INTL International Studies', 'JDST Judaic Studies',
            'LA Landscape Architecture', 'LAS Latin American Studies', 'LING Linguistics', 'MATH Mathematics',
            'MDVL Medieval Studies', 'PHIL Philosophy', 'PHYS Physics', 'PS Political Science', 'PSY Psychology',
            'REES Russian and East European Studies', 'REL Religious Studies', 'RL Romance Languages', 'SCAN Scandinavian',
            'SOC Sociology', 'TA Theater Arts', "WGS Women's and Gender Studies"]

GRADE_OPT = ["A", "D/F"]
FACULTY_OPT = ["All Instructors", "Regular Faculty"]
GRAPH_TYPE = ["single_class", "department", "class_level_dept"]



############################################################################
# ResWindow function that displays user selections and the graph that was generated. 
############################################################################

def ResWindow(mode=0):
    """
    ResWindow() contains all the logic needed to send selectedDic to the graphing module for processing and calls the displaySelect() 
    nested function that provides the logic for displaying the users selection of the graph they just recieved in order to allow the user
    to reference their old selections if needed in order they wanted to recreate a graph with only a small change.

    ResWindow() will call the main(selectedDic) function located in graph_gen.py in order to pass the user input to generate said graph
    Until the user quits the graph window that is generated by the graphing module, then the graph selections will be displayed on a new 
    frame that can be resized and maintained open for the user to reference as they submit a new request 
    """
    global selectedDic
    global color_Mode
    resbg = ""
    windH = root.winfo_height()
    if color_Mode == True:
        resbg = submainbg
    else:
        resbg = darkslabbg

    resFrame = tk.Frame(main, bg=resbg)
    selectFrame = tk.Frame(resFrame, bg=resbg)
    header = tk.Label(selectFrame, text="Prior Selections Made:", font='Helvetica 10 bold',bg=resbg)


    for i in range(3):
        resFrame.rowconfigure(1, weight=1)

    resFrame.rowconfigure(1, weight=1)

    def displaySelect():
        global selectedDic
        header.grid(row=0, column=0, padx=15, pady=10)
        cnt = 2
        for key, value in selectedDic.items():
            ent = Entry(selectFrame, width=10)
            ent.grid(row=cnt, column=0, padx=10, pady=10)
            ent.insert(END, key)
            ent1 = Entry(selectFrame, width=10)
            ent1.grid(row=cnt, column=1, padx=10, pady=10)
            if key == "Subject":
                tmp = []
                val = selectedDic[key]
                tmp = val.split(" ")
                value = tmp[0]

            if key == "ClassCount":
                if value == True:
                    value = "On"
                else:
                    value = "Off"
            if key == "xaxisCourse":
                if value == 1:
                    value = "Courses"
                else:
                    value = "Instructors"
            ent1.insert(END, value)
            cnt += 1
        graph.main(selectedDic)

        

    print("before displaySelect")
    displaySelect()
    selectFrame.grid(row=0, column=0)
    resFrame.place(height=windH, width=700)
    print("after displaySelect")

    backButton = tk.Button(resFrame, text="close Selection Window", command=lambda: [resFrame.destroy()])
    main.add(resFrame)
    backButton.grid(row=1, column=0, sticky='w', padx=20, pady=20)



############################################################################
# Window Class used in order to create warning popup window
############################################################################

class Win:
    """
    The Win Class provides the functionality which allows for the user to recieve warning pop-ups if they are missing a required selection
    such as subject and A's or D/F's percentages 
    """
    def popup(self, alertM=""):
        tk.Tk().withdraw()
        name = messagebox.showinfo(title="Warning", message=alertM)





############################################################################
# Functions Created to provide functionaliy to the GUI and make it responsive in regards to user input
############################################################################



def submitQuery():
    '''
    submitQuery() provides the functionality of validating a users selections prior to sending the user selections to the graphing module 
    that will interpret said values and generate a graph that visually represents the users request
    The function will ensure that the user has selected a Subject and the grades to be presented (A's or D/F's)
    The function will also prompt different warning depending on what parameters are missing from the users input and will prevent
    submission of an invalid request, preventing any errors caused by user error to occur in the graphing module

    If no user errors are detected, the fucntion will then add the final remaining keys to selectedDic which consit of:
        grade_type
        class_count
        xaxis_course
        light_mode

    these values are based off of what the current global variables for each are. This approach was chosen to ensure that if the user
    makes any last minute changes to any selection, they can do so without having to reset the selection menu and/or making a change
    that isnt properly recorded and changed in selectedDic. This also provides onbe last check to make sure that the user-filled dictionary
    has all the nessessary keys needed to provide the graphing module all the information it needs in order to create an accurate graph
    '''

    global xaxis
    global color_Mode

    global hasGrade
    if (hasGrade == False) and (len(selectedDic) == 0):
        win = Win()
        win.popup("Must Select Subject and EasyA/Pass Field in order to submit")
        return 0
    elif (hasGrade == False) and (len(selectedDic) > 0):
        win = Win()
        win.popup("Must Select either A or D/F")
    else:
        print(f"==========global hasGrade: {hasGrade}")
        selectedList.append(gradeSel)
        if "instructor_type" not in selectedDic:
            selectedDic["instructor_type"] = "All Instructors"
        selectedDic["grade_type"] = gradeSel
        selectedDic["class_count"] = classCountSelection
        selectedDic["xaxis_course"] = xaxis
        print(f"final color_mode: {color_Mode}")
        selectedDic["light_mode"] = color_Mode
        print(f"Submitting complete query: {selectedDic}")
        ResWindow()

def clear(object):
    """
    Helper function created in order to clear a frame of all objects contained within a frame
    """
    slaves = object.grid_slaves()
    for x in slaves:
        x.destroy()

def openWeb(link):
    """
    openWeb() simply calls the webbrowser library within python3 that allows the user to click on a button that is binded to a link
    and redirects the users to the destination link on their native browser. 
    """
    webbrowser.open_new(link)

def clearBox():
    """
    clearBox() clears all selections made on the gui by resetting every user option to its default value.
    """
    global selectedDic
    global classCountSelection
    global NaturalONLY
    global xaxis
    global courselvlList
    global hasGrade

    subMenu0.set('')
    subMenu1.set('')
    subMenu2.set('')
    # subMenu3.set('')
    subMenu4.set('All Instructors')
    subMenu5.set('')
    NaturalScience.deselect()
    subMenu0.config(values=NATURAL_SCIENCE)
    ClassCount.deselect()
    courselvlList.clear()
    classCountSelection = False
    PassTypeL0.deselect()
    PassTypeL1.deselect()
    selectedDic.clear()
    Xaxis.deselect()
    xaxis = False
    box_state = False
    menuState='disabled'
    subMenu1.config(state=menuState)
    subMenu2.config(state=menuState)
    subMenu4.config(state=menuState)
    subMenu5.config(state=menuState)
    print("===================USER RESET DIC=======================\n")
    selectedDic.clear()
    print(f"SelectedDic: {selectedDic}\n")


def change_theme():
    """
    Calls the tkinter method .tk.call in order to call the azure-dark execuatable wiithin assets which help with the light/dark mode
    visual changes wihtin the UI
    """
    if root.tk.call("ttk::style", "theme", "use")=="azure-dark":
        root.tk.call("set_theme", "light")
    else:
        root.tk.call("set_theme", "dark")

def toggle():
    """
    toggle() bears the task of configuring the background (bg) color if each of the objects within the UI and by using .config()
    changing the background in real time based off the global variable color_Mode which gets triggered by the user hitting the 
    Light/dark mode toggle in the top status bar of the UI

    """
    global color_Mode

    if color_Mode == False:
        toggleB.config(image=offjpg)
        change_theme()
        subMain.config(bg=submainbg)
        NaturalScience.config(bg=submainbg)
        subjL.config(bg=submainbg)
        classL.config(bg=submainbg)
        courseL.config(bg=submainbg)
        instructL.config(bg=submainbg)
        ClassCount.config(bg=submainbg)
        PassTypeL.config(bg=submainbg)
        PassTypeL0.config(bg=submainbg)
        PassTypeL1.config(bg=submainbg)
        logo_widget2.config(bg=submainbg)
        slab1.config(bg=navbg)
        slab2.config(bg=navbg)
        slab3.config(bg=navbg)
        NavBar.config(bg=navbg)
        logoBar.config(bg=logobg)
        toggleLab.config(bg=logobg)
        toggleB.config(bg=logobg)
        logo_widget.config(bg=logobg)
        Xaxis.config(bg=submainbg)
        color_Mode = True
        print(f"Global ColorMode: {color_Mode}\n")

    else:
        toggleB.config(image=onjpg)
        change_theme() 
        NaturalScience.config(bg=darksubmainbg)
        subMain.config(bg=darksubmainbg)
        subjL.config(bg=darksubmainbg)
        classL.config(bg=darksubmainbg)
        courseL.config(bg=darksubmainbg)
        instructL.config(bg=darksubmainbg)
        ClassCount.config(bg=darksubmainbg)
        PassTypeL.config(bg=darksubmainbg)
        PassTypeL0.config(bg=darksubmainbg)
        PassTypeL1.config(bg=darksubmainbg)
        logo_widget2.config(bg=darksubmainbg)
        slab1.config(bg=darkslabbg)
        slab2.config(bg=darkslabbg)
        slab3.config(bg=darkslabbg)
        NavBar.config(bg=darkslabbg)
        logoBar.config(bg=darklogobg)
        toggleLab.config(bg=darklogobg)
        toggleB.config(bg=darklogobg)
        logo_widget.config(bg=darklogobg)
        Xaxis.config(bg=darksubmainbg)
        color_Mode = False
        print(f"Global ColorMode: {color_Mode}\n")

def closeGUI():
    """ 
    closeGUI() is called when the user presses the Quit EasyA button located on the navBar Frame. The function when called closes the
    connetion that is made with the database, destroys the root frame of the GUI and then calls exit() in order to close the session in
    the terminal that is running the software
    """
    conn.close()
    print(".\n.\n.\n.\n.\n")
    print("closing connection to Database...")
    print("Shutting down EasyA application....")
    root.destroy()
    exit()

def sendSelected(data):
    # selectedList.append(data)
    # print(f"New array: {selectedList}")
    pass
menuState = 'disabled'

"""
sub_select{integer}(event) are responsible for tracking user selection for each combobox or checkbox that allows the user to select an option. These functions 
called by the "command" parameter within said tk.checkbox or tk.combobox
"""

def sub_select0(event):
    """
    sub_select0(event) takes in a user selection from the Subject field and adds it to selectedDIC with the key name "Subject" and 
    the Subject abbreviation as the value of the new key. 
    once sub_select0(event) registers a selection made by the user, it then unblocks the rest of the dropdown boxes from the user. This 
    feature was implemented in order to guarentee the user picks a subject before being able to pick any other proceeding option.
    """
    global currSubject
    global selectedDic
    selected = subMenu0.get()
    code = selected.split(" ")
    print(code[0])
    sendSelected(code[0])
    selectedDic["Subject"] = code[0]
    box_state = True
    menuState = 'enabled'
    subMenu1.config(state=menuState)
    subMenu2.config(state=menuState)
    subMenu4.config(state=menuState)
    subMenu5.config(state=menuState)
    currSubject = code[0]
    print(selectedDic)


def sub_select1(event):
    """
    sub_select1(event) takes in a user selection from Course Level and creates a new key,value entry in selectedDic with they key 
    name being "class_level" and the value being the class level number (100, 200,...,600) or All Courses. To mitigate user error, 
    if the user selects "All courses", the function also adds the key,value pairs:
            "class_code" : selectedDic['Subject']
            "graph_type" : "department"

        The reason for this is that when the user selects "All courses", the only valid graph that can be created is a department graph 
        that contains all courses within the selected subject

    However, if the user selects a specific course level, then the function will populate selectedDic with the key,value pairs:
            "class_code" = *user selected class level*
            "graph_type" = "class_level_dept"

        These key,value are chosen due to preemptivly anticipate the user wanting to submit a request showing all classes within the 
        specific department and specific level within that department. 

    if a specific class level is chosen, then the proceeding dropdown "Course" is then populated to show all courses within the database
    that are in that class level that the user selects. This is a dynamic feature as if the user changes course level or subject, the 
    function will be recalled and display the classes matching the new, updated user selection 
    """
    global currCourseLvl
    global currSubject
    global selectedDic
    selected = subMenu1.get()
    if selected == "All Courses":
        selectedDic['class_level'] = selectedDic['Subject']
        temp = selectedDic['Subject']
        subMenu2.set(str(temp))
        subMenu5.set("department")
        selectedDic["class_code"] = selectedDic['Subject']
        selectedDic['graph_type'] = "department"
    else:
        selectedDic["class_level"] = selected

        selectedDic["class_code"] = selectedDic['Subject']
        subMenu5.set("class_level_dept")
        selectedDic['graph_type'] = "class_level_dept"
    print(selected)
    currCourseLvl = selected
    coursePopulate(currSubject, currCourseLvl)
    subMenu2.config(values=courselvlList)
    subMenu2.set('')
    print(selectedDic)

def sub_select2(event):
    """
    sub_select2(event) takes in the user selection from the courses dropdown menu and determines which option was chosen by the user
    if the user chooses "All courses selected", it will then modify the "class_code" key to have the value selectedDic['Subject'] 
    as "all courses selected" refers to all courses within the selected course level

    else if the user selects a specific course, then selectedDic["class_code"] is updated to have the course code that was selected and
    selectedDic["graph_type"] is updated to have the value "single_class"
    """
    global selectedDic
    selected = subMenu2.get()
    print(selected)
    if "selected" in str(selected): 
        selectedDic["class_code"] = str(selectedDic['Subject']) + str(selectedDic["class_level"])
        subMenu5.set("class_level_dept")
        selectedDic["graph_type"] = "class_level_dept"
    else:
        selectedDic["class_code"] = selected
        selectedDic["graph_type"] = "single_class"
        subMenu5.set("single_class")

    print(selectedDic)

def sub_select4(event):
    """
    sub_select4(event) takes in the users selection from the "Instructor" dropdown options and adds it to the selectedDic with the 
    key,value pair being:
        "Instructor" = *user selection*
    """
    selected = subMenu4.get()
    print(selected)
    sendSelected(selected)
    selectedDic["instructor_type"] = selected
    print(selectedDic)

def sub_select5(event):
    selected = subMenu5.get()
    print(selected)
    sendSelected(selected)
    selectedDic["graph_type"] = selected
    print(selectedDic)


def sub_select6():
    """
    sub_select6() takes in the user input from the two Radiobutton() objects which determine whether the user selects A's or D/F grades to
    be graphed based off all preceeding selections made by the user
    """
    global hasGrade
    hasGrade = True
    selected = ''
    global gradeSel
    if var1.get() == 1:
        selected = 'Percent As'
    elif var1.get() == 2:
        selected = 'Percent Ds/Fs'
    
    print(f"seleted in subselect6: {selected}")
    gradeSel = selected
    print(selectedDic)

def sub_select7():
    """
    sub_selct7() takes in the users input regarding if they want the number of classes taught by the faculty displayed on the graph 
    or not. 
    """
    selected = ''
    global classCountSelection
    if classCount.get() == 1:
        classCountSelection = True
        print(classCountSelection)

    else: 
        classCountSelection = False
        print(classCountSelection)
    print(selectedDic)

def sub_select8():
    """
    sub_select8() takes in the users selection regarding if they want the default Natural Science Subjects List to choose from or if 
    they want the entire availble Course subjects provides by the database obtained via the Database Module 
    """
    global naturalONLY
    if NaturalS.get() == 1:
        naturalONLY = False 
        subMenu0.config(values=groupLS)
        print(f"NaturalS: {naturalONLY}")
    else:
        naturalONLY = True 
        subMenu0.config(values=NATURAL_SCIENCE)
        print(f"NaturalS: {naturalONLY}")
    print(selectedDic)

def sub_select9():
    """
    sub_select9() takes in the users input regarding if they want the default option of instructor names on the x-axis of the graph
    or if they desire to see course on the x-axis. This toggle is important when selecting class_level_dept graphs or department graph types
    """
    global xaxis
    if xaxisToggle.get() == 1:
        xaxis = True
        print(f"X-axis: {xaxis}")
    else:
        xaxis = False
        print(f"X-axis: {xaxis}")
    print(selectedDic)

def aboutPage():
    """
    aboutPage() contains the logic needed to display the about page that has the names of group members of this project and the source that
    was used to populate the database and a disclaimer regarding the available data that is used by the EasyA software 
    It also cites the Project 1 doc 
    """
    global color_Mode
    aPbg = navbg
    if color_Mode == False:
        aPbg = darkslabbg
    else:
        aPbg = navbg

    windH = root.winfo_height()
    aboutFrame = tk.Frame(root, bg=aPbg) 
    logoBarFiller = tk.Frame(aboutFrame, bg=aPbg, height=60)
    backButton = tk.Button(aboutFrame, text="X", bg=aPbg, command=lambda: [aboutFrame.destroy()] )
    aboutLabel = tk.Label(aboutFrame, bg=aPbg, text="About", font=('Helvetica 20'))
    textBlock = tk.Text(aboutFrame, width=40, wrap="word", font=('Helvetica 12'))
    text="""
EasyA software was built by:

Daniel Willard
Freddy Lopez
Jacob Burke
Simon Zhao

Sources:
classes.cs.uoregon.edu/24W/cs422/P1/Project_1_Document.pdf
Author: Prof. Anthony Hornof
Date: 01/09/2024


DISCLAIMER:

If your class doesn't show up here, it means the data was redacted. Data from 67 percent of the 48,309 classes was redacted by the UO Public Records Office and is not diplayed here. Upon inquiry about the removed data, the office cited three conditions which must be met in order to release grade data without violating student privacy via the Family Education Rights and Privacy Act (FERPA)

The numbers are reflections only of students who received letter grades

1) The actual class enrollment must be greater than or equal to ten students
2) All students in the class do not receive the same grade 
3) A person would need to figure out the grades of at least six students in the class to deduce the grades of other students.(In other words, a class redacted for this reason - whether a class of 10 or 300 - awarded every student the same grade except for five or fewer students)

27,013 classes were redacted solely for the first condition. 5,737 classes were redacted because it met the second two conditions

In the creation of this software, the group did not include Pass/No Pass grades given in the remaining unredacted classes.
    """






    logoBarFiller.grid(row=0, column=0, sticky="ew", pady=70)
    aboutFrame.place(height=windH, width=400)
    backButton.grid(row=0, column=0, sticky='w')
    aboutLabel.grid(row=1,column=0, padx=20, pady=20)

    textBlock.grid(row=2, column=0, padx=8)
    textBlock.insert(INSERT, text)
    logoBar.tkraise()


# Create root Window for the GUI
global root
root = tk.Tk()
root.tk.call("source", "assets/Azure-ttk-theme-main/azure.tcl")
root.tk.call("set_theme", "light")
root.title("Easy A")
root.eval("tk::PlaceWindow . center")
root.geometry("800x750")
#root.configure(bg=rootbg)



# Create toplevel frame for the result window that will display graphs 
# resWindow.grid(row=0, column=20)
# Redesigning the base frames slightly

onjpg = PhotoImage(file= "assets/icons8-toggle-on-50.png") 
offjpg = PhotoImage(file="assets/icons8-toggle-off-50.png")



logoBar = tk.Frame(root, bg=logobg, height=60)
#paddLab = tk.Label(logoBar, text="", bg=logobg)
#paddLab.grid(row=1, column=2, padx=240, pady=8)
toggleB = tk.Button(logoBar, image=offjpg, background=logobg, bd=0, command=toggle)
toggleB.pack(side="right", expand=False, anchor='e', ipadx=15, ipady=10) 
toggleLab = tk.Label(logoBar, text="Light/Dark Mode:", bg=logobg)
toggleLab.pack(side="right", fill="x", expand=False, anchor='e', ipadx=15, ipady=10)
#toggleLab.grid(row=1, column=2, padx=10, pady=8, sticky='e')
#toggleB.grid(row=1, column=3, padx=2, pady=8, sticky='ne')


# This is the Logo that I created in Adobe Illistrator

logoFrame = tk.Frame(root, bg=logobg, height=50)
logoImg = Image.open("assets/EasyA.png")
logoS = logoImg.resize((100, 40))
#logo = ImageTk.PhotoImage(file="assets/EasyA.png")
logo = ImageTk.PhotoImage(logoS)
logo_widget = tk.Label(logoBar, image=logo, bg=logobg)
logo_widget.pack(side="left", expand=False, anchor='w', ipadx=15, ipady=10)
#logo_widget.grid(row=1, column=1, padx=5, pady=8)



main = tk.PanedWindow(root, bg=navbg)
"""
NavBar = tk.Frame(main, bg="#99fb99", width=100)
subMain = tk.PanedWindow(root, bg="#FFF", width=200))
main.add(NavBar)
main.add(subMain)
"""

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
logoBar.grid(row=0, column=0, sticky="ew")
main.grid(row=1, column=0, sticky="nsew")


NavBar = tk.Frame(main, bg=navbg, width=100)
subMain = tk.Frame(root, bg=submainbg, width=200)
# resFrame = tk.Frame(main, bg=submainbg)

"""
All tk.IntVar() variables used to track user checkbox selection  
"""
var1 = tk.IntVar()
var2 = tk.IntVar()
classCount = tk.IntVar()
NaturalS = tk.IntVar()
xaxisToggle = tk.IntVar()

"""
All of the Initialization of tkinter Labels, Buttons, Checkboxes, and images displayed. These are then called by firstsubMainPage() function in order to
actually place the objects on the screen for the user to see anf interact 
"""
NaturalScience = Checkbutton(subMain, text="Include all courses", bg=submainbg, variable=NaturalS, onvalue=1, offvalue=0, command=sub_select8)
subjL = tk.Label(subMain, text="Subject: ", bg=submainbg)
classL = tk.Label(subMain, text="Course Level: ", bg=submainbg)
courseL= tk.Label(subMain, text="Course Name: ", bg=submainbg)
instructL = tk.Label(subMain, text="Instructor: ", bg=submainbg)
graphTypeL = tk.Label(subMain, text="Graph Type: ", bg=submainbg)
ClassCount = tk.Checkbutton(subMain, text="Class Count", bg=submainbg, variable=classCount, onvalue=1, offvalue=0, command=sub_select7)
Xaxis = tk.Checkbutton(subMain, text="Label courses on x-axis", bg=submainbg, variable=xaxisToggle, onvalue=1, offvalue=0, command=sub_select9)
PassTypeL = tk.Label(subMain, text="EasyA/Pass: ", bg=submainbg)
PassTypeL0 = tk.Radiobutton(subMain, text="A", bg=submainbg, variable=var1, value=1, command=sub_select6)
PassTypeL1 = tk.Radiobutton(subMain, text="D/F", bg=submainbg, variable=var1, value=2, command=sub_select6)

# Placeing custom logo on the screen 
logoImgv2 = Image.open("assets/EasyA.png")
logoS2 = logoImgv2.resize((90, 35))
#logo = ImageTk.PhotoImage(file="assets/EasyA.png")
logo2 = ImageTk.PhotoImage(logoS2)
logo_widget2 = tk.Label(subMain, image=logo2, bg=submainbg)


varSelect = StringVar(subMain)
# Creating the Comboboxes for dropdown selection 
subMenu0 = ttk.Combobox(subMain, textvariable=varSelect, values=NATURAL_SCIENCE)
subMenu0.bind("<<ComboboxSelected>>", sub_select0)
subMenu1 = ttk.Combobox(subMain, values=TEMP_OPT, state=menuState)
subMenu1.bind("<<ComboboxSelected>>", sub_select1)
subMenu2 = ttk.Combobox(subMain, values=courselvlList, state=menuState)
subMenu2.bind("<<ComboboxSelected>>", sub_select2)
subMenu4 = ttk.Combobox(subMain, values=FACULTY_OPT, state=menuState)
subMenu4.bind("<<ComboboxSelected>>", sub_select4)
subMenu5 = ttk.Combobox(subMain, values=GRAPH_TYPE, state=menuState)
subMenu5.bind("<<ComboboxSelected>>", sub_select5)


canvas = Canvas(subMain, width=100, height=10)
submitBttn = ttk.Button(subMain, text="Submit", command=lambda: [submitQuery()])
canvas = Canvas(subMain, width=100, height=10)
canvas1 = Canvas(subMain, width=100, height=10)
clearBttn = ttk.Button(subMain, text="Reset All", command=clearBox)

slab1 = tk.Button(NavBar, text="About", bg=navbg, command=aboutPage, font=("Adobe Caslon Pro", 8))
slab2 = tk.Label(NavBar, text="GitHub", bg=navbg, cursor="hand2", font=("Adobe Caslon Pro", 8))
slab3 = tk.Label(NavBar, text="Data Source", bg=navbg, cursor="hand2", font=("Adobe Caslon Pro", 8))
sExitbuttn = ttk.Button(NavBar, text="Quit EasyA", command=closeGUI)


    
    



def firstsubMainPage():
    # This funciton contains all of the positioning of the tkinter objects displayed on the the GUI
    # For this specific GUI, I chose to use the .grid() method to accuratly place objects on the screen. 

    NaturalScience.grid(row=2, column=1, ipadx=20, ipady=5)
   
    subjL.grid(row=3, column=1, ipadx=20, ipady=5)

    classL.grid(row=4, column=1, ipadx=20, ipady=5)  

    courseL.grid(row=5, column=1, ipadx=20, ipady=5) 

    instructL.grid(row=6, column=1, ipadx=20, ipady=5) 

    ClassCount.grid(row=9, column=1, ipadx=20, ipady=5)

    Xaxis.grid(row=9, column=2, ipadx=20, ipady=5)

    PassTypeL.grid(row=8, column=1, ipadx=0, ipady=5) 

    logo_widget2.grid(row=1, column=1, padx=30, pady=20, sticky="nsew")

    subMenu0.grid(row=3, column=2, padx=10, pady=10)

    subMenu1.grid(row=4, column=2, padx=10, pady=10)

    subMenu2.grid(row=5, column=2, padx=10, pady=10)

    subMenu4.grid(row=6, column=2, padx=10, pady=10)
    subMenu4.set('All Instructors')

    PassTypeL0.grid(row=8, column=2, padx=0, pady=10)
    PassTypeL1.grid(row=8, column=3, padx=0, pady=10)

    canvas.grid(row=11, column=2, padx=10, pady=10)

    submitBttn.grid(row=12, column=2, padx=10, pady=10) 

    canvas1.grid(row=11, column=1, padx=10, pady=10)

    clearBttn.grid(row=12, column=1, padx=10, pady=10)

    main.add(NavBar, stretch="never")
    main.add(subMain)


    # Labels that will turn into clickable buttons that will take you to the desired screen and information

    slab1.grid(row=1, column=1, padx=5, pady=40)
    slab1.bind("<Button-1>", lambda e: aboutPage())

    slab2.grid(row=2, column=1, padx=5, pady=40)
    slab2.bind("<Button-1>", lambda e: openWeb("https://github.com/freddy-lopez01/Project-1-EasyA"))

    slab3.grid(row=3, column=1, padx=5, pady=40)
    slab3.bind("<Button-1>", lambda e: openWeb("https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/"))

    sExitbuttn.grid(row=8, column=1, padx=5, pady=80)


firstsubMainPage()
root.mainloop()

