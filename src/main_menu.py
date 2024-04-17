import tkinter, customtkinter, utils

def run(app : tkinter.Tk, username : str):
    for slave in app.grid_slaves():
        slave.destroy()
    
    app.attributes("-fullscreen", True)