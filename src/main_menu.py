import tkinter, customtkinter, utils, tetris
            
def remove_frame(name : str):
    if name == "main_menu":
        frame_main_menu.grid_forget()
    elif name == "leaderboard":
        frame_leaderboard.grid_forget()
    elif name =="options":
        global button_bind_selected
        if button_bind_selected is not None:
            button_bind_selected.configure(text=button_bind_selected.cget('text')[1:-1], text_color="black")
            button_bind_selected = None
        frame_options.grid_forget()
    
def play_button_pressed():
    tetris.run(app, name, bind_options)

def show_main_menu(frame_to_remove : str):
    remove_frame(frame_to_remove)
    frame_main_menu.grid(row=0, column=0, pady=(370,0))

def show_leaderboard():
    frame_main_menu.grid_forget()
    frame_leaderboard.grid(row=0, column=0, pady=(350,0))

def show_options():
    frame_main_menu.grid_forget()
    frame_options.grid(row=0, column=0, pady=(350,0))

button_bind_selected = None

def button_bind_pressed(button : tkinter.Button):
    global button_bind_selected
     
    if button_bind_selected is None:
        button.configure(text=f"< {button.cget('text')} >", text_color="yellow")
        button_bind_selected = button

def key_pressed_event(event):
    global button_bind_selected 
    
    key_code = event.keycode
    key_name = str(event.keysym)
        
    if button_bind_selected is not None:
        
        if key_code == 27:
            button_bind_selected.configure(text=button_bind_selected.cget('text')[1:-1].capitalize(), text_color="black")
            button_bind_selected = None
            return
        
        for bind in bind_options:
            if bind[1][0] == key_code and bind[0] != bind_options[button_bind_selected.bind_id][0]: # We don't care about assigning same value on the same bind
                # match, can't assign this twice
                tkinter.messagebox.showwarning(title="Conflit", message=f"Cette touche a déjà été assigné à '{bind[0]}' !")
                button_bind_selected.configure(text=button_bind_selected.cget('text')[1:-1].capitalize(), text_color="black")
                button_bind_selected = None
                return
        
        bind_options[button_bind_selected.bind_id][1] = (key_code, key_name)
        utils.update_bind_options(name, bind_options)
        button_bind_selected.configure(text=key_name.capitalize(), text_color="black")
        button_bind_selected = None
        
        

def run(application : tkinter.Tk, username : str):
    global app, bind_options, name

    app = application
    bind_options = utils.get_bind_options(username)
    name = username
    
    # Reset grids to default values and remove widgets from grids
    utils.reset_grids(app)
            
    app.attributes("-fullscreen", True)
    
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    global image_canvas
    image_canvas = customtkinter.CTkCanvas(app, background="black", highlightthickness=0)
    image_canvas.grid_columnconfigure(0, weight=1)
    image_canvas.grid_rowconfigure(0, weight=1)

    image_canvas.grid(row=0, column=0, sticky="NSWE")

    title_image = utils.get_image("main_menu_tetris_logo.png", 1000 * 1.5, 694 * 1.5)

    image_title_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="black")
    image_title_label.grid(row=0, column=0, sticky="NSWE")
    
    global frame_main_menu, frame_leaderboard, frame_options
    
    frame_color = "#3566c9"
    button_color = "#778899"
    button_color_hover = "#BDB76B"
    scrollable_color_bg = "#2B2B2B"
    
    frame_main_menu = customtkinter.CTkFrame(master=image_canvas, fg_color=frame_color, bg_color=frame_color)
    frame_main_menu.grid_columnconfigure(0, weight=1)
    frame_main_menu.grid_rowconfigure(0, weight=1)
    frame_main_menu.grid_rowconfigure(1, weight=1)
    frame_main_menu.grid_rowconfigure(2, weight=1)
    frame_main_menu.grid_rowconfigure(3, weight=1)
    frame_main_menu.grid(row=0, column=0, pady=(370,0))
    
    width_button = 250
    padx_button = 15
    
    button_play = customtkinter.CTkButton(master=frame_main_menu, text="Jouer", corner_radius=0, height=65, fg_color=button_color, hover_color=button_color_hover, font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2", command=play_button_pressed)
    button_play.grid(row=0, column=0, sticky="EW", pady=(10,5), padx=padx_button)
    
    button_leaderboard = customtkinter.CTkButton(master=frame_main_menu, text="Leaderboard", corner_radius=0, height=65, fg_color=button_color, hover_color=button_color_hover, font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2", command=show_leaderboard)
    button_leaderboard.grid(row=1, column=0, sticky="EW", pady=5, padx=padx_button)
    
    button_option = customtkinter.CTkButton(master=frame_main_menu, text="Options", corner_radius=0, height=65, fg_color=button_color, hover_color=button_color_hover, font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2", command=show_options)
    button_option.grid(row=2, column=0, sticky="EW", pady=5, padx=padx_button)
    
    button_quit = customtkinter.CTkButton(master=frame_main_menu, text="Quitter", corner_radius=0, height=65, fg_color=button_color, hover_color=button_color_hover, font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2", command=lambda: app.quit())
    button_quit.grid(row=3, column=0, sticky="EW", pady=(5,10), padx=padx_button)
    
    # leaderboard menu
    frame_leaderboard = customtkinter.CTkFrame(master=image_canvas,  corner_radius=0, fg_color=frame_color, bg_color=frame_color)
    frame_leaderboard.grid_rowconfigure(0, weight=1)
    frame_leaderboard.grid_rowconfigure(1, weight=1)
    frame_leaderboard.grid_rowconfigure(2, weight=1)

    label_leaderboard = customtkinter.CTkLabel(master=frame_leaderboard, width=300, corner_radius=0, fg_color=frame_color, bg_color=frame_color, text="Leaderboard", font=(0,30), text_color="White")
    label_leaderboard.grid(row=0, column=0, sticky= "S", pady=10)

    scrollable_frame = customtkinter.CTkScrollableFrame(width=250, master=frame_leaderboard, fg_color=scrollable_color_bg, border_color=frame_color)
    scrollable_frame.grid_columnconfigure(1,weight=1)
    scrollable_frame.grid(row=1, column=0, pady=10)
    
    # Create a list to store the leaderboard data
    leaderboard_data = [("Player1", 6546546), ("Player2", 846510), ("Player3", 8456654), ("Player3", 566456), ("Player3", 654564), ("Player3", 80), ("Player3", 80), ("Player3", 80), ("Player3", 80), ("Player3", 80), ("Player3", 80)]
    
    #leaderboard_data = utils.get_highscore_list()
    
    for i in range(len(leaderboard_data)):
        username_label = customtkinter.CTkLabel(master=scrollable_frame, corner_radius=0, text=leaderboard_data[i][0], text_color="White", font=(0, 14))
        score_label = customtkinter.CTkLabel(master=scrollable_frame, corner_radius=0, text=leaderboard_data[i][1], text_color="White", font=(0, 14))
        username_label.grid(row=i, column=0, padx=15, pady=(0, 10), sticky="EW")
        score_label.grid(row=i, column=2, padx=15, pady=(0, 10), sticky="EW")

    button_back = customtkinter.CTkButton(master=frame_leaderboard, text="Menu principal", corner_radius=0, height=50, fg_color=button_color, hover_color=button_color_hover, font=("Arial Bold", 20), text_color="white", cursor="hand2", command= lambda: show_main_menu("leaderboard"))
    button_back.grid(row=2, column=0, sticky="EW", padx=15, pady=(0,10))
    
    # options menu
    
    frame_options = customtkinter.CTkFrame(master=image_canvas,  corner_radius=0, fg_color=frame_color, bg_color=frame_color)
    frame_options.grid_rowconfigure(0, weight=1)
    frame_options.grid_rowconfigure(1, weight=1)
    frame_options.grid_rowconfigure(2, weight=1)

    label_options = customtkinter.CTkLabel(master=frame_options, width=300, corner_radius=0, fg_color=frame_color, bg_color=frame_color, text="Options", font=(0,30), text_color="White")
    label_options.grid(row=0, column=0, sticky= "S", pady=10)

    scrollable_options = customtkinter.CTkScrollableFrame(width=250, master=frame_options, fg_color=scrollable_color_bg, border_color=frame_color)
    scrollable_options.grid(row=1, column=0, pady=10)
      
    label_slider = customtkinter.CTkLabel(master=scrollable_options, corner_radius=0, text="Volume", font=(0,14), text_color="White")
    label_slider.grid(row=0, column=0, sticky="W", padx=5)

    sound_volume_slider = customtkinter.CTkSlider(scrollable_options, width=170, from_=0, to=1, number_of_steps=100)
    sound_volume_slider.grid(row=0, column=0, padx=70, pady=10, sticky="E")
    
    for i in range(len(bind_options)):
        data = bind_options[i]
        label_option_bind = customtkinter.CTkLabel(master=scrollable_options, corner_radius=0, text=data[0], font=(0,14), text_color="White")
        button_bind = customtkinter.CTkButton(master=scrollable_options, text=data[1][1], corner_radius=0, height=30,  fg_color=button_color, hover_color=button_color_hover, font=("Arial Bold", 13), text_color="black", cursor="hand2")
        button_bind.configure(command=lambda button_pressed=button_bind: button_bind_pressed(button_pressed))
        button_bind.bind_id = i
        
        label_option_bind.grid(row=i+1, column=0, sticky="W", padx=5)
        button_bind.grid(row=i+1, column=0, sticky="E", padx=(0,70), pady=5)    

    button_back = customtkinter.CTkButton(master=frame_options, text="Menu principal", corner_radius=0, height=50, fg_color=button_color, hover_color=button_color_hover, font=("Arial Bold", 20), text_color="white", cursor="hand2", command= lambda: show_main_menu("options"))
    button_back.grid(row=2, column=0, sticky="EW", padx=15, pady=(0,10))
    
    app.bind("<Key>", key_pressed_event)