import tkinter, customtkinter, utils

def run(app : tkinter.Tk, username : str):

    # Reset grids to default values and remove widgets from grids
    
    for slave in app.grid_slaves():
        slave.destroy()
    
    for i in range(app.grid_size()[0]):
        app.grid_columnconfigure(i, weight=0, minsize=0)
    
    for i in range(app.grid_size()[1]):
        app.grid_rowconfigure(i, weight=0, minsize=0)
            
    app.attributes("-fullscreen", True)

    
    
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    
    image_canvas = customtkinter.CTkCanvas(app, background="#96B5BA", highlightthickness=0)
    image_canvas.grid_columnconfigure(0, weight=1)
    image_canvas.grid_rowconfigure(0, weight=1)

    image_canvas.grid(row=0, column=0, sticky="NSWE")

    title_image = utils.get_image("main_menu_tetris_logo.png", 1000 * 1.5, 694 * 1.5)

    image_title_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="#96B5BA")
    image_title_label.grid(row=0, column=0, sticky="NSWE")

    frame_buttons = customtkinter.CTkFrame(master=image_canvas, fg_color="#3566c9", bg_color="#3566c9")
    frame_buttons.grid_columnconfigure(0, weight=1)
    frame_buttons.grid_rowconfigure(0, weight=1)
    frame_buttons.grid_rowconfigure(1, weight=1)
    frame_buttons.grid_rowconfigure(2, weight=1)
    frame_buttons.grid_rowconfigure(3, weight=1)
    frame_buttons.grid(row=0, column=0, pady=(370,0))
    
    width_button = 250
    padx_button = 15
    
    button_play = customtkinter.CTkButton(master=frame_buttons, text="Jouer", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2")
    button_play.grid(row=0, column=0, sticky="EW", pady=5, padx=padx_button)
    
    button_leaderboard = customtkinter.CTkButton(master=frame_buttons, text="Leaderboard", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2")
    button_leaderboard.grid(row=1, column=0, sticky="EW", pady=5, padx=padx_button)
    
    button_option = customtkinter.CTkButton(master=frame_buttons, text="Leaderboard", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2")
    button_option.grid(row=2, column=0, sticky="EW", pady=5, padx=padx_button)
    
    button_quit = customtkinter.CTkButton(master=frame_buttons, text="Quitter", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2")
    button_quit.grid(row=3, column=0, sticky="EW", pady=5, padx=padx_button)