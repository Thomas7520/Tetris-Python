import customtkinter
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils

def open_new_account_window(event):
    pass

def button_login_press():
    print("button pressed")

app = customtkinter.CTk()

app.title("Login")

window_height = 600 
window_width = 900

app.config(background='#96B5BA')

app.minsize(window_width, window_height)
app.resizable(False,False)

app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.update()

utils.center_window(app, window_width, window_height)

image_canvas = customtkinter.CTkCanvas(app, background="#96B5BA", highlightthickness=0)
image_canvas.grid(row=0, column=0, sticky="N")
image_canvas.update()

title_image = utils.get_image("title_tetris.png", 512, 153)

title_x = (image_canvas.winfo_width() - title_image.width()) / 2
title_y = 25

image_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="#96B5BA")
image_label.grid(row=0, column=0, pady=20)
image_label.update()

login_canvas = customtkinter.CTkCanvas(app, width=window_width - 300, height=window_height-240,background="red",highlightthickness=0)
login_canvas.grid(row=1, column=0, pady=(0,100))
login_canvas.pack_propagate(0)
login_canvas.update()

nickname_entry = customtkinter.CTkEntry(master=login_canvas, placeholder_text="Pseudo", height=60, width=login_canvas.winfo_width() - 200 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", font=("", 20))
nickname_entry.pack(pady=(50,0))
nickname_entry.update()

password_entry = customtkinter.CTkEntry(master=login_canvas, placeholder_text="Mot de passe", height=60, width=login_canvas.winfo_width() - 200 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", font=("", 20))
password_entry.pack(pady=(20,0))
password_entry.update()

frame_create_account = customtkinter.CTkFrame(login_canvas)
frame_create_account.pack(side="left",padx=40, pady=10)

frame_username = customtkinter.CTkFrame(login_canvas)
frame_username.pack(side="right",padx=40, pady=10)

button_login = customtkinter.CTkButton(master=frame_username,text="Se connecter", corner_radius=0, height=50, bg_color="#67E9DA", fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=225, cursor="hand2", command=button_login_press)
button_login.pack()
button_login.update()

label_create_account = customtkinter.CTkLabel(master=frame_create_account, text="Créer un compte", text_color="#9A9A9A", fg_color="white", bg_color="white",font=("Arial Bold", 16), command=open_new_account_window)
label_create_account.pack()
label_create_account.update()

login_canvas.create_rectangle(0, 0, login_canvas.winfo_width(), 10, fill="#626F71", outline="")
login_canvas.create_rectangle(0, 10, login_canvas.winfo_width(), login_canvas.winfo_height(), fill="white", outline="")

app.mainloop()








