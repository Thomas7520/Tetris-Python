import tkinter, customtkinter
import tkinter.messagebox
import sys
import utils
import main_menu

# Allows to remove the strange blur effect
if sys.platform == "win32":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


is_login_window = True

def switch_window(event=None):
    global is_login_window

    if is_login_window:
        register_window()
    else:
        login_window()
    
    is_login_window = not is_login_window
    
    if password_entry.view_password:
        password_entry.view_password = False
        password_entry.configure(show="*")
        image_password_label.configure(image=password_entry.image)
    
    username_entry.focus()

def label_switch_window_hover_on(event):
    label_switch_window.configure(text_color="#2e2e2e")
    app.config(cursor="hand2")

def label_switch_window_hover_off(event):
    label_switch_window.configure(text_color="#9A9A9A")
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
    
def state_password_view(event=None):
    password_entry.view_password = not password_entry.view_password
    
    if password_entry.view_password:
        password_entry.configure(show="")
        image_password_label.configure(image=password_entry.image_show_hover)
    else:
        password_entry.configure(show="*")
        image_password_label.configure(image=password_entry.image_hover)
        
def perform_button(event=None):
    if is_login_window:
        perform_login()
    else:
        perform_register()
        
def perform_login():
    if not username_entry.get():
        tkinter.messagebox.showwarning(title="Erreur", message="Veuillez saisir un pseudo !")
    elif not password_entry.get():
        tkinter.messagebox.showwarning(title="Erreur", message="Veuillez saisir un mot de passe !")
    elif not utils.username_exist(username_entry.get()) or not utils.check_password(username_entry.get(), password_entry.get()):
        tkinter.messagebox.showwarning(title="Erreur", message="Le nom d'utilisateur ou le mot de passe est incorrect !")
    else:
        
        tkinter.messagebox.showinfo(title="Login", message="Connexion avec succès !")
        main_menu.run(app, username_entry.get())
        
def perform_register():
    if not username_entry.get():
        tkinter.messagebox.showwarning(title="Erreur", message="Veuillez saisir un pseudo !")
    elif not password_entry.get():
        tkinter.messagebox.showwarning(title="Erreur", message="Veuillez saisir un mot de passe !")
    elif not email_entry.get():
        tkinter.messagebox.showwarning(title="Erreur", message="Veuillez saisir un email !")
    elif not utils.is_valid_email(email_entry.get()):
        tkinter.messagebox.showwarning(title="Erreur", message="Veuillez saisir un email valide !")
    elif utils.username_exist(username_entry.get()) or utils.email_exist(email_entry.get()):
        tkinter.messagebox.showwarning(title="Erreur", message="Le compte existe déjà !")
    else:
        utils.add_user_csv([username_entry.get(), email_entry.get(), password_entry.get()])
        utils.add_user_options_csv([username_entry.get(), 0, utils.default_bind_options])
        tkinter.messagebox.showwarning(title="Erreur", message="Le compte a été crée avec succès !")

        switch_window()
        


    
def login_window():
    if not username_entry._placeholder_text_active: username_entry.delete(0, 'end')
    if not password_entry._placeholder_text_active: password_entry.delete(0, 'end')
    if not email_entry._placeholder_text_active: email_entry.delete(0, 'end')
        
    label_switch_window.configure(text="Créer un compte")
    button_perform.configure(text="Se connecter")    

    email_entry.grid_forget()
    email_entry_label.grid_forget()
    
    

def register_window():
    if not username_entry._placeholder_text_active: username_entry.delete(0, 'end')
    if not password_entry._placeholder_text_active: password_entry.delete(0, 'end')
    
    label_switch_window.configure(text="Se connecter")
    button_perform.configure(text="Créer le compte")
    email_entry.grid(row=1, column=0, sticky="sew", padx=(25,0), pady=5)
    email_entry_label.grid(row=1, column=1, sticky="se", padx=(0,25), pady=5)


def run():
    global app, is_login_window

    app = tkinter.Tk()
    app.title("Login")
    app.config(background='#96B5BA')
    
    platform_name = sys.platform
    if platform_name == 'darwin':

        logo_image = 'tetris_icon.icns'

    elif platform_name == 'win32':
        logo_image = 'tetris_icon.ico'

    else:
        logo_image = 'tetris_icon.xbm'
    
    app.iconbitmap(utils.image_path / logo_image)

    app.grid_rowconfigure(0, weight=1, minsize=20)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=1, minsize=20)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1, minsize=600) #Taille minimale du login canva cohérente
    app.grid_columnconfigure(2, weight=1)


    # Pour éviter que le login canva prenne toute la place en y, il faut introduire des canvas dans les 2 grilles à gauche et à droite et 1 en bas
    fill_left_canvas = customtkinter.CTkCanvas(app, background=app["background"],highlightthickness=0, width=60)
    fill_left_canvas.grid(row=1, column=0, sticky="NSEW")

    fill_right_canvas = customtkinter.CTkCanvas(app, background=app["background"],highlightthickness=0, width=60)
    fill_right_canvas.grid(row=1, column=2, sticky="NSEW")

    fill_bottom_canvas = customtkinter.CTkCanvas(app, background=app["background"],highlightthickness=0, height=40)
    fill_bottom_canvas.grid(row=2, column=1, sticky="NEW")

    image_canvas = customtkinter.CTkCanvas(app, background="#96B5BA", highlightthickness=0)
    image_canvas.grid(row=0, column=1, sticky="N")

    title_image = utils.get_image("title_tetris.png", 512, 153)

    image_title_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="#96B5BA")
    image_title_label.grid(row=0, column=0, pady=20)

    login_canvas = customtkinter.CTkCanvas(app, background="white", highlightthickness=0)
    login_canvas.grid_rowconfigure(0, weight=1, minsize=20)
    login_canvas.grid_rowconfigure(1, weight=1)
    login_canvas.grid_rowconfigure(2, weight=1)
    login_canvas.grid_columnconfigure(0, weight=1)
    login_canvas.grid(row=1, column=1, sticky="NSEW")
    
    login_canvas.update()


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

    global username_entry, email_entry, password_entry, image_password_label
    
    username_entry = customtkinter.CTkEntry(master=frame_components, placeholder_text="Pseudo", height=70 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", font=("", 20))
    username_entry.image = utils.get_image("user_icon.png", 64, 64)
    username_entry.grid(row=0, column=0, sticky="sew", padx=(25,0), pady=5)

    image_username_label = customtkinter.CTkLabel(frame_components, text="", width=0,height=70, image=username_entry.image, fg_color="#D9D9D9", bg_color="#D9D9D9")
    image_username_label.grid(row=0, column=1, sticky="se", padx=(0,25), pady=5)

    global email_entry, email_entry_label
    
    email_entry = customtkinter.CTkEntry(master=frame_components, placeholder_text="Email", height=70 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", font=("", 20))
    email_entry.image = utils.get_image("email_icon.png", 64, 64)
    
    email_entry_label = customtkinter.CTkLabel(frame_components, text="", width=0,height=70, image=email_entry.image, fg_color="#D9D9D9", bg_color="#D9D9D9")


    password_entry = customtkinter.CTkEntry(master=frame_components, placeholder_text="Mot de passe", height=70 ,fg_color="#D9D9D9", corner_radius=0, border_color="#D9D9D9", bg_color="#D9D9D9",text_color="#9A9A9A", show='*', font=("", 20))
    password_entry.view_password = False
    password_entry.image = utils.get_image("password_icon.png", 64, 64)
    password_entry.image_hover = utils.get_image("password_icon_hover.png", 64, 64)
    password_entry.image_show = utils.get_image("password_icon_show.png", 64, 64)
    password_entry.image_show_hover = utils.get_image("password_icon_show_hover.png", 64, 64)
    password_entry.grid(row=2, column=0, sticky="sew", padx=(25,0), pady=5)
    password_entry.bind("<Return>", perform_button)
   
    image_password_label = customtkinter.CTkLabel(frame_components, text="", height=70, image=password_entry.image, fg_color="#D9D9D9", bg_color="#D9D9D9")
    image_password_label.bind("<Button-1>", state_password_view)
    image_password_label.bind("<Enter>", label_password_hover_on)
    image_password_label.bind("<Leave>", label_password_hover_off)
    image_password_label.grid(row=2, column=1, sticky="se", padx=(0,25), pady=5)

    global frame_components_bottom
    frame_components_bottom = customtkinter.CTkFrame(login_canvas, fg_color="white", bg_color="white", height= 90 , width=login_canvas.winfo_width() - 30)
    frame_components_bottom.grid_columnconfigure(0, weight=1)
    frame_components_bottom.grid_columnconfigure(1, weight=1)
    frame_components_bottom.grid_rowconfigure(1, weight=1)
    frame_components_bottom.grid(row=2, column=0, sticky="nswe")

    global label_switch_window, button_perform
    label_switch_window = customtkinter.CTkLabel(master=frame_components_bottom, text="Créer un compte",text_color="#9A9A9A", fg_color="white", bg_color="white",font=("Arial Bold", 20))
    label_switch_window.bind("<Enter>", label_switch_window_hover_on)
    label_switch_window.bind("<Leave>", label_switch_window_hover_off)
    label_switch_window.bind("<Button-1>", switch_window)
    label_switch_window.grid(row=0, column=0, sticky="w", padx=25, pady=(0,10))
    
    button_perform = customtkinter.CTkButton(master=frame_components_bottom,text="Se connecter", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=200, cursor="hand2", command=perform_button)
    button_perform.grid(row=0, column=1, sticky="e", padx=25, pady=(0,10))
    
    app.minsize(app.winfo_reqwidth(), app.winfo_reqheight())

    app.mainloop()
    
if __name__ == "__main__":
    run()