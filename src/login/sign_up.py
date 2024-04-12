import customtkinter
import CTkMessagebox
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

sign_in_script = utils.login_path / "sign_in.py"
main_menu_script = utils.root_path / "src" / "main_menu.py"

    
def label_new_account_hover_on(event):
    label_create_account.configure(text_color="#2e2e2e")
    app.config(cursor="hand2")

def label_new_account_hover_off(event):
    label_create_account.configure(text_color="#9A9A9A")
    app.config(cursor="")

def label_password_hover_on(event):
    if password_entry.view_password:
        image_password_label.configure(image=password_entry.image_show_hover)
    else:
        image_password_label.configure(image=password_entry.image_hover)
    
    app.config(cursor="hand2")
    
def label_password_hover_off(event):
    if password_entry.view_password:
        image_password_label.configure(image=password_entry.image_show)
    else:
        image_password_label.configure(image=password_entry.image)
    
    app.config(cursor="")
    
def state_password_view(event):
    password_entry.view_password = not password_entry.view_password
    
    if password_entry.view_password:
        password_entry.configure(show="")
        image_password_label.configure(image=password_entry.image_show_hover)
    else:
        password_entry.configure(show="*")
        image_password_label.configure(image=password_entry.image_hover)
        

def open_new_account_window(event):
    app.destroy()
    utils.exec_python(sign_in_script)
    
def perform_login(event=None):
    if not username_entry.get():
        CTkMessagebox.CTkMessagebox(title="Erreur", message="Veuillez saisir un pseudo", icon="warning")
    elif not password_entry.get():
        CTkMessagebox.CTkMessagebox(title="Erreur", message="Veuillez saisir un mot de passe", icon="warning")
    elif not utils.username_exist(username_entry.get()) or not utils.check_password(username_entry.get(), password_entry.get()):
        CTkMessagebox.CTkMessagebox(title="Erreur", message="Le nom d'utilisateur ou le mot de passe est incorrect", icon="warning")
    else:
        CTkMessagebox.CTkMessagebox(title="Login", message="Connexion avec succès !", icon="check").get()
        utils.exec_python(main_menu_script, [username_entry.get()])
        app.destroy()
    
def run():
    global app 

    app = customtkinter.CTk()
    app.title("Login")
    app.config(background='#96B5BA')
    app.iconbitmap(utils.image_path / "tetris_icon.ico")
    
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1, minsize=600) #Taille minimale du login canva cohérente
    app.grid_columnconfigure(2, weight=1)
    app.update()

    # Pour éviter que le login canva prenne toute la place en y, il faut introduire des canvas dans les 2 grilles à gauche et à droite
    fill_left_canvas = customtkinter.CTkCanvas(app, background=app["background"], highlightthickness=0, width=20)
    fill_left_canvas.grid(row=1, column=0, sticky="NSEW")

    fill_right_canvas = customtkinter.CTkCanvas(app, background=app["background"], highlightthickness=0, width=20)
    fill_right_canvas.grid(row=1, column=2, sticky="NSEW")

    fill_bottom_canvas = customtkinter.CTkCanvas(app, background=app["background"], highlightthickness=0, height=20)
    fill_bottom_canvas.grid(row=2, column=1, sticky="NEW")

    image_canvas = customtkinter.CTkCanvas(app, background="#96B5BA", highlightthickness=0)
    image_canvas.grid(row=0, column=1, sticky="N")

    title_image = utils.get_image("title_tetris.png", 512, 153)

    image_title_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="#96B5BA")
    image_title_label.grid(row=0, column=0, pady=20)

    login_canvas = customtkinter.CTkCanvas(app, background="white", highlightthickness=0)
    login_canvas.grid(row=1, column=1, sticky="NSEW")

    login_canvas.grid_rowconfigure(0, weight=1, minsize=20)
    login_canvas.grid_rowconfigure(1, weight=1)
    login_canvas.grid_rowconfigure(2, weight=1)

    login_canvas.grid_columnconfigure(0, weight=1)
    login_canvas.update()


    top_bar = customtkinter.CTkFrame(login_canvas, fg_color="#626F71", bg_color="#626F71", height=20)
    top_bar.grid(row=0, column=0, sticky="NEW")

    frame_components = customtkinter.CTkFrame(login_canvas, fg_color="white", bg_color="white" , width=login_canvas.winfo_width() - 30)
    frame_components.grid_rowconfigure(0, weight=1)
    frame_components.grid_columnconfigure(0, weight=1)
    frame_components.grid_columnconfigure(1, weight=0)

    frame_components.grid_rowconfigure(1, weight=1)
    frame_components.grid_rowconfigure(2, weight=1)

    frame_components.grid(row=1, column=0, sticky="nsew", pady=10)

    global username_entry, password_entry, image_password_label
    
    username_entry = customtkinter.CTkEntry(master=frame_components, placeholder_text="Pseudo", height=70 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", font=("", 20))
    username_entry.image = utils.get_image("user_icon.png", 64, 64)
    username_entry.grid(row=0, column=0, sticky="sew", padx=(25,0), pady=5)

    image_username_label = customtkinter.CTkLabel(frame_components, text="", width=0,height=70, image=username_entry.image, fg_color="#D9D9D9", bg_color="#D9D9D9")
    image_username_label.grid(row=0, column=1, sticky="se", padx=(0,25), pady=5)

    password_entry = customtkinter.CTkEntry(master=frame_components, placeholder_text="Mot de passe", height=70 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", show='*', font=("", 20))
    password_entry.view_password = False
    password_entry.image = utils.get_image("password_icon.png", 64, 64)
    password_entry.image_hover = utils.get_image("password_icon_hover.png", 64, 64)
    password_entry.image_show = utils.get_image("password_icon_show.png", 64, 64)
    password_entry.image_show_hover = utils.get_image("password_icon_show_hover.png", 64, 64)
    password_entry.grid(row=1, column=0, sticky="sew", padx=(25,0), pady=5)
    password_entry.bind("<Return>", perform_login)
    
    image_password_label = customtkinter.CTkLabel(frame_components, text="", height=70, image=password_entry.image, fg_color="#D9D9D9", bg_color="#D9D9D9")
    image_password_label.bind("<Button-1>", state_password_view)
    image_password_label.bind("<Enter>", label_password_hover_on)
    image_password_label.bind("<Leave>", label_password_hover_off)
    image_password_label.grid(row=1, column=1, sticky="se", padx=(0,25), pady=5)


    frame_components_bottom = customtkinter.CTkFrame(login_canvas, fg_color="white", bg_color="white", height= 90 , width=login_canvas.winfo_width() - 30)
    frame_components_bottom.grid_columnconfigure(0, weight=1)
    frame_components_bottom.grid_columnconfigure(1, weight=1)
    frame_components_bottom.grid_rowconfigure(1, weight=1)
    frame_components_bottom.grid(row=3, column=0, sticky="nswe")

    global label_create_account
    label_create_account = customtkinter.CTkLabel(master=frame_components_bottom, text="Créer un compte",text_color="#9A9A9A", fg_color="white", bg_color="white",font=("Arial Bold", 20))
    label_create_account.bind("<Enter>", label_new_account_hover_on)
    label_create_account.bind("<Leave>", label_new_account_hover_off)
    label_create_account.bind("<Button-1>", open_new_account_window)
    label_create_account.grid(row=0, column=0, sticky="w", padx=25, pady=(0,10))

    button_login = customtkinter.CTkButton(master=frame_components_bottom,text="Se connecter", corner_radius=0, height=65, bg_color="#67E9DA", fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=200, cursor="hand2", command=perform_login)
    button_login.grid(row=0, column=1, sticky="e", padx=25, pady=(0,10))

    app.minsize(app.winfo_width(), app.winfo_height())
    app.mainloop()
    
if __name__ == "__main__":
    run()