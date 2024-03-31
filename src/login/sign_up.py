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

window_height = 500
window_width = 1000

app.minsize(window_width, window_height)

utils.center_window(app, window_width, window_height)

app.grid_rowconfigure(0, weight = 0)
app.grid_columnconfigure(1, weight = 0)

app.update()

login_canvas = customtkinter.CTkCanvas(app, width=app.winfo_width(), height=app.winfo_height(),  background="#1d2a2f", highlightthickness=0)
login_canvas.grid(row=0, column=0, sticky="nsew")  # Le canevas s'étend dans toutes les directions
login_canvas.update()




image = utils.get_image("title_tetris.png", 512, 153)  # Insérer le chemin de votre image

x = (login_canvas.winfo_width() - image.width()) / 2
y = 25

# Placer l'image au centre du canevas

image_label = customtkinter.CTkLabel(master=app, text="", image=image, bg_color="#1d2a2f")
image_label.grid(row=0, column=0, pady=20, sticky="N")

app.grid_rowconfigure(0, weight=1)  # Permet au canevas de s'étendre verticalement
app.grid_columnconfigure(0, weight=1)  # Permet au canevas de s'étendre horizontalement


login_frame = customtkinter.CTkFrame(master=login_canvas, fg_color="#69a0a7", corner_radius=20, width=window_width - 400, height=window_height - 200)
login_frame.pack_propagate(0)
login_frame.place(anchor='center', relx=0.5, rely=0.63)


text_login_color = "black"

customtkinter.CTkLabel(master=login_frame, text="Connectez-vous", text_color=text_login_color, font=("Arial Bold", 24)).pack(anchor="s", pady=(20, 5))

customtkinter.CTkLabel(master=login_frame, text="Pseudo:", text_color=text_login_color, font=("Arial Bold", 14), compound="center").pack(anchor="s", pady=(10, 0))
customtkinter.CTkEntry(master=login_frame, width=225, fg_color="#EEEEEE", border_color=text_login_color, border_width=1, text_color="#000000").pack(anchor="s")

customtkinter.CTkLabel(master=login_frame, text="Mot de passe:", text_color=text_login_color, font=("Arial Bold", 14), compound="center").pack(anchor="s", pady=(5, 0))
customtkinter.CTkEntry(master=login_frame, width=225, fg_color="#EEEEEE", border_color=text_login_color, border_width=1, text_color="#000000", show="*").pack(anchor="s")

customtkinter.CTkButton(master=login_frame, text="Se connecter", fg_color="#508991", hover_color="#436e77", font=("Arial Bold", 12), text_color=text_login_color, width=225, cursor="hand2").pack(anchor="s", pady=(30, 0))

label_new_account = customtkinter.CTkLabel(master=login_frame, text="Vous n'avez pas de compte ? Cliquez ici pour vous inscrire", text_color="black", anchor="w", justify="center", font=("Arial Bold", 14), compound="center")
label_new_account.pack(anchor="s", pady=(25, 0))
label_new_account.bind("<Enter>", label_new_accound_hover_on)
label_new_account.bind("<Leave>", label_new_accound_hover_off)
label_new_account.bind("<Button-1>", open_new_account_window)

label_username = customtkinter.CTkLabel(login_canvas, text="Nom d'utilisateur")
label_password = customtkinter.CTkLabel(login_canvas, text="Mot de passe")

app.mainloop()










