import customtkinter
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import center_window

    
def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("Login")

#center(app)
window_height = 500
window_width = 900

center_window(app, window_width, window_height)



button = customtkinter.CTkButton(app, text="my button", command=button_callback)
button.grid(row=0, column=0, padx=20, pady=20)

app.mainloop()






