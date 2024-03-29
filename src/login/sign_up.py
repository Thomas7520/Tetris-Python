import customtkinter
import os, sys
from PIL import Image, ImageTk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils

    
def button_callback():
    print("button pressed")

app = customtkinter.CTk()

app.title("Login")
app.resizable(width=False, height=False)
window_height = 500
window_width = 1000

utils.center_window(app, window_width, window_height)

#app.grid_columnconfigure(0, weight=1)
#app.grid_columnconfigure(1, weight=2)

login_canvas = customtkinter.CTkCanvas(app, width=window_width - 300, height=window_height - 150, background=app["bg"], bd=0, highlightthickness=0)

login_canvas.place(relx=0.5, rely=0.57, anchor=customtkinter.CENTER)
login_canvas.update()

#utils.round_rectangle(login_canvas, 0,0, login_canvas.winfo_width(),login_canvas.winfo_height(), radius=60, fill="#525252")

"""label_username = customtkinter.CTkLabel(login_canvas, text="Nom d'utilisateur")
label_password = customtkinter.CTkLabel(login_canvas, text="Mot de passe")


#label_username.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
#label_username.pack()

button_login = customtkinter.CTkButton(app, text="Se connecter", command=button_callback)
#button_login.grid(row=1, column=2)"""

chemin_images = os.path.abspath(os.path.join(os.getcwd(), "images"))


img = ImageTk.PhotoImage(Image.open(f"{chemin_images}\\background_login.png").resize((login_canvas.winfo_width(), login_canvas.winfo_height())))
login_canvas.create_image(0,0, anchor=customtkinter.NW, image=img)



app.mainloop()








