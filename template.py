import tkinter as tk
from tkinter import *
from tkinter import font, ttk, StringVar, Button, Canvas 
from PIL import ImageTk, Image
import array
import webbrowser


LARGE_FONT= ("Verdana", 12)
color_Mode = True

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



class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def toggle(self, cont):
        print("hello")


        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)


        onjpg = PhotoImage(file= "assets/icons8-toggle-on-50.png") 
        offjpg = PhotoImage(file="assets/icons8-toggle-off-50.png")
        color_Mode = True

        logobg = "#eaddcf"
        navbg = "#e3f6f5"
        sideBarbg = "#"
        #submainbg = "#3f3f46"

        submainbg = "#fef6e4"
        darksubmainbg = "#282828"
        darkslabbg = "#787878"
        darklogobg="#242424"

        logoBar = tk.Frame(self, bg=logobg, height=60)
        logoBar.grid(row=0, column=0, sticky="nsew")
        logoFrame = tk.Frame(logoBar, bg=logobg, height=50)
        # logoFrame.grid(row=0, column=0)
        logoImg = Image.open("assets/EasyA.png")
        logoS = logoImg.resize((100, 40))
        logo = ImageTk.PhotoImage(file="assets/EasyA.png")
        logo2 = ImageTk.PhotoImage(logoS)
        logo_widget = tk.Label(logoBar, image=logo2, bg=logobg)
        logo_widget.grid(row=0, column=0, padx=5, pady=8)

        
        paddLab = tk.Label(logoBar, text="", bg=logobg)
        paddLab.grid(row=0, column=2, padx=140, pady=8)
        toggleLab = tk.Label(logoBar, text="Light/Dark Mode:", bg=logobg)
        toggleLab.grid(row=0, column=3, padx=10, pady=8)
        toggleB = Button(logoBar, image=offjpg, background=logobg, command=lambda: controller.toggle())
        toggleB.grid(row=0, column=4, padx=2, pady=8)

        main = tk.PanedWindow(self, bg=navbg)
        # """
        #NavBar = tk.Frame(main, bg="#99fb99", width=100)
        # subMain = tk.PanedWindow(root, bg="#FFF", width=200))
        # main.add(NavBar)
        # main.add(subMain)
        # """

        #self.grid_rowconfigure(1, weight=1)
        #self.grid_columnconfigure(0, weight=1)
        main.grid(row=1, column=0, sticky="nsew")


        NavBar = tk.Frame(main, bg=navbg, width=70)
        subMain = tk.PanedWindow(self, bg=submainbg, width=200)
        subMain.grid(row=1, column=2)


        # This is the Logo that I created in Adobe Illistrator


        # button = tk.Button(self, text="Visit Page 1",
        #                     command=lambda: controller.show_frame(PageOne))
        # button.pack()

        # button2 = tk.Button(self, text="Visit Page 2",
        #                     command=lambda: controller.show_frame(PageTwo))
        # button2.pack()



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()
        


app = SeaofBTCapp()
app.title("EasyA")
app.eval("tk::PlaceWindow . center")
app.geometry("600x850")
onjpg = PhotoImage(file= "assets/icons8-toggle-on-50.png") 
offjpg = PhotoImage(file="assets/icons8-toggle-off-50.png")

def change_theme():
    if app.tk.call("ttk::style", "theme", "use")=="azure-dark":
        app.tk.call("set_theme", "light")
    else:
        app.tk.call("set_theme", "dark")



app.mainloop()
