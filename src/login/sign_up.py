import customtkinter
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils


def label_new_accound_hover_on(event):
    label_new_account.configure(text_color="#E44982")
    app.config(cursor="hand2")

def label_new_accound_hover_off(event):
    label_new_account.configure(text_color="black")
    app.config(cursor="")

def open_new_account_window(event):
    pass

def button_login():
    print("button pressed")

app = customtkinter.CTk()

app.title("Login")
app.resizable(width=False, height=False)

window_height = 500
window_width = 1000

utils.center_window(app, window_width, window_height)

#app.grid_columnconfigure(0, weight=1)
#app.grid_columnconfigure(1, weight=2)

#login_canvas = customtkinter.CTkCanvas(app, width=window_width - 300, height=window_height - 150, background=app["bg"], bd=0, highlightthickness=0)

#login_canvas.place(relx=0.5, rely=0.57, anchor=customtkinter.CENTER)
#login_canvas.update()






app.update()

login_canvas = customtkinter.CTkCanvas(app, width=app.winfo_width(), height=app.winfo_height(),  background="#1d2a2f", highlightthickness=0)
login_canvas.pack()
login_canvas.update()


image = utils.get_image("title_tetris.png", 512, 153)  # Insérer le chemin de votre image

x = (login_canvas.winfo_width() - image.width()) / 2
y = 25

# Placer l'image au centre du canevas
login_canvas.create_image(x, y, anchor=customtkinter.NW, image=image)

login_frame = customtkinter.CTkFrame(master=login_canvas, fg_color="#69a0a7", corner_radius=20, width=window_width - 400, height=window_height - 200)
login_frame.pack_propagate(0)
login_frame.place(anchor='center', relx=0.5, rely=0.63)

text_login_color = "black"

customtkinter.CTkLabel(master=login_frame, text="Connectez-vous", text_color=text_login_color, anchor="w", justify="center", font=("Arial Bold", 24)).pack(anchor="s", pady=(20, 5))

customtkinter.CTkLabel(master=login_frame, text="Pseudo:", text_color=text_login_color, anchor="w", justify="center", font=("Arial Bold", 14), compound="center").pack(anchor="s", pady=(10, 0))
customtkinter.CTkEntry(master=login_frame, width=225, fg_color="#EEEEEE", border_color=text_login_color, border_width=1, text_color="#000000").pack(anchor="s")

customtkinter.CTkLabel(master=login_frame, text="Mot de passe:", text_color=text_login_color, anchor="w", justify="center", font=("Arial Bold", 14), compound="center").pack(anchor="s", pady=(5, 0))
customtkinter.CTkEntry(master=login_frame, width=225, fg_color="#EEEEEE", border_color=text_login_color, border_width=1, text_color="#000000", show="*").pack(anchor="s")

customtkinter.CTkButton(master=login_frame, text="Se connecter", fg_color="#508991", hover_color="#436e77", font=("Arial Bold", 12), text_color=text_login_color, width=225, cursor="hand2").pack(anchor="s", pady=(30, 0))

label_new_account = customtkinter.CTkLabel(master=login_frame, text="Vous n'avez pas de compte ? Cliquez ici pour vous inscrire", text_color="black", anchor="w", justify="center", font=("Arial Bold", 14), compound="center")
label_new_account.pack(anchor="s", pady=(25, 0))
label_new_account.bind("<Enter>", label_new_accound_hover_on)
label_new_account.bind("<Leave>", label_new_accound_hover_off)
label_new_account.bind("<Button-1>", open_new_account_window)

#utils.round_rectangle(login_canvas, 0,0, login_canvas.winfo_width(),login_canvas.winfo_height(), radius=60, fill="#525252")

"""label_username = customtkinter.CTkLabel(login_canvas, text="Nom d'utilisateur")
label_password = customtkinter.CTkLabel(login_canvas, text="Mot de passe")


#label_username.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
#label_username.pack()

button_login = customtkinter.CTkButton(app, text="Se connecter", command=button_callback)
#button_login.grid(row=1, column=2)"""


#background_img = utils.get_image("background_login.png", login_canvas.winfo_width(), login_canvas.winfo_height())
#login_canvas.create_image(0,0, anchor=customtkinter.NW, image=background_img)


app.mainloop()










