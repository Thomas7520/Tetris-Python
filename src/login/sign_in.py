import customtkinter
import CTkMessagebox
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

sign_up_script = utils.login_path / "sign_up.py"
    
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
    utils.exec_python(sign_up_script)

def perform_register(event=None):
    if not username_entry.get():
        CTkMessagebox.CTkMessagebox(title="Erreur", message="Veuillez saisir un pseudo !", icon="warning")
    elif not password_entry.get():
        CTkMessagebox.CTkMessagebox(title="Erreur", message="Veuillez saisir un mot de passe !", icon="warning")
    elif not email_entry.get():
        CTkMessagebox.CTkMessagebox(title="Erreur", message="Veuillez saisir un email !", icon="warning")
    elif not utils.is_valid_email(email_entry.get()):
        CTkMessagebox.CTkMessagebox(title="Erreur", message="Veuillez saisir un email valide !", icon="warning") 
    elif utils.username_exist(username_entry.get()) or utils.email_exist(email_entry.get()):
        CTkMessagebox.CTkMessagebox(title="Erreur", message="Le compte existe déjà", icon="warning")
    else:
        utils.write_csv([username_entry.get(), email_entry.get(), password_entry.get()])
        CTkMessagebox.CTkMessagebox(title="Login", message="Le compte a été crée avec succès", icon="check").get() #Le get permet de mettre en pause le programme jusqu'à ce que la fenêtre soit fermée

        app.destroy()
        utils.exec_python(sign_up_script)
        

def run():
    global app 

    app = customtkinter.CTk()
    app.attributes('-fullscreen', "true")

    app.title("Login")
    app.config(background='#96B5BA')
    app.iconbitmap(utils.image_path / "tetris_icon.ico")

    app.mainloop() 
    # This call is appears to be necessary to make the app actually go full screen.    app.mainloop()
    
if __name__ == "__main__":
    run()