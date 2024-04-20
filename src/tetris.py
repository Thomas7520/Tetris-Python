import tkinter as tk
import random as rd
import threading as th

width = 10
height = 22
cell_size = 32

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

playfield = [[0] * width for _ in range(height)]
actual_piece = None
score = 0
game_over = False
level = 1
lines_cleared = 0
acceleration_coef = 1
app = tk.Tk()
app.title("Tetris")
app.attributes("-fullscreen", True)
speed = round(800 / (1 + level * acceleration_coef))

playfield_canvas = tk.Canvas(
    app, width=width * cell_size, height=height * cell_size, bg="black")
playfield_canvas.pack(expand=1)


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
    if actual_piece is not None and not game_over:
        if actual_piece["x"] > 0 and not collision(-1):
            actual_piece["x"] -= 1
            refresh_playfield()
            preview_piece()


def move_right(event):
    if actual_piece is not None and not game_over:
        if actual_piece["x"] < width and not collision(1):
            actual_piece["x"] += 1
            refresh_playfield()
            preview_piece()


def move_down_touch(event):
    if actual_piece is not None and not game_over:
        if actual_piece["y"] < height  and not collision(0, 1):
            actual_piece["y"] += 1
            refresh_playfield()
            preview_piece()


def move_down():
    global actual_piece, score, lines_cleared, level
    if actual_piece is not None and not game_over:
        if actual_piece["y"] < height - len(actual_piece["forme"][0]) and not collision(0, 1):
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


def drop_piece(event):
    global actual_piece, score, lines_cleared, level
    if actual_piece is not None and not game_over:
        while not collision(0, 1):
            actual_piece["y"] += 1
        piece_fix()
        new_piece()
        update_score()
        check_level()
        refresh_playfield()
        


def piece_rotation(event=None):
    if actual_piece is not None and not game_over:
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
        score += 40 * (level + 1)
    elif len(complete_lines) == 2:
        score += 100 * (level + 1)
    elif len(complete_lines) == 3:
        score += 300 * (level + 1)
    elif len(complete_lines) == 4:
        score += 1200 * (level + 1)

    for y in complete_lines:
        playfield.pop(y)
        playfield.insert(0, [0] * width)

    refresh_playfield()


def piece_fix():
    global actual_piece
    rotation = actual_piece["rotation"]
    for y, line in enumerate(actual_piece["forme"][rotation]):
        for x, case in enumerate(line):
            if case != 0:
                playfield[actual_piece["y"] + y][actual_piece["x"] + x] = case
    clear_lines()


def game_loop():
    new_piece()
    refresh_playfield()
    app.after(speed,move_down)


def threading_game_loop():
    game_thread = th.Thread(target=game_loop)
    game_thread.daemon = True
    game_thread.start()


def update_score():
    global score, game_over, level, lines_cleared
    if game_over:
        playfield_canvas.create_text(width * cell_size // 2, height *
                                     cell_size // 2, text="Game Over", fill="white", font=("Arial", 30))
        playfield_canvas.create_text(width * cell_size // 2, height * cell_size //
                                     2 + 50, text="Score: {}".format(score), fill="white", font=("Arial", 20))
    else:
        playfield_canvas.delete("score")
        playfield_canvas.create_text(width * cell_size // 2, cell_size // 2,
                                     text="Score: {}".format(score), fill="white", font=("Arial", 20), tag="score")
        playfield_canvas.create_text(width * cell_size // 2, cell_size // 2 + 30, text="Lines: {}".format(
            lines_cleared), fill="white", font=("Arial", 20), tag="score")
        playfield_canvas.create_text(width * cell_size // 2, cell_size // 2 + 60,
                                     text="Level: {}".format(level), fill="white", font=("Arial", 20), tag="score")


def check_level():
    global level, lines_cleared
    if lines_cleared >= 10 * level:
        level += 1
        lines_cleared = 0


def main():
    app.bind("<Left>", move_left)
    app.bind("<Right>", move_right)
    app.bind("<Down>", move_down_touch)
    app.bind("<Up>", piece_rotation)
    app.bind("<space>", drop_piece)

    threading_game_loop()
    app.mainloop()


if __name__ == "__main__":
    main()