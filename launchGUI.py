import tkinter as tk
from tkinter import *
from tkinter import font, ttk, StringVar, Button, Canvas 
from PIL import ImageTk, Image
import array
import webbrowser

# Color pallete used in GUI

color_Mode = True

logobg = "#eaddcf"
navbg = "#e3f6f5"
sideBarbg = "#"
#submainbg = "#3f3f46"

submainbg = "#fef6e4"
darksubmainbg = "#242424"
darkslabbg = "#787878"

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




# Create root Window for the GUI
root = tk.Tk()
root.tk.call("source", "assets/Azure-ttk-theme-main/azure.tcl")
root.tk.call("set_theme", "light")
root.title("Easy A")
root.eval("tk::PlaceWindow . center")
root.geometry("600x850")
#root.configure(bg=rootbg)



# Create toplevel frame for the result window that will display graphs 

#resWindow.grid(row=0, column=0, sticky="nsew")
# Redesigning the base frames slightly

onjpg = PhotoImage(file= "assets/icons8-toggle-on-50.png") 
offjpg = PhotoImage(file="assets/icons8-toggle-off-50.png")

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
        facultyL.config(bg=submainbg)
        instructL.config(bg=submainbg)
        graphTypeL.config(bg=submainbg)
        PassTypeL.config(bg=submainbg)
        logo_widget2.config(bg=submainbg)
        slab1.config(bg=navbg)
        slab2.config(bg=navbg)
        slab3.config(bg=navbg)
        NavBar.config(bg=navbg)
        color_Mode = True

    else:
        toggleB.config(image=onjpg)
        change_theme() 
        subMain.config(bg=darksubmainbg)
        subjL.config(bg=darksubmainbg)
        classL.config(bg=darksubmainbg)
        courseL.config(bg=darksubmainbg)
        facultyL.config(bg=darksubmainbg)
        instructL.config(bg=darksubmainbg)
        graphTypeL.config(bg=darksubmainbg)
        PassTypeL.config(bg=darksubmainbg)
        logo_widget2.config(bg=darksubmainbg)
        slab1.config(bg=darkslabbg)
        slab2.config(bg=darkslabbg)
        slab3.config(bg=darkslabbg)
        NavBar.config(bg=darkslabbg)
        color_Mode = False

logoBar = tk.Frame(root, bg=logobg, height=60)
paddLab = tk.Label(logoBar, text="", bg=logobg)
paddLab.grid(row=1, column=2, padx=140, pady=8)
toggleLab = tk.Label(logoBar, text="Light/Dark Mode:", bg=logobg)
toggleLab.grid(row=1, column=3, padx=10, pady=8)
toggleB = Button(logoBar, image=offjpg, background=logobg, bd=0, command=toggle)
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
subMain = tk.PanedWindow(root, bg=submainbg, width=200)


if color_Mode == False:
    subMain.config(bg=darksubmainbg)
    subjL.config(bg=darksubmainbg)





# Contrary to the name subMain, this window will hold the bulk of the interation that the user will have with the GUI

subjL = tk.Label(subMain, text="Subject: ", bg=submainbg)
subjL.grid(row=2, column=1, ipadx=20, ipady=5)

classL = tk.Label(subMain, text="Course Level: ", bg=submainbg)
classL.grid(row=3, column=1, ipadx=20, ipady=5)  

courseL= tk.Label(subMain, text="Course: ", bg=submainbg)
courseL.grid(row=4, column=1, ipadx=20, ipady=5) 

facultyL = tk.Label(subMain, text="Faculty: ", bg=submainbg)
facultyL.grid(row=5, column=1, ipadx=20, ipady=5) 

instructL = tk.Label(subMain, text="Instructor: ", bg=submainbg)
instructL.grid(row=6, column=1, ipadx=20, ipady=5) 

graphTypeL = tk.Label(subMain, text="Graph Type ", bg=submainbg)
graphTypeL.grid(row=7, column=1, ipadx=20, ipady=5) 


PassTypeL = tk.Label(subMain, text="EasyA/Pass ", bg=submainbg)
PassTypeL.grid(row=8, column=1, ipadx=20, ipady=5) 



if color_Mode == False:
    subMain.config(bg=darksubmainbg)
    subjL.config(bg=darksubmainbg)
    subjL.update_idletasks()




def toggle():
    global color_Mode

    if color_Mode == False:
        toggleB.config(image=offjpg)
        change_theme()
        subMain.config(bg=submainbg)
        subjL.config(bg=submainbg)
        color_Mode = True

    else:
        toggleB.config(image=onjpg)
        change_theme()        
        subMain.config(bg=darksubmainbg)
        subjL.config(bg=darksubmainbg)
        color_Mode = False













# For some reason the passing of the Combobox object as an Argument 
# did not parse correctly therefore the modulariy is exaggerated

selectedList = []
def sendSelected(data):
    selectedList.append(data)
    print(f"New array: {selectedList}")


def sub_select0(event):
    selected = subMenu0.get()
    print(selected)
    sendSelected(selected)

def sub_select1(event):
    selected = subMenu1.get()
    print(selected)
    sendSelected(selected)

def sub_select2(event):
    selected = subMenu2.get()
    print(selected)
    sendSelected(selected)


def sub_select3(event):
    selected = subMenu3.get()
    print(selected)
    sendSelected(selected)

def sub_select4(event):
    selected = subMenu4.get()
    print(selected)
    sendSelected(selected)


def sub_select5(event):
    selected = subMenu5.get()
    print(selected)
    sendSelected(selected)


def sub_select6(event):
    selected = subMenu6.get()
    print(selected)
    sendSelected(selected)

#varSelect = StringVar(subMain)
#varSelect.set(TEMP_OPT[0])
logoImgv2 = Image.open("assets/EasyA.png")
logoS2 = logoImgv2.resize((90, 35))
#logo = ImageTk.PhotoImage(file="assets/EasyA.png")
logo2 = ImageTk.PhotoImage(logoS2)
logo_widget2 = tk.Label(subMain, image=logo2, bg=submainbg)
logo_widget2.grid(row=1, column=1, padx=30, pady=20, sticky="nsew")

varSelect = StringVar(subMain)
#varSelect.set(TEMP_OPT[0])

def clearBox():
    """menuNum = Num
    if menuNum == 0:
        subMenu0.set('')
    elif memuNum == 1:
        subMenu1.set('')
    elif memuNum == 2:
        subMenu2.set('')
    elif memuNum == 3:
        subMenu3.set('')
    elif memuNum == 5:
        subMenu4.set('')
    elif memuNum == 6:
        subMenu5.set('')
    elif memuNum == 7:
        subMenu6.set('')
    else:"""
    subMenu0.set('')
    subMenu1.set('')
    subMenu2.set('')
    subMenu3.set('')
    subMenu4.set('')
    subMenu5.set('')
    subMenu6.set('')
    selectedList.clear()


subMenu0 = ttk.Combobox(subMain, textvariable=varSelect, values=TEMP_OPT)
subMenu0.bind("<<ComboboxSelected>>", sub_select0)
subMenu0.grid(row=2, column=2, padx=10, pady=10)


subMenu1 = ttk.Combobox(subMain, values=TEMP_SUB)
subMenu1.bind("<<ComboboxSelected>>", sub_select1)
subMenu1.grid(row=3, column=2, padx=10, pady=10)


subMenu2 = ttk.Combobox(subMain, values=TEMP_OPT)
subMenu2.bind("<<ComboboxSelected>>", sub_select2)
subMenu2.grid(row=4, column=2, padx=10, pady=10)


subMenu3 = ttk.Combobox(subMain, values=TEMP_OPT)
subMenu3.bind("<<ComboboxSelected>>", sub_select3)
subMenu3.grid(row=5, column=2, padx=10, pady=10)


subMenu4 = ttk.Combobox(subMain, values=TEMP_OPT)
subMenu4.bind("<<ComboboxSelected>>", sub_select4)
subMenu4.grid(row=6, column=2, padx=10, pady=10)


subMenu5 = ttk.Combobox(subMain, values=TEMP_OPT)
subMenu5.bind("<<ComboboxSelected>>", sub_select5)
subMenu5.grid(row=7, column=2, padx=10, pady=10)


subMenu6 = ttk.Combobox(subMain, values=TEMP_OPT)
subMenu6.bind("<<ComboboxSelected>>", sub_select5)
subMenu6.grid(row=8, column=2, padx=10, pady=10)


# Function for submitBttn Button Action
def submitQuery():
    print(f"Submitting complete query: {selectedList}")
    #resWindow.tkraise()


# Submit Button to submit complete query to database API

canvas = Canvas(subMain, width=100, height=10)
canvas.grid(row=10, column=2, padx=10, pady=10)


submitBttn = ttk.Button(subMain, text="Submit", command=lambda: [submitQuery(), resWindow.tkraise()])
submitBttn.grid(row=11, column=2, padx=10, pady=10) 


canvas = Canvas(subMain, width=100, height=10)
canvas.grid(row=10, column=1, padx=10, pady=10)

clearBttn = ttk.Button(subMain, text="Reset All", command=clearBox)
clearBttn.grid(row=11, column=1, padx=10, pady=10)

main.add(NavBar)
main.add(subMain)

#Creating the side labels into links that will take the user to the GitHub repo and source data URL


def openWeb(link):
    webbrowser.open_new(link)

# Labels that will turn into clickable buttons that will take you to the desired screen and information

slab1 = tk.Label(NavBar, text="About", bg=navbg, cursor="hand2", font=("Adobe Caslon Pro", 8))
slab1.grid(row=1, column=1, padx=5, pady=40)
#slab1.bind("<Button-1>", lambda e: openWeb("https://github.com/freddy-lopez01/Project-1-EasyA"))

slab2 = tk.Label(NavBar, text="GitHub", bg=navbg, cursor="hand2", font=("Adobe Caslon Pro", 8))
slab2.grid(row=2, column=1, padx=5, pady=40)
slab2.bind("<Button-1>", lambda e: openWeb("https://github.com/freddy-lopez01/Project-1-EasyA"))

slab3 = tk.Label(NavBar, text="Data Source", bg=navbg, font=("Adobe Caslon Pro", 8))
slab3.grid(row=3, column=1, padx=5, pady=40)



def closeGUI():
    root.destroy()


sExitbuttn = ttk.Button(NavBar, text="Quit EasyA", command=closeGUI)
sExitbuttn.grid(row=8, column=1, padx=5, pady=80)



root.mainloop()
