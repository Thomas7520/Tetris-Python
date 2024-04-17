import tkinter, customtkinter, utils

def run(app : tkinter.Tk, username : str):
    for slave in app.grid_slaves():
        slave.destroy()
    
    app.attributes("-fullscreen", True)
    
    
    image_canvas = customtkinter.CTkCanvas(app, background="#96B5BA", highlightthickness=0)
    image_canvas.pack()

    title_image = utils.get_image("main_menu_tetris_logo.png", 1000 * 1.5, 694 * 1.5)

    image_title_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="#96B5BA")
    image_title_label.pack()

    button_perform = customtkinter.CTkButton(master=image_canvas, text="Se connecter", corner_radius=0, height=65, bg_color="#67E9DA", fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=200, cursor="hand2")
    button_perform.place(relx=0.5, rely=0.5, in_=image_canvas)
