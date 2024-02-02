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






#
# Global variables
#
color_Mode = True #This represents whether the user chooses the UI to be in light or dark mode. If true light mode, false for darkmode 
classCountSelection = False #Represents if the user wishes to have Class count on or off. False for off, True for on 
is_data = False 
box_state = False
selectedDic = {}
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


#
# Connecting to the database in order to create dynamic dropdown options
#
courseOPT = []
conn = sqlite3.connect('assets/CompleteDatabase.sqlite')
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
    global courselvlList
    courselvlList.clear()
    #fetcher = DataFetcher(CourseLvl, path)
    conn2 = sqlite3.connect('./Databases/GradeDatabase.sqlite')
    cursor2 = conn2.cursor()
    cursor2.execute("""SELECT group_code from 'course_data';""")

    # cursor2.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    data2 = cursor2.fetchall()
    #print(data2)
    codeTemplate = str(Subject)+str(CourseLvl[0])
    print(codeTemplate)
    for sub in data2:
        code = sub[0]
        if codeTemplate in code:
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
    # subMenu1.config(values=courselvlList)



# print(courselvlList)

# coursePopulate('CIS', '400')
print(courselvlList)
        





# Lists used by combobox

NATURAL_SCIENCE = ['BI Biology', 'CH Chemistry and Biochemistry', 'CIS Computer and Information Science', 'ERTH Earth Sciences', 'General Science Program', 'HPHY Human Physiology', 'MATH Mathematics', 'Neuroscience', 'PHYS Physics', 'PSY Psychology']

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



"""
ResWindow function that displays user selections and the graph that was generated. 
"""

def ResWindow(mode=0):
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
    header = tk.Label(selectFrame, text="Selections Made:", font='Helvetica 10 bold',bg=resbg)


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
        selectedDic.clear()

        

    ###
    # fig = Figure(figsize=(5,5), dpi=65)
    # #dummy test plot 
    # y = [1**2 for i in range(101)]
    # plot1 = fig.add_subplot(111)
    # plot1.plot(y)
    print("before displaySelect")
    # selectFrame.grid(row=0, column=2)
    displaySelect()
    selectFrame.grid(row=0, column=2)
    resFrame.place(height=windH, width=700)
    # graph.main(selectedDic)
    print("after displaySelect")


    # selectFrame.grid(row=0, column=2)
    # graph.main(selectedDic)

    # ax.plot()
    # canvas.draw()
    # canvas = FigureCanvasTkAgg(fig, master=resFrame) 
    # canvas.get_tk_widget().grid(row=0, column=0)
    ###

    # resFrame.place(height=windH, width=700)
    backButton = tk.Button(resFrame, text="New Query", command=lambda: [resFrame.destroy(), clearBox()])
    main.add(resFrame)
    backButton.grid(row=1, column=0, sticky='w', padx=20, pady=20)



"""
Window Class used in order to create warning popup window
"""
class Win:
    def popup(self, alertM=""):
        tk.Tk().withdraw()
        name = messagebox.showinfo(title="Warning", message=alertM)


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


def submitQuery():
    if (var1.get() == 0) and (var2.get() == 0) and (len(selectedDic) == 0):
        win = Win()
        win.popup("Must Select Subject and EasyA/Pass Field in order to submit")
        return 0
    elif (var1.get() == 0) and (var2.get() == 0) and (len(selectedList) > 0):
        win = Win()
        win.popup("Must Select either A or D/F")
    else:
        global xaxis
        global color_Mode
        selectedList.append(gradeSel)
        if "instructor_type" not in selectedDic:
            selectedDic["instructor_type"] = "All Instructors"
        selectedDic["grade_type"] = gradeSel
        selectedDic["class_count"] = classCountSelection
        selectedDic["xaxis_course"] = xaxis
        selectedDic["light_mode"] = color_Mode
        #print(f"Submitting complete query: {selectedList}")
        print(f"Submitting complete query: {selectedDic}")
        ResWindow()
        #resWindow.tkraise()

def clear(object):
    slaves = object.grid_slaves()
    for x in slaves:
        x.destroy()

def openWeb(link):
    webbrowser.open_new(link)

def clearBox():
    global selectedDic
    global classCountSelection
    global NaturalONLY
    global xaxis
    global courselvlList

    subMenu0.set('')
    subMenu1.set('')
    subMenu2.set('')
    # subMenu3.set('')
    subMenu4.set('All Instructors')
    subMenu5.set('')
    NaturalScience.deselect()
    subMenu0.config(values=groupLS)
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
    if root.tk.call("ttk::style", "theme", "use")=="azure-dark":
        root.tk.call("set_theme", "light")
    else:
        root.tk.call("set_theme", "dark")

def toggle():
    global color_Mode

    if color_Mode == False:
        toggleB.config(image=offjpg)
        change_theme()
        subMain.config(bg=submainbg)
        #subjL.config(bg=submainbg)
        NaturalScience.config(bg=submainbg)
        subjL.config(bg=submainbg)
        classL.config(bg=submainbg)
        courseL.config(bg=submainbg)
        graphTypeL.config(bg=submainbg)
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
        paddLab.config(bg=logobg)
        toggleLab.config(bg=logobg)
        toggleB.config(bg=logobg)
        logo_widget.config(bg=logobg)
        Xaxis.config(bg=submainbg)
        color_Mode = True
        #if ResWindow:
        #    ResWindow(mode=1)
        #    print("light mode")
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
        graphTypeL.config(bg=darksubmainbg)
        PassTypeL.config(bg=darksubmainbg)
        PassTypeL0.config(bg=darksubmainbg)
        PassTypeL1.config(bg=darksubmainbg)
        logo_widget2.config(bg=darksubmainbg)
        slab1.config(bg=darkslabbg)
        slab2.config(bg=darkslabbg)
        slab3.config(bg=darkslabbg)
        NavBar.config(bg=darkslabbg)
        logoBar.config(bg=darklogobg)
        paddLab.config(bg=darklogobg)
        toggleLab.config(bg=darklogobg)
        toggleB.config(bg=darklogobg)
        logo_widget.config(bg=darklogobg)
        Xaxis.config(bg=darksubmainbg)
        color_Mode = False
        #if ResWindow:
        #    ResWindow(mode=1)
        #    print("dark mode")
        print(f"Global ColorMode: {color_Mode}\n")

def closeGUI():
    conn.close()
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
    global currCourseLvl
    global currSubject
    global selectedDic
    selected = subMenu1.get()
    if selected == "All Courses":
        selectedDic['class_level'] = selectedDic['Subject']
    else:
        selectedDic["class_level"] = selected
    print(selected)
    currCourseLvl = selected
    coursePopulate(currSubject, currCourseLvl)
    subMenu2.config(values=courselvlList)
    subMenu2.set('')
    print(selectedDic)

def sub_select2(event):
    selected = subMenu2.get()
    print(selected)
    if "selected" in str(selected): 
        selectedDic["class_code"] = selectedDic['Subject']
    else:
        selectedDic["class_code"] = selected
    sendSelected(selected)
    #selectedDic["class_code"] = selected
    print(selectedDic)

def sub_select4(event):
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
    selected = ''
    global gradeSel
    if (var1.get() == 1) and (var2.get() == 1):
        print("error: cannot choose both options in same query")
        win = Win()
        win.popup("Must Select either A or D/F. User cannot select both")
        PassTypeL0.deselect()
        PassTypeL1.deselect()
        return 0
    elif (var2.get() == 0) and (var1.get() == 1):
        selected = 'Percent As'
    elif (var2.get() == 1) and (var1.get() == 0):
        selected = 'Percent Ds/Fs'
    else:
        print("error: Must select either A or D/F to submit query")
        win = Win()
        win.popup("Must Select either A or D/F")
        PassTypeL0.deselect()
        PassTypeL1.deselect()
        return 0
    print(f"seleted in subselect6: {selected}")
    gradeSel = selected
    print(selectedDic)

def sub_select7():
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
    global naturalONLY
    if NaturalS.get() == 1:
        naturalONLY = True
        subMenu0.config(values=groupLS)
        print(f"NaturalS: {naturalONLY}")
    else:
        naturalONLY = False
        subMenu0.config(values=NATURAL_SCIENCE)
        print(f"NaturalS: {naturalONLY}")
    print(selectedDic)

def sub_select9():
    global xaxis
    if xaxisToggle.get() == 1:
        xaxis = True
        print(f"X-axis: {xaxis}")
    else:
        xaxis = False
        print(f"X-axis: {xaxis}")
    print(selectedDic)


# Create root Window for the GUI
global root
root = tk.Tk()
root.tk.call("source", "assets/Azure-ttk-theme-main/azure.tcl")
root.tk.call("set_theme", "light")
root.title("Easy A")
root.eval("tk::PlaceWindow . center")
root.geometry("900x850")
#root.configure(bg=rootbg)



# Create toplevel frame for the result window that will display graphs 
# resWindow.grid(row=0, column=20)
# Redesigning the base frames slightly

onjpg = PhotoImage(file= "assets/icons8-toggle-on-50.png") 
offjpg = PhotoImage(file="assets/icons8-toggle-off-50.png")



logoBar = tk.Frame(root, bg=logobg, height=60)
paddLab = tk.Label(logoBar, text="", bg=logobg)
paddLab.grid(row=1, column=2, padx=240, pady=8)
toggleLab = tk.Label(logoBar, text="Light/Dark Mode:", bg=logobg)
toggleLab.grid(row=1, column=3, padx=10, pady=8)
toggleB = tk.Button(logoBar, image=offjpg, background=logobg, bd=0, command=toggle)
toggleB.grid(row=1, column=4, padx=2, pady=8)


# This is the Logo that I created in Adobe Illistrator

logoFrame = tk.Frame(root, bg=logobg, height=50)
logoImg = Image.open("assets/EasyA.png")
logoS = logoImg.resize((100, 40))
#logo = ImageTk.PhotoImage(file="assets/EasyA.png")
logo = ImageTk.PhotoImage(logoS)
logo_widget = tk.Label(logoBar, image=logo, bg=logobg)
logo_widget.grid(row=1, column=1, padx=5, pady=8)



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


NavBar = tk.Frame(main, bg=navbg, width=70)
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
PassTypeL0 = tk.Checkbutton(subMain, text="A", bg=submainbg, variable=var1, onvalue=1, offvalue=0, command=sub_select6)
PassTypeL1 = tk.Checkbutton(subMain, text="D/F", bg=submainbg, variable=var2, onvalue=1, offvalue=0, command=sub_select6)

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
#subMenu6 = ttk.Combobox(subMain, values=GRADE_OPT)
#subMenu6.bind("<<ComboboxSelected>>", sub_select6)


canvas = Canvas(subMain, width=100, height=10)
submitBttn = ttk.Button(subMain, text="Submit", command=lambda: [submitQuery()])
canvas = Canvas(subMain, width=100, height=10)
canvas1 = Canvas(subMain, width=100, height=10)
clearBttn = ttk.Button(subMain, text="Reset All", command=clearBox)
# nextBttn = ttk.Button(subMain, text="Next Page", command=ResWindow)

slab1 = tk.Label(NavBar, text="About", bg=navbg, cursor="hand2", font=("Adobe Caslon Pro", 8))
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

    graphTypeL.grid(row=7, column=1, ipadx=20, ipady=5) 

    ClassCount.grid(row=9, column=1, ipadx=20, ipady=5)

    Xaxis.grid(row=9, column=2, ipadx=20, ipady=5)

    PassTypeL.grid(row=8, column=1, ipadx=0, ipady=5) 

    logo_widget2.grid(row=1, column=1, padx=30, pady=20, sticky="nsew")

    subMenu0.grid(row=3, column=2, padx=10, pady=10)

    subMenu1.grid(row=4, column=2, padx=10, pady=10)

    subMenu2.grid(row=5, column=2, padx=10, pady=10)

    subMenu4.grid(row=6, column=2, padx=10, pady=10)
    subMenu4.set('All Instructors')

    subMenu5.grid(row=7, column=2, padx=10, pady=10)

    PassTypeL0.grid(row=8, column=2, padx=0, pady=10)
    PassTypeL1.grid(row=8, column=3, padx=0, pady=10)

    canvas.grid(row=11, column=2, padx=10, pady=10)

    submitBttn.grid(row=12, column=2, padx=10, pady=10) 

    canvas1.grid(row=11, column=1, padx=10, pady=10)

    clearBttn.grid(row=12, column=1, padx=10, pady=10)

    main.add(NavBar)
    main.add(subMain)


    # Labels that will turn into clickable buttons that will take you to the desired screen and information

    # slab1 = tk.Label(NavBar, text="About", bg=navbg, cursor="hand2", font=("Adobe Caslon Pro", 8))
    slab1.grid(row=1, column=1, padx=5, pady=40)
    slab1.bind("<Button-1>", lambda e: openWeb("https://github.com/freddy-lopez01/Project-1-EasyA"))

    # slab2 = tk.Label(NavBar, text="GitHub", bg=navbg, cursor="hand2", font=("Adobe Caslon Pro", 8))
    slab2.grid(row=2, column=1, padx=5, pady=40)
    slab2.bind("<Button-1>", lambda e: openWeb("https://github.com/freddy-lopez01/Project-1-EasyA"))

    # slab3 = tk.Label(NavBar, text="Data Source", bg=navbg, cursor="hand2", font=("Adobe Caslon Pro", 8))
    slab3.grid(row=3, column=1, padx=5, pady=40)
    slab3.bind("<Button-1>", lambda e: openWeb("https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/"))

    sExitbuttn.grid(row=8, column=1, padx=5, pady=80)


firstsubMainPage()
root.mainloop()

