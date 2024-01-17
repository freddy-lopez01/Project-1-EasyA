import tkinter as tk 
from tkinter import font, ttk 
from PIL import ImageTk, Image


# Color pallete used in GUI
logobg = "#a3a3a3"
navbg = "#374151"
sideBarbg = "#52525b"
submainbg = "#3f3f46"


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
root.tk.call("set_theme", "dark")
root.title("Easy A")
root.eval("tk::PlaceWindow . center")
root.geometry("500x600")
#root.configure(bg=rootbg)


# Redesigning the base frames slightly 

logoBar = tk.Frame(root, bg=logobg, height=60)

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


NavBar = tk.Frame(main, bg=navbg, width=100)
subMain = tk.PanedWindow(root, bg=submainbg, width=200)

# Contrary to the name subMain, this window will hold the bulk of the interation that the user will have with the GUI

subjL = tk.Label(subMain, text="Subject Code: ", bg=submainbg).grid(row=2, column=1, ipadx=20, ipady=5)
classL = tk.Label(subMain, text="Course Level: ", bg=submainbg).grid(row=3, column=1, ipadx=20, ipady=5)  

instructL = tk.Label(subMain, text="Instructor: ", bg=submainbg).grid(row=4, column=1, ipadx=20, ipady=5) 



def sub_select(event):
    print("Selection was made\n")


#subselect = StringVar(subMain)
#subselect.select(TEMP_OPT[0])

logoImgv2 = Image.open("assets/EasyA.png")
logoS2 = logoImgv2.resize((90, 35))
#logo = ImageTk.PhotoImage(file="assets/EasyA.png")
logo2 = ImageTk.PhotoImage(logoS2)
logo_widget2 = tk.Label(subMain, image=logo2, bg=submainbg)
logo_widget2.grid(row=1, column=1, padx=30, pady=20, sticky="nsew")

subMenu = ttk.Combobox(subMain, values=TEMP_OPT)
subMenu.bind("<<ComboboxSelected>>", sub_select)
subMenu.grid(row=2, column=2, padx=10, pady=10)


subMenu1 = ttk.Combobox(subMain, values=TEMP_SUB)
subMenu1.bind("<<ComboboxSelected>>", sub_select)
subMenu1.grid(row=3, column=2, padx=10, pady=10)


subMenu2 = ttk.Combobox(subMain, values=TEMP_OPT)
subMenu2.bind("<<ComboboxSelected>>", sub_select)
subMenu2.grid(row=4, column=2, padx=10, pady=10)


main.add(NavBar)
main.add(subMain)



# Labels that will turn into clickable buttons that will take you to the desired screen and information
slab1 = tk.Label(NavBar, text="About", bg=navbg, fg="white", font=("Adobe Caslon Pro", 8))
slab1.grid(row=1, column=1, padx=5, pady=40)


slab2 = tk.Label(NavBar, text="Updates", bg=navbg, fg="white", font=("Adobe Caslon Pro", 8))
slab2.grid(row=2, column=1, padx=5, pady=40)


slab3 = tk.Label(NavBar, text="Data Source", bg=navbg, fg="white", font=("Adobe Caslon Pro", 8))
slab3.grid(row=3, column=1, padx=5, pady=40)






root.mainloop()
