import tkinter as tk
 
# setup
root = tk.Tk()
root.title("Menu system")
 
# create frames
menuFrame = tk.Frame(root)
menuFrame.grid(row=0, column=0)
itemFrame = tk.Frame(root)
itemFrame.grid(row=0, column=1)
 
# clear screen function
def clear(object):
    slaves = object.grid_slaves()
    for x in slaves:
        x.destroy()
 
# different items on different menus
def menu1():
    clear(itemFrame)
    tk.Label(itemFrame, text="Hello").grid(row=0, column=0)
    tk.Entry(itemFrame).grid(row=1, column=0)
 
def menu2():
    clear(itemFrame)
    tk.Checkbutton(itemFrame, text="greetings").grid(row=0, column=0)
    tk.Label(itemFrame, text="Menu2").grid(row=1, column=0)
 
# persistent menu buttons
menuButton1 = tk.Button(menuFrame, text="menu1", command=menu1).grid(row=0, column=0)
menuButton2 = tk.Button(menuFrame, text="menu2", command=menu2).grid(row=1, column=0)
 
tk.mainloop()
