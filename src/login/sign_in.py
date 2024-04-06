import customtkinter
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

    
def label_new_account_hover_on(event):
    label_create_account.configure(text_color="#2e2e2e")
    app.config(cursor="hand2")

def label_new_account_hover_off(event):
    label_create_account.configure(text_color="#9A9A9A")
    app.config(cursor="")

def open_new_account_window(event):
    pass

def button_login_press():
    print("button pressed")

app = customtkinter.CTk()

app.title("Login")

"""window_height = 600 * 1.5
window_width = 900 * 1.5"""

app.config(background='#96B5BA')

app.minsize(600, 563) # Avant c'était window_height et window_width mais ça semble rendre mieux ainsi, à voir
app.geometry("600x563") # C'est le redimensionnement le plus cohérent

app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(1, weight=1, minsize=650) #Si on veut éviter l'étirement du login
app.grid_columnconfigure(2, weight=1)
app.update()


# Pour éviter que le login canva prenne toute la place en y, il faut introduire des canvas dans les 2 grilles à gauche et à droite
fill_left_canvas = customtkinter.CTkCanvas(app, background=app["background"],highlightthickness=0)
fill_left_canvas.grid(row=1, column=0, sticky="NSEW")

fill_right_canvas = customtkinter.CTkCanvas(app, background=app["background"],highlightthickness=0)
fill_right_canvas.grid(row=1, column=2, sticky="NSEW")


image_canvas = customtkinter.CTkCanvas(app, background="#96B5BA", highlightthickness=0)
image_canvas.grid(row=0, column=1, sticky="N")
image_canvas.update()

title_image = utils.get_image("title_tetris.png", 512, 153)

title_x = (image_canvas.winfo_width() - title_image.width()) / 2
title_y = 25

image_title_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="#96B5BA")
image_title_label.grid(row=0, column=0, pady=20)
image_title_label.update()

login_canvas = customtkinter.CTkCanvas(app, background="white", highlightthickness=0)
login_canvas.grid(row=1, column=1, sticky="NSEW")
login_canvas.update()

login_canvas.grid_rowconfigure(0, weight=1)
login_canvas.grid_rowconfigure(1, weight=1)
login_canvas.grid_rowconfigure(2, weight=1)

login_canvas.grid_columnconfigure(0, weight=1)


top_bar = customtkinter.CTkFrame(login_canvas, fg_color="#626F71", bg_color="#626F71", height=20)
top_bar.grid(row=0, column=0, sticky="NEW")

frame_components = customtkinter.CTkFrame(login_canvas, fg_color="white", bg_color="white" , width=login_canvas.winfo_width() - 30)
frame_components.grid_rowconfigure(0, weight=1)
frame_components.grid_columnconfigure(0, weight=1)
frame_components.grid_columnconfigure(1, weight=0)

frame_components.grid_rowconfigure(1, weight=1)
frame_components.grid_rowconfigure(2, weight=1)
frame_components.grid_rowconfigure(3, weight=1)

frame_components.grid(row=1, column=0, sticky="nsew", pady=10)
frame_components.update()


username_entry = customtkinter.CTkEntry(master=frame_components, placeholder_text="Pseudo", height=70 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", font=("", 20))
username_entry.image = utils.get_image("user_icon.png", 64, 64)
username_entry.grid(row=0, column=0, sticky="sew", padx=(25,0), pady=5)
username_entry.update()

image_username_label = customtkinter.CTkLabel(frame_components, text="", width=0,height=70, image=username_entry.image, fg_color="#D9D9D9", bg_color="#D9D9D9")
image_username_label.grid(row=0, column=1, sticky="se", padx=(0,25), pady=5)


email_entry = customtkinter.CTkEntry(master=frame_components, placeholder_text="Email", height=70 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", font=("", 20))
email_entry.image = utils.get_image("email_icon.png", 64, 64)
email_entry.grid(row=1, column=0, sticky="sew", padx=(25,0), pady=5)
email_entry.update()

email_entry_label = customtkinter.CTkLabel(frame_components, text="", width=0,height=70, image=email_entry.image, fg_color="#D9D9D9", bg_color="#D9D9D9")
email_entry_label.grid(row=1, column=1, sticky="se", padx=(0,25), pady=5)


password_entry = customtkinter.CTkEntry(master=frame_components, placeholder_text="Mot de passe", height=70 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", show='*', font=("", 20))
password_entry.image = utils.get_image("password_icon.png", 64, 64)
password_entry.grid(row=2, column=0, sticky="sew", padx=(25,0), pady=5)
password_entry.update()

image_password_label = customtkinter.CTkLabel(frame_components, text="", height=70, image=password_entry.image, fg_color="#D9D9D9", bg_color="#D9D9D9")
image_password_label.grid(row=2, column=1, sticky="se", padx=(0,25), pady=5)


frame_components_bottom = customtkinter.CTkFrame(login_canvas, fg_color="white", bg_color="white", height= 90 , width=login_canvas.winfo_width() - 30)
frame_components_bottom.grid_columnconfigure(0, weight=1)
frame_components_bottom.grid_columnconfigure(1, weight=1)
frame_components_bottom.grid_rowconfigure(1, weight=1)
frame_components_bottom.grid(row=3, column=0, sticky="nswe")
frame_components_bottom.update()


label_create_account = customtkinter.CTkLabel(master=frame_components_bottom, text="Se connecter",text_color="#9A9A9A", fg_color="white", bg_color="white",font=("Arial Bold", 20))
label_create_account.bind("<Enter>", label_new_account_hover_on)
label_create_account.bind("<Leave>", label_new_account_hover_off)
label_create_account.bind("<Button-1>", open_new_account_window)
label_create_account.grid(row=0, column=0, sticky="w", padx=25, pady=(0,10))
label_create_account.update()

button_login = customtkinter.CTkButton(master=frame_components_bottom,text="Créer le compte", corner_radius=0, height=65, bg_color="#67E9DA", fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=200, cursor="hand2", command=button_login_press)
button_login.grid(row=0, column=1, sticky="e", padx=25, pady=(0,10))
button_login.update()

app.mainloop()