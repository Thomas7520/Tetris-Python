import tkinter, customtkinter, utils


def reset_grids():
    for slave in app.grid_slaves():
        slave.destroy()
    
    for i in range(app.grid_size()[0]):
        app.grid_columnconfigure(i, weight=0, minsize=0)
    
    for i in range(app.grid_size()[1]):
        app.grid_rowconfigure(i, weight=0, minsize=0)
            
def remove_frame(name : str):
    if name == "main_menu":
        frame_main_menu.grid_forget()
    elif name == "leaderboard":
        frame_leaderboard.grid_forget()
    else:
        pass
    
def play_button_pressed():
    pass

def show_main_menu(frame_to_remove : str):
    remove_frame(frame_to_remove)
    frame_main_menu.grid(row=0, column=0, pady=(370,0))



def show_leaderboard():
    frame_main_menu.grid_forget()
    
    frame_leaderboard.grid(row=0, column=0, pady=(350,0))

def show_options():
    pass


def run(application : tkinter.Tk, username : str):
    global app
    
    app = application
    # Reset grids to default values and remove widgets from grids
    reset_grids()
    
    for slave in app.grid_slaves():
        slave.destroy()
    
    for i in range(app.grid_size()[0]):
        app.grid_columnconfigure(i, weight=0, minsize=0)
    
    for i in range(app.grid_size()[1]):
        app.grid_rowconfigure(i, weight=0, minsize=0)
            
    app.attributes("-fullscreen", True)

    
    
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    global image_canvas
    image_canvas = customtkinter.CTkCanvas(app, background="#96B5BA", highlightthickness=0)
    image_canvas.grid_columnconfigure(0, weight=1)
    image_canvas.grid_rowconfigure(0, weight=1)

    image_canvas.grid(row=0, column=0, sticky="NSWE")

    title_image = utils.get_image("main_menu_tetris_logo.png", 1000 * 1.5, 694 * 1.5)

    image_title_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="#96B5BA")
    image_title_label.grid(row=0, column=0, sticky="NSWE")
    
    
    global frame_main_menu, frame_leaderboard
        
    frame_main_menu = customtkinter.CTkFrame(master=image_canvas, fg_color="#3566c9", bg_color="#3566c9")
    frame_main_menu.grid_columnconfigure(0, weight=1)
    frame_main_menu.grid_rowconfigure(0, weight=1)
    frame_main_menu.grid_rowconfigure(1, weight=1)
    frame_main_menu.grid_rowconfigure(2, weight=1)
    frame_main_menu.grid_rowconfigure(3, weight=1)
    frame_main_menu.grid(row=0, column=0, pady=(370,0))
    
    width_button = 250
    padx_button = 15
    
    button_play = customtkinter.CTkButton(master=frame_main_menu, text="Jouer", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2")
    button_play.grid(row=0, column=0, sticky="EW", pady=5, padx=padx_button)
    
    button_leaderboard = customtkinter.CTkButton(master=frame_main_menu, text="Leaderboard", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2", command=show_leaderboard)
    button_leaderboard.grid(row=1, column=0, sticky="EW", pady=5, padx=padx_button)
    
    button_option = customtkinter.CTkButton(master=frame_main_menu, text="Options", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2")
    button_option.grid(row=2, column=0, sticky="EW", pady=5, padx=padx_button)
    
    button_quit = customtkinter.CTkButton(master=frame_main_menu, text="Quitter", corner_radius=0, height=65, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=width_button, cursor="hand2", command=lambda: app.quit())
    button_quit.grid(row=3, column=0, sticky="EW", pady=5, padx=padx_button)
    
    
    
    # leaderboard menu
    
    frame_leaderboard = customtkinter.CTkFrame(master=image_canvas,  corner_radius=0, fg_color="#96B5BA", bg_color="#96B5BA")
    frame_leaderboard.grid_rowconfigure(0, weight=1)
    frame_leaderboard.grid_rowconfigure(1, weight=1)
    frame_leaderboard.grid_rowconfigure(2, weight=1)



    label_leaderboard = customtkinter.CTkLabel(master=frame_leaderboard, corner_radius=0, fg_color="#96B5BA", bg_color="#96B5BA", text="Leaderboard", font=(0,30), text_color="White")
    label_leaderboard.grid(row=0, column=0, sticky= "S", pady=10)

    scrollable_frame = customtkinter.CTkScrollableFrame(master=frame_leaderboard)
    scrollable_frame.grid_columnconfigure(1,weight=1)
    scrollable_frame.grid(row=1, column=0, pady=10)
    
    
    # Create a list to store the leaderboard data
    leaderboard_data = [("Player1", 6546546), ("Player2", 846510), ("Player3", 8456654), ("Player3", 566456), ("Player3", 654564), ("Player3", 80), ("Player3", 80), ("Player3", 80), ("Player3", 80), ("Player3", 80), ("Player3", 80)]
    
    for i in range(len(leaderboard_data)):
        username_label = customtkinter.CTkLabel(master=scrollable_frame, corner_radius=0, text=leaderboard_data[i][0], text_color="White")
        score_label = customtkinter.CTkLabel(master=scrollable_frame, corner_radius=0, text=leaderboard_data[i][1], text_color="White")
        username_label.grid(row=i, column=0, pady=(0, 10), sticky="W")
        score_label.grid(row=i, column=1, pady=(0, 10), sticky="E")

    button_back = customtkinter.CTkButton(master=frame_leaderboard, text="Menu principal", corner_radius=0, height=50, fg_color="#67E9DA", hover_color="#436e77", font=("Arial Bold", 20), text_color="white", width=250, cursor="hand2", command= lambda: show_main_menu("leaderboard"))
    button_back.grid(row=2, column=0, sticky="EW", padx=15, pady=(0,10))