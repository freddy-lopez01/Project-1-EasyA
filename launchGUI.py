import tkinter as tk 
from tkinter import font 
from PIL import ImageTk



root = tk.Tk()

root.title("Easy A")
root.eval("tk::PlaceWindow . center")
root.geometry("700x700")

f1 = tk.Frame(root, width=700, height=700, bg="#f59e42")
f1.grid(row=0, column=0)
f1.pack_propagate(False)
# logo_img = Image.open("assets/EasyA.png")
# logo_img = logo_img.resize((50, 30), Image.ANTIALIAS) 
logo = ImageTk.PhotoImage(file="assets/EasyA.png")
logo_widget = tk.Label(f1, image=logo, bg="#f59e42")
logo_widget.image = logo
logo_widget.pack()

tk.Label(f1, text="Class selection", bg="#f59e42", fg="white", font=("TkMenuFont", 14)).pack()
lab1 = tk.Label(root, text="EasyA", font=('Arial', 20))
#lab1.pack()



root.mainloop()
