import tkinter as tk
from tkinter import *
from tkinter import font, ttk, StringVar, Button, Canvas, messagebox 
from PIL import ImageTk, Image
import array
import webbrowser

# Color pallete used in GUI

color_Mode = True

is_data = False

box_state = False

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

#Temporary Lists to test dropdown box selections

TEMP_OPT = ["100", "200", "300", "400", "500"]
TEMP_SUB = ['AFR African Studies', 'ANTH Anthropology',
            'ASIA Asian Studies', 'BI Biology', 'CH Chemistry',
            'CINE Cinema Studies', 'CIS Computer and Information Science',
            'CIT Computer Information Technology', 'CLAS Classics', 'COLT Comparative Literature',
            'CRWR Creative Writing', 'EALL East Asian Languages and Literatures', 'EC Economics',
            'ENG English', 'ENVS Environmental Studies', 'ES Ethnic Studies', 'EURO European Studies',
            'FLR Folklore', 'GEOG Geography', 'GEOL Geological Sciences', 'GER German', 'HIST History',
            'HPHY Human Physiology', 'HUM Humanities', 'INTL International Studies', 'JDST Judaic Studies',
            'LA Landscape Architecture', 'LAS Latin American Studies', 'LING Linguistics', 'MATH Mathematics',
            'MDVL Medieval Studies', 'PHIL Philosophy', 'PHYS Physics', 'PS Political Science', 'PSY Psychology',
            'REES Russian and East European Studies', 'REL Religious Studies', 'RL Romance Languages', 'SCAN Scandinavian',
            'SOC Sociology', 'TA Theater Arts', "WGS Women's and Gender Studies"]

GRADE_OPT = ["A", "D/F"]

selectedDic = {}
selectedList = []
gradeSel = "A"
#    subMain.tkraise()

def ResWindow():
    # clear(subMain)
    resbg = ""
    windH = root.winfo_height()
    if color_Mode == False:
        resbg = darksubmainbg
    else:
        resbg = submainbg
    resFrame = tk.Frame(main, bg=resbg)

    resFrame.place(height=windH, width=700)
    test = tk.Label(resFrame, text="solid")
    backButton = tk.Button(resFrame, text="New Query", command=lambda: [resFrame.destroy(), clearBox()])
    main.add(resFrame)
    test.grid(row=0, column=0)
    backButton.grid(row=1, column=0)
class Win:
    def popup(self, alertM=""):
        tk.Tk().withdraw()
        name = messagebox.showinfo(title="Warning", message=alertM)
def submitQuery():
    if (var1.get() == 0) and (var2.get() == 0) and (len(selectedList) == 0):
        win = Win()
        win.popup("Must Select Subject and EasyA/Pass Field in order to submit")
        return 0
    elif (var1.get() == 0) and (var2.get() == 0) and (len(selectedList) > 0):
        win = Win()
        win.popup("Must Select either A or D/F")
    else:
        selectedList.append(gradeSel)
        selectedDic["GradeSel"] = gradeSel
        print(f"Submitting complete query: {selectedList}")
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
    subMenu0.set('')
    subMenu1.set('')
    subMenu2.set('')
    # subMenu3.set('')
    subMenu4.set('')
    subMenu5.set('')
    PassTypeL0.deselect()
    PassTypeL1.deselect()
    selectedDic.clear()
    box_state = False
    menuState='disabled'
    subMenu1.config(state=menuState)
    subMenu2.config(state=menuState)
    subMenu4.config(state=menuState)
    subMenu5.config(state=menuState)


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
        subjL.config(bg=submainbg)
        classL.config(bg=submainbg)
        courseL.config(bg=submainbg)
        #facultyL.config(bg=submainbg)
        instructL.config(bg=submainbg)
        graphTypeL.config(bg=submainbg)
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
        color_Mode = True
        print(f"Global ColorMode: {color_Mode}\n")

    else:
        toggleB.config(image=onjpg)
        change_theme() 
        subMain.config(bg=darksubmainbg)
        subjL.config(bg=darksubmainbg)
        classL.config(bg=darksubmainbg)
        courseL.config(bg=darksubmainbg)
        #facultyL.config(bg=darksubmainbg)
        instructL.config(bg=darksubmainbg)
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
        color_Mode = False
        print(f"Global ColorMode: {color_Mode}\n")

def closeGUI():
    root.destroy()
    exit()

def sendSelected(data):
    selectedList.append(data)
    print(f"New array: {selectedList}")
menuState = 'disabled'

def sub_select0(event):
    selected = subMenu0.get()
    print(selected)
    sendSelected(selected)
    selectedDic["Subject"] = selected
    box_state = True
    menuState = 'enabled'
    subMenu1.config(state=menuState)
    subMenu2.config(state=menuState)
    subMenu4.config(state=menuState)
    subMenu5.config(state=menuState)


def sub_select1(event):
    selected = subMenu1.get()
    print(selected)
    sendSelected(selected)
    selectedDic["CourseLevel"] = selected

def sub_select2(event):
    selected = subMenu2.get()
    print(selected)
    sendSelected(selected)
    selectedDic["CourseName"] = selected

def sub_select4(event):
    selected = subMenu4.get()
    print(selected)
    sendSelected(selected)
    selectedDic["Instructor"] = selected


def sub_select5(event):
    selected = subMenu5.get()
    print(selected)
    sendSelected(selected)


def sub_select6():
    selected = ''
    if (var1.get() == 1) and (var2.get() == 1):
        print("error: cannot choose both options in same query")
        win = Win()
        win.popup("Must Select either A or D/F")
        PassTypeL0.deselect()
        PassTypeL1.deselect()
        return 0
    elif (var2.get() == 0) and (var1.get() == 1):
        selected = 'A'
    elif (var2.get() == 1) and (var1.get() == 0):
        selected = 'D/F'
    else:
        print("error: Must select either A or D/F to submit query")
        win = Win()
        win.popup("Must Select either A or D/F")
        PassTypeL0.deselect()
        PassTypeL1.deselect()
        return 0
    print(selected)
    gradeSel = selected

# Create root Window for the GUI
global root
root = tk.Tk()
root.tk.call("source", "assets/Azure-ttk-theme-main/azure.tcl")
root.tk.call("set_theme", "light")
root.title("Easy A")
root.eval("tk::PlaceWindow . center")
root.geometry("800x850")
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
var1 = tk.IntVar()
var2 = tk.IntVar()


subjL = tk.Label(subMain, text="Subject: ", bg=submainbg)
classL = tk.Label(subMain, text="Course Level: ", bg=submainbg)
courseL= tk.Label(subMain, text="Course: ", bg=submainbg)
instructL = tk.Label(subMain, text="Instructor: ", bg=submainbg)
graphTypeL = tk.Label(subMain, text="Graph Type: ", bg=submainbg)
PassTypeL = tk.Label(subMain, text="EasyA/Pass: ", bg=submainbg)
PassTypeL0 = tk.Checkbutton(subMain, text="A", bg=submainbg, variable=var1, onvalue=1, offvalue=0, command=sub_select6)
PassTypeL1 = tk.Checkbutton(subMain, text="D/F", bg=submainbg, variable=var2, onvalue=1, offvalue=0, command=sub_select6)

logoImgv2 = Image.open("assets/EasyA.png")
logoS2 = logoImgv2.resize((90, 35))
#logo = ImageTk.PhotoImage(file="assets/EasyA.png")
logo2 = ImageTk.PhotoImage(logoS2)
logo_widget2 = tk.Label(subMain, image=logo2, bg=submainbg)


varSelect = StringVar(subMain)


subMenu0 = ttk.Combobox(subMain, textvariable=varSelect, values=TEMP_SUB)
subMenu0.bind("<<ComboboxSelected>>", sub_select0)
subMenu1 = ttk.Combobox(subMain, values=TEMP_OPT, state=menuState)
subMenu1.bind("<<ComboboxSelected>>", sub_select1)
subMenu2 = ttk.Combobox(subMain, values=TEMP_SUB, state=menuState)
subMenu2.bind("<<ComboboxSelected>>", sub_select2)
subMenu4 = ttk.Combobox(subMain, values=TEMP_OPT, state=menuState)
subMenu4.bind("<<ComboboxSelected>>", sub_select4)
subMenu5 = ttk.Combobox(subMain, values=TEMP_OPT, state=menuState)
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
    # Contrary to the name subMain, this window will hold the bulk of the interation that the user will have with the GUI

    # subjL = tk.Label(subMain, text="Subject: ", bg=submainbg)
    subjL.grid(row=2, column=1, ipadx=20, ipady=5)

    # classL = tk.Label(subMain, text="Course Level: ", bg=submainbg)
    classL.grid(row=3, column=1, ipadx=20, ipady=5)  

    # courseL= tk.Label(subMain, text="Course: ", bg=submainbg)
    courseL.grid(row=4, column=1, ipadx=20, ipady=5) 


    # instructL = tk.Label(subMain, text="Instructor: ", bg=submainbg)
    instructL.grid(row=5, column=1, ipadx=20, ipady=5) 

    # graphTypeL = tk.Label(subMain, text="Graph Type ", bg=submainbg)
    graphTypeL.grid(row=6, column=1, ipadx=20, ipady=5) 


    
    #PassTypeL0
    #PassTypeL = tk.Label(subMain, text="EasyA/Pass ", bg=submainbg)
    PassTypeL.grid(row=7, column=1, ipadx=0, ipady=5) 





    # For some reason the passing of the Combobox object as an Argument 
    # did not parse correctly therefore the modulariy is exaggerated

    # logoImgv2 = Image.open("assets/EasyA.png")
    # logoS2 = logoImgv2.resize((90, 35))
    # #logo = ImageTk.PhotoImage(file="assets/EasyA.png")
    # logo2 = ImageTk.PhotoImage(logoS2)
    # logo_widget2 = tk.Label(subMain, image=logo2, bg=submainbg)
    logo_widget2.grid(row=1, column=1, padx=30, pady=20, sticky="nsew")

    # varSelect = StringVar(subMain)


    # subMenu0 = ttk.Combobox(subMain, textvariable=varSelect, values=TEMP_SUB)
    # subMenu0.bind("<<ComboboxSelected>>", sub_select0)
    subMenu0.grid(row=2, column=2, padx=10, pady=10)


    # subMenu1 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu1.bind("<<ComboboxSelected>>", sub_select1)
    subMenu1.grid(row=3, column=2, padx=10, pady=10)

    # subMenu1 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu1.bind("<<ComboboxSelected>>", sub_select1)
    # subMenu2 = ttk.Combobox(subMain, values=TEMP_SUB)
    # subMenu2.bind("<<ComboboxSelected>>", sub_select2)
    subMenu2.grid(row=4, column=2, padx=10, pady=10)

    # subMenu1 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu1.bind("<<ComboboxSelected>>", sub_select1)
    # subMenu2 = ttk.Combobox(subMain, values=TEMP_SUB)
    # subMenu2.bind("<<ComboboxSelected>>", sub_select2)
    # subMenu4 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu4.bind("<<ComboboxSelected>>", sub_select4)
    subMenu4.grid(row=5, column=2, padx=10, pady=10)

    # subMenu1 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu1.bind("<<ComboboxSelected>>", sub_select1)
    # subMenu2 = ttk.Combobox(subMain, values=TEMP_SUB)
    # subMenu2.bind("<<ComboboxSelected>>", sub_select2)
    # subMenu4 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu4.bind("<<ComboboxSelected>>", sub_select4)
    # subMenu5 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu5.bind("<<ComboboxSelected>>", sub_select5)
    subMenu5.grid(row=6, column=2, padx=10, pady=10)

    # subMenu1 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu1.bind("<<ComboboxSelected>>", sub_select1)
    # subMenu2 = ttk.Combobox(subMain, values=TEMP_SUB)
    # subMenu2.bind("<<ComboboxSelected>>", sub_select2)
    # subMenu4 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu4.bind("<<ComboboxSelected>>", sub_select4)
    # subMenu5 = ttk.Combobox(subMain, values=TEMP_OPT)
    # subMenu5.bind("<<ComboboxSelected>>", sub_select5)
    # subMenu6 = ttk.Combobox(subMain, values=GRADE_OPT)
    # subMenu6.bind("<<ComboboxSelected>>", sub_select6)
    
    PassTypeL0.grid(row=7, column=2, padx=0, pady=10)
    PassTypeL1.grid(row=7, column=3, padx=0, pady=10)

    # resFrame = tk.Frame(main)

    # Submit Button to submit complete query to database API

    # canvas = Canvas(subMain, width=100, height=10)
    canvas.grid(row=10, column=2, padx=10, pady=10)

    # submitBttn = ttk.Button(subMain, text="Submit", command=lambda: [submitQuery(), resWindow.tkraise()])
    submitBttn.grid(row=11, column=2, padx=10, pady=10) 


    # canvas = Canvas(subMain, width=100, height=10)
    canvas1.grid(row=10, column=1, padx=10, pady=10)

    # clearBttn = ttk.Button(subMain, text="Reset All", command=clearBox)
    clearBttn.grid(row=11, column=1, padx=10, pady=10)

    # nextBttn = ttk.Button(subMain, text="Next Page", command=ResWindow)
    # nextBttn.grid(row=11, column=3, padx=10, pady=10)

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

