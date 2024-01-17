#!/usr/bin/env python3

from tkinter import *
import tkinter as tk
from tkinter import font

wind = tk.Tk()
fstyle1 = font.Font(size=20)

def login(window):

    hpage = Frame(window)
    hpage.grid(row=0, column=0, sticky="nsew") 
    hpLabel = Label(hpage, text="Easy A", font=fstyle1) 
    hpLabel.place(x=0.5, y=0.5, anchor=CENTER)



def main():
    wind.geometry("650x650")
    home = login(wind)
    # frame = Frame(wind)
    # button = Button(frame, text='Login')
    # button.pack()
    
    wind.mainloop()
    


if __name__ == "__main__":
    main()
