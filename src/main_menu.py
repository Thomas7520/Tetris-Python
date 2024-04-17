import customtkinter, utils

def run(app : customtkinter.CTk, username : str):
    for slave in app.grid_slaves():
        slave.destroy()
    
    image_canvas = customtkinter.CTkCanvas(app, background="#96B5BA", highlightthickness=0)
    image_canvas.grid(row=0, column=1, sticky="N")

    title_image = utils.get_image("title_tetris.png", 512, 153)

    image_title_label = customtkinter.CTkLabel(master=image_canvas, text="", image=title_image, bg_color="#96B5BA")
    image_title_label.grid(row=0, column=0, pady=20)

