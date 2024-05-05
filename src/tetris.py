import tkinter as tk
import random as rd
import threading as th
import customtkinter as ctk
import pyautogui
import sys
import utils

width = 10
height = 22
cell_size = 32

SIDE_CELL_SIZE = 32
SIDE_CANVAS_WIDTH = 4 * cell_size
SIDE_CANVAS_HEIGHT = 4 * cell_size

colors = {
    0: "#000000",
    1: "#FF0000",
    2: "#00FF00",
    3: "#0000FF",
    4: "#FFA500",
    5: "#FFFF00",
    6: "#800080",
    7: "#00FFFF"
}

tetrominos_rotations = [
    # Tétrimino 1 (forme en T)
    [
        # Configuration initiale
        [[0, 0, 1],
         [1, 1, 1]],
        # Rotation à 90 degrés
        [[1, 0],
         [1, 0],
         [1, 1]],
        # Rotation à 180 degrés
        [[1, 1, 1],
         [1, 0, 0]],
        # Rotation à 270 degrés
        [[1, 1],
         [0, 1],
         [0, 1]]
    ],

    # Tétrimino 2 (forme en Z)
    [
        # Configuration initiale
        [[0, 2, 2],
         [2, 2, 0]],
        # Rotation à 90 degrés
        [[2, 0],
         [2, 2],
         [0, 2]]
    ],

    # Tétrimino 3 (forme en L)
    [
        # Configuration initiale
        [[0, 3, 0],
         [3, 3, 3]],
        # Rotation à 90 degrés
        [[3, 0],
         [3, 3],
         [3, 0]],
        # Rotation à 180 degrés
        [[3, 3, 3],
         [0, 3, 0]],
        # Rotation à 270 degrés
        [[0, 3],
         [3, 3],
         [0, 3]]
    ],

    # Tétrimino 4 (forme en S)
    [
        # Configuration initiale
        [[4, 4, 0],
         [0, 4, 4]],
        # Rotation à 90 degrés
        [[0, 4],
         [4, 4],
         [4, 0]]
    ],

    # Tétrimino 5 (forme en J)
    [
        # Configuration initiale
        [[5, 0, 0],
         [5, 5, 5]],
        # Rotation à 90 degrés
        [[5, 5],
         [5, 0],
         [5, 0]],
        # Rotation à 180 degrés
        [[5, 5, 5],
         [0, 0, 5]],
        # Rotation à 270 degrés
        [[0, 5],
         [0, 5],
         [5, 5]]
    ],

    # Tétrimino 6 (forme en I)
    [
        # Configuration initiale
        [[6],
         [6],
         [6],
         [6]],

        [[6, 6, 6, 6]]
    ],

    # Tétrimino 7 (forme en O)
    [
        # Configuration initiale
        [[7, 7],
         [7, 7]]
    ]
]


user_screen_width, user_screen_height = pyautogui.size()

playfield = [[0] * width for _ in range(height)]
actual_piece = None
score = 0
game_over = False
level = 1
lines_cleared = 0
acceleration_coef = 1
"""app = tk.Tk()
app.title("Tetris")
app.attributes("-fullscreen", True)"""

speed = round(800 / (1 + level * acceleration_coef))

waiting_piece = None
c_use = False

paused = False


def new_piece():
    global actual_piece, game_over
    if not game_over:
        shape = rd.choice(tetrominos_rotations)
        color = rd.choice(list(colors.values()))
        actual_piece = {
            "forme": shape,
            "couleur": color,
            "rotation": 0,
            "x": width // 2 - len(shape[0][0]) // 2,
            "y": 0
        }
    if collision():
        game_over = True


def draw_bordered_rectangle(x, y, fill_color):
    grad_color_dark = darken_color(fill_color)
    grad_color_light = lighten_color(fill_color)
    playfield_canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size,
                                      (y + 1) * cell_size, fill=grad_color_dark, outline="", tags="piece")
    playfield_canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1)
                                      * cell_size, (y + 1) * cell_size, outline="black", width=2, tags="piece")


def lighten_color(color, factor=1.2):
    r, g, b = hex_to_rgb(color)
    r = min(int(r * factor), 255)
    g = min(int(g * factor), 255)
    b = min(int(b * factor), 255)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def darken_color(color, factor=0.8):
    r, g, b = hex_to_rgb(color)
    r = max(int(r * factor), 0)
    g = max(int(g * factor), 0)
    b = max(int(b * factor), 0)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def preview_piece():
    if actual_piece is not None:
        temp_piece = actual_piece.copy()
        rotation = actual_piece["rotation"]
        temp_piece["rotation"] = rotation
        for y_offset in range(height - len(temp_piece["forme"][rotation]), -1, -1):
            temp_piece["y"] = y_offset
            if not collision_preview(temp_piece):
                refresh_playfield()
                draw_preview_piece(temp_piece)
                return


def collision_preview(piece):
    rotation = piece["rotation"]
    for y, ligne in enumerate(piece["forme"][rotation]):
        for x, case in enumerate(ligne):
            if case != 0:
                piece_x = piece["x"] + x
                piece_y = piece["y"] + y

                if not (0 <= piece_x < width and 0 <= piece_y < height) or playfield[piece_y][piece_x] != 0:
                    return True
    return False


def draw_preview_piece(piece):
    playfield_canvas.delete("preview")
    rotation = piece["rotation"]
    for y, ligne in enumerate(piece["forme"][rotation]):
        for x, case in enumerate(ligne):
            if case != 0:
                piece_x = piece["x"] + x
                piece_y = piece["y"] + y
                playfield_canvas.create_rectangle(
                    piece_x * cell_size, piece_y * cell_size,
                    (piece_x + 1) * cell_size, (piece_y + 1) * cell_size,
                    outline="#FFFFFF", width=2, tag="preview"
                )


def refresh_playfield():
    playfield_canvas.delete("grid")
    playfield_canvas.delete("piece")

    for y in range(height):
        for x in range(width):
            color_id = playfield[y][x]
            if color_id != 0:
                draw_bordered_rectangle(x, y, colors[color_id])

    grid_color = "#353535"
    for y in range(height):
        playfield_canvas.create_line(
            0, y * cell_size, width * cell_size, y * cell_size, fill=grid_color, tag="grid")
    for x in range(width):
        playfield_canvas.create_line(
            x * cell_size, 0, x * cell_size, height * cell_size, fill=grid_color, tag="grid")

    if actual_piece is not None:
        rotation = actual_piece["rotation"]
        for y, ligne in enumerate(actual_piece["forme"][rotation]):
            for x, case in enumerate(ligne):
                if case != 0:
                    piece_x = actual_piece["x"] + x
                    piece_y = actual_piece["y"] + y
                    draw_bordered_rectangle(piece_x, piece_y, colors[case])


def move_left(event):
    if actual_piece is not None and not game_over and not paused:
        if actual_piece["x"] > 0 and not collision(-1):
            actual_piece["x"] -= 1
            refresh_playfield()
            preview_piece()


def move_right(event):
    if actual_piece is not None and not game_over and not paused:
        if actual_piece["x"] < width and not collision(1):
            actual_piece["x"] += 1
            refresh_playfield()
            preview_piece()


def move_down_touch(event):
    if actual_piece is not None and not game_over and not paused:
        if actual_piece["y"] < height and not collision(0, 1):
            actual_piece["y"] += 1
            refresh_playfield()
            preview_piece()


def move_down():
    global actual_piece, score, lines_cleared, level, c_use, paused
    if actual_piece is not None and not game_over and not paused:
        if actual_piece["y"] < height and not collision(0, 1):
            actual_piece["y"] += 1
            refresh_playfield()
            preview_piece()
            app.after(speed, move_down)
        else:
            piece_fix()
            new_piece()
            refresh_playfield()
            app.after(speed, move_down)
            update_score()
            check_level()
            c_use = False


def drop_piece(event):
    global actual_piece, score, lines_cleared, level, c_use
    if actual_piece is not None and not game_over and not paused:
        cpt = 0
        while not collision(0, 1):
            actual_piece["y"] += 1
            cpt += 1
        piece_fix()
        new_piece()
        update_score()
        check_level()
        refresh_playfield()
        score += 5 * (cpt // 3)
        c_use = False


def piece_rotation(event=None):
    if actual_piece is not None and not game_over and not paused:
        rotation = (actual_piece["rotation"] + 1) % len(actual_piece["forme"])
        old_rotation = actual_piece["rotation"]
        actual_piece["rotation"] = rotation
        if collision():
            actual_piece["rotation"] = old_rotation
        preview_piece()
        refresh_playfield()


def collision(dx=0, dy=0):
    global actual_piece
    rotation = actual_piece["rotation"]
    for y, ligne in enumerate(actual_piece["forme"][rotation]):
        for x, case in enumerate(ligne):
            if case != 0:
                new_x, new_y = actual_piece["x"] + \
                    x + dx, actual_piece["y"] + y + dy
                if not (0 <= new_x < width and 0 <= new_y < height) or playfield[new_y][new_x] != 0:
                    return True
    return False


def clear_lines():
    global playfield, score, lines_cleared
    complete_lines = []
    for y in range(height):
        if all(playfield[y]):
            complete_lines.append(y)

    lines_cleared += len(complete_lines)
    if len(complete_lines) == 1:
        score += 100 * level
    elif len(complete_lines) == 2:
        score += 300 * level
    elif len(complete_lines) == 3:
        score += 500 * level
    elif len(complete_lines) == 4:
        score += 800 * level

    for y in complete_lines:
        playfield.pop(y)
        playfield.insert(0, [0] * width)

    refresh_playfield()


def piece_fix():
    global actual_piece, c_use
    rotation = actual_piece["rotation"]
    for y, line in enumerate(actual_piece["forme"][rotation]):
        for x, case in enumerate(line):
            if case != 0:
                playfield[actual_piece["y"] + y][actual_piece["x"] + x] = case
    c_use = False
    clear_lines()


def change_piece(event=None):
    global actual_piece, waiting_piece, c_use
    if not c_use and not paused:
        if waiting_piece is None:
            waiting_piece = actual_piece
            new_piece()
        else:
            actual_piece, waiting_piece = waiting_piece, actual_piece
            actual_piece["x"] = width // 2 - \
                len(actual_piece["forme"][actual_piece["rotation"]][0]) // 2
            actual_piece["y"] = 0
        refresh_side_piece()
        refresh_playfield()
    c_use = True


def game_loop():
    new_piece()
    refresh_playfield()
    app.after(speed, move_down)


def threading_game_loop():
    game_thread = th.Thread(target=game_loop)
    game_thread.daemon = True
    game_thread.start()


def update_score():
    global score, game_over, level, lines_cleared
    if game_over:
        game_over_screen()
    else:
        if 'score_label' in globals() and level_label in globals() and lines_label in globals():
            score_label.configure(text='Score \n {}'.format(score))
            level_label.configure(text='Level \n {}'.format(level))
            lines_label.configure(
                text='Lines Cleared \n {}'.format(lines_cleared))
        else:
            score_screen()


def score_screen():
    global score_canvas, score_label, level_label, lines_label

    # Créer le canvas score_canvas s'il n'existe pas encore
    if not 'score_canvas' in globals():
        score_canvas = ctk.CTkFrame(
            app, width=200, height=300, corner_radius=8, fg_color="black")
        score_canvas.place(in_=playfield_canvas,
                            relx=0, x=-230, y=300, anchor=tk.NW)

    # Créer ou mettre à jour le texte du score
    if not 'score_label' in globals():
        score_label = ctk.CTkLabel(
            score_canvas, text='Score\n {}'.format(score), font=("Arial", 20))
        score_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    else:
        score_label.configure(text='Score \n {}'.format(score))

    # Créer ou mettre à jour le texte du niveau
    if not 'level_label' in globals():
        level_label = ctk.CTkLabel(
            score_canvas, text='Level\n {}'.format(level), font=("Arial", 20))
        level_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    else:
        level_label.configure(text='Level \n {}'.format(level))

    # Créer ou mettre à jour le texte des lignes effacées
    if not 'lines_label' in globals():
        lines_label = ctk.CTkLabel(score_canvas, text='Lines\n {}'.format(
            lines_cleared), font=("Arial", 20))
        lines_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    else:
        lines_label.configure(text='Lines \n {}'.format(lines_cleared))


def check_level():
    global level, lines_cleared
    if lines_cleared == 10:
        level = 2
    elif lines_cleared == 20:
        level = 3
    elif lines_cleared == 30:
        level = 4
    elif lines_cleared == 40:
        level = 5
    elif lines_cleared == 50:
        level = 6
    elif lines_cleared == 60:
        level = 7
    elif lines_cleared == 70:
        level = 8
    elif lines_cleared == 80:
        level = 9
    elif lines_cleared == 90:
        level = 10
    elif lines_cleared == 120:
        level = 11


def refresh_side_piece():
    if waiting_piece is not None:
        draw_side_piece(waiting_piece)
    else:
        rectangle_side_canvas.delete("side_piece")


def draw_side_piece(piece):
    rectangle_side_canvas.delete("side_piece")
    rotation = piece["rotation"]
    piece_color = piece["couleur"]
    piece_form = piece["forme"][rotation]

    # Calculer les dimensions du rectangle_side_canvas et de la pièce
    canvas_width = rectangle_side_canvas.winfo_width()
    canvas_height = rectangle_side_canvas.winfo_height()
    piece_width = len(piece_form[0])
    piece_height = len(piece_form)

    # Calculer les coordonnées pour centrer la pièce dans le rectangle_side_canvas
    start_x = (canvas_width - piece_width * SIDE_CELL_SIZE) // 2
    start_y = (canvas_height - piece_height * SIDE_CELL_SIZE) // 2

    for y, ligne in enumerate(piece_form):
        for x, case in enumerate(ligne):
            if case != 0:
                rectangle_side_canvas.create_rectangle(
                    start_x + x * SIDE_CELL_SIZE, start_y + y * SIDE_CELL_SIZE,
                    start_x + (x + 1) * SIDE_CELL_SIZE, start_y +
                    (y + 1) * SIDE_CELL_SIZE,
                    fill=piece_color, outline="#000000", width=2, tags="side_piece"
                )


def home():
    import main_menu
# Récupérer les noms des variables actuelles dans le module
    variables_to_keep = ["pause_canvas", "piece_rotation", "app", "name", "run", "width", "height", "cell_size", "SIDE_CELL_SIZE", "SIDE_CANVAS_WIDTH", "SIDE_CANVAS_HEIGHT", "colors", 
                     "tetrominos_rotations", "user_screen_width", "user_screen_height", "playfield", "actual_piece", "score", 
                     "game_over", "level", "lines_cleared", "acceleration_coef", "speed", "waiting_piece", "c_use", "paused"]
    import types
    
    

    app.unbind(f"<{bind_options[0][1][1]}>")
    app.unbind(f"<{bind_options[1][1][1]}>")
    app.unbind(f"<{bind_options[2][1][1]}>")
    app.unbind(f"<{bind_options[3][1][1]}>")
    app.unbind(f"<{bind_options[4][1][1]}>")
    app.unbind(f"<{bind_options[5][1][1]}>")
    app.unbind("<Escape>")
    # Supprimer toutes les variables sauf celles à conserver
    for var_name, var_value in list(sys.modules[__name__].__dict__.items()):
        if var_name not in variables_to_keep and not var_name.startswith("__") and not isinstance(var_value, types.ModuleType) and not isinstance(sys.modules[__name__].__dict__[var_name], types.FunctionType):
            del sys.modules[__name__].__dict__[var_name]
    

    
    utils.reset_places(app)
    main_menu.run(app, name)



def quit():
    app.destroy()


def toggle_pause(event=None):
    global paused, pause_canvas
    if not game_over:
        def create_pause_menu():

            pause_canvas = ctk.CTkFrame(
                app, width=300, height=300, corner_radius=8, border_width=4, fg_color="black")

            pause_label = ctk.CTkLabel(
                pause_canvas, text="Paused", fg_color="black", font=("Arial", 30))
            pause_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

            button_frame = tk.Frame(pause_canvas, bg="#000000")

            play_button = ctk.CTkButton(master=button_frame,
                                        width=250,
                                        height=40,
                                        fg_color="#5dd55d",
                                        text_color="black",
                                        border_width=3,
                                        border_color="#90ee90",
                                        corner_radius=8,
                                        text="Resume",
                                        hover_color="#4ee44e",
                                        command=lambda: toggle_pause())

            home_button = ctk.CTkButton(master=button_frame,
                                        width=250,
                                        height=40,
                                        fg_color="#999999",
                                        text_color="black",
                                        border_width=3,
                                        border_color="#bfbfbf",
                                        corner_radius=8,
                                        text="Home",
                                        hover_color="#7a7a7a",
                                        command=lambda: home())

            quit_button = ctk.CTkButton(master=button_frame,
                                        width=250,
                                        height=40,
                                        fg_color="#999999",
                                        text_color="black",
                                        border_width=3,
                                        border_color="#bfbfbf",
                                        corner_radius=8,
                                        text="Quit",
                                        hover_color="#7a7a7a",
                                        command=lambda: quit())

            # Placer les boutons dans le cadre
            play_button.pack(fill=tk.X, padx=10, pady=10)
            home_button.pack(fill=tk.X, padx=10, pady=10)
            quit_button.pack(fill=tk.X, padx=10, pady=10)

            # Centrer le cadre sur le pause_canvas
            button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

            # Centrer le pause_canvas sur la fenêtre principale
            pause_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            return pause_canvas

        paused = not paused
        if paused:
            pause_canvas = create_pause_menu()
        else:
            pause_canvas.destroy()
            move_down()


def pause_game():
    toggle_pause()


def game_over_screen():
    global game_over_canvas, score, lines_cleared

    # Créer le cadre pour l'écran de fin de partie
    game_over_canvas = ctk.CTkFrame(
        app, width=300, height=300, corner_radius=8, border_width=4, fg_color="black")

    # Ajouter une étiquette pour afficher "Game Over"
    game_over_label = ctk.CTkLabel(
        game_over_canvas, text="Game Over", fg_color="black", font=("Arial", 35))
    game_over_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    # Positionner le cadre de fin de partie au centre de la fenêtre
    game_over_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Charger les images des boutons
    home_img = utils.get_image("home_icon.png", 50, 50)
    restart_img = utils.get_image("restart_icon.png", 50, 50)
    quit_img = utils.get_image("quit_icon.png", 50, 50)

    # Créer les boutons d'accueil, de redémarrage et de quitter
    home_button = ctk.CTkButton(game_over_canvas, image=home_img, command=home,
                                text="", width=50, height=50, fg_color="#999999", hover_color="#7a7a7a", border_width=3,
                                border_color="#bfbfbf",
                                corner_radius=8,)
    restart_button = ctk.CTkButton(
        game_over_canvas, image=restart_img, command=restart_game, text="", width=50, height=50, fg_color="#5dd55d", hover_color="#4ee44e", border_width=3,
        border_color="#90ee90",
        corner_radius=8,)
    quit_button = ctk.CTkButton(game_over_canvas, image=quit_img, command=quit,
                                text="", width=50, height=50, fg_color="#999999", hover_color="#7a7a7a", border_width=3,
                                border_color="#bfbfbf",
                                corner_radius=8,)
    score_label = ctk.CTkLabel(game_over_canvas, text="Score : {} \n\n Level : {}".format(
        score, level), font=("Arial", 20))

    score_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    home_button.place(relx=0.25, rely=0.8, anchor=tk.CENTER)
    restart_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    quit_button.place(relx=0.75, rely=0.8, anchor=tk.CENTER)
    
    if utils.get_highscore(name) < score:
        utils.update_highscore(name, score)


def restart_game():
    global game_over, score, lines_cleared, level, playfield, actual_piece, waiting_piece, c_use

    game_over = False
    score = 0
    lines_cleared = 0
    level = 1

    playfield = [[0] * width for _ in range(height)]

    actual_piece = None
    waiting_piece = None

    c_use = False
    
    update_score()

    threading_game_loop()

    refresh_playfield()

    refresh_side_piece()

    if 'game_over_canvas' in globals():
        game_over_canvas.destroy()


def main():
    """global playfield_canvas, side_canvas, rectangle_side_canvas
    app.bind("<Left>", move_left)
    app.bind("<Right>", move_right)
    app.bind("<Down>", move_down_touch)
    app.bind("<Up>", piece_rotation)
    app.bind("<space>", drop_piece)
    app.bind("c", change_piece)
    app.bind("<Escape>", toggle_pause)

    playfield_canvas = tk.Canvas(
        app, width=width * cell_size, height=height * cell_size, bg="black")
    playfield_canvas.pack(expand=1)

    if sys.platform == "win32":
        app.update()
    side_canvas = ctk.CTkFrame(
        app, width=4 * cell_size, height=4 * cell_size, corner_radius=8, fg_color="Black")
    side_canvas.place(in_=playfield_canvas,
                            relx=0, x=-150, y=20, anchor=tk.NW)

    rectangle_side_canvas = tk.Canvas(
        side_canvas, width=4 * cell_size - 20, height=4 * cell_size - 20, bg="black", border=False)

    rectangle_side_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    score_canvas = ctk.CTkFrame(
        app, width=200, height=300, corner_radius=8, fg_color="black")
    score_canvas.place(x=((app.winfo_width() - width * cell_size - SIDE_CANVAS_WIDTH) // 2 - SIDE_CANVAS_WIDTH) - 35,
                       y=(app.winfo_height() - SIDE_CANVAS_HEIGHT*4))

    score_label = ctk.CTkLabel(
        score_canvas, text='Score\n {}'.format(score), font=("Arial", 20))
    score_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    level_label = ctk.CTkLabel(
        score_canvas, text='Level\n {}'.format(level), font=("Arial", 20))
    level_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    lines_label = ctk.CTkLabel(score_canvas, text='Lines\n {}'.format(
        lines_cleared), font=("Arial", 20))
    lines_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    next_piece_Canvas = ctk.CTkFrame(
        app, width=200, height=350, corner_radius=8, fg_color="black")
    next_piece_Canvas.place(in_=playfield_canvas,
                            relx=1.0, x=20, y=10, anchor=tk.NW)

    threading_game_loop()
    app.mainloop()"""


def run(application : tk.Tk, username : str, options : list):
    global playfield_canvas, side_canvas, rectangle_side_canvas
    
    global app, name, bind_options
    app = application
    name = username
    bind_options = options
    utils.reset_grids(app)

    app.title("Tetris")
    app.bind(f"<{bind_options[0][1][1]}>", piece_rotation)
    app.bind(f"<{bind_options[1][1][1]}>", move_down_touch)
    app.bind(f"<{bind_options[2][1][1]}>", move_left)
    app.bind(f"<{bind_options[3][1][1]}>", move_right)
    app.bind(f"<{bind_options[4][1][1]}>", drop_piece)
    app.bind(f"<{bind_options[5][1][1]}>", change_piece)
    app.bind("<Escape>", toggle_pause)

    playfield_canvas = tk.Canvas(
        app, width=width * cell_size, height=height * cell_size, bg="black")
    playfield_canvas.pack(expand=1)

    side_canvas = ctk.CTkFrame(
        app, width=4 * cell_size, height=4 * cell_size, corner_radius=8, fg_color="Black")
    side_canvas.place(in_=playfield_canvas,
                            relx=0, x=-190, y=20, anchor=tk.NW)

    rectangle_side_canvas = tk.Canvas(
        side_canvas, width=4 * cell_size - 20, height=4 * cell_size - 20, bg="black", border=False)

    rectangle_side_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    score_canvas = ctk.CTkFrame(
        app, width=200, height=300, corner_radius=8, fg_color="black")
    score_canvas.place(in_=playfield_canvas,
                            relx=0, x=-230, y=300, anchor=tk.NW)

    score_label = ctk.CTkLabel(
        score_canvas, text='Score\n {}'.format(score), font=("Arial", 20))
    score_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    level_label = ctk.CTkLabel(
        score_canvas, text='Level\n {}'.format(level), font=("Arial", 20))
    level_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    lines_label = ctk.CTkLabel(score_canvas, text='Lines\n {}'.format(
        lines_cleared), font=("Arial", 20))
    lines_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    next_piece_Canvas = ctk.CTkFrame(
        app, width=200, height=350, corner_radius=8, fg_color="black")
    next_piece_Canvas.place(in_=playfield_canvas,
                            relx=1.0, x=20, y=10, anchor=tk.NW)


    global paused, game_over
    
    if paused or game_over:
        game_over = paused = False
        restart_game()
    else: 
        threading_game_loop()    
    
if __name__ == "__main__":
    main()
