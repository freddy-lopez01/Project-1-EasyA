#!/usr/bin/env python3

from tkinter import *
import tkinter as tk


def login(window):
    welcomeLab = Label(window, text="EasyA")
    welcomeLab.pack()

def main():
    rootWind = tk.Tk()
    login(rootWind)
    frame = Frame(rootWind)
    frame.pack()
    button = Button(frame, text='Login')
    button.pack()
    
    rootWind.mainloop()
    


if __name__ == "__main__":
    main()
