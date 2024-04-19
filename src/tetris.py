import tkinter as tk
import random as rd
import threading as th

width = 10
height = 20
cell_size = 32

colors = {
    0: "#000000",
    1: "#FF0000",
    2: "#00FF00",
    3: "#0000FF",
    4: "#FFA500",
    5: "#FFFF00",
    6: "#800080",
    7: "#00FFFF",
    5: "#10FFFF",
}

tetrominos = [
    [[0, 0, 1],
     [1, 1, 1]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[0, 3, 0],
     [3, 3, 3]],

    [[4, 4, 0],
     [0, 4, 4]],

    [[0, 5, 5],
     [5, 5, 0]],

    [[6, 0, 0],
     [6, 6, 6]],

    [[7],
     [7],
     [7],
     [7],
     ],

    [[8, 8],
     [8, 8]]
]


playfield = [[0] * width for _ in range(height)]


actual_piece = None


app = tk.Tk()
app.title("Tetris")
app.attributes("-fullscreen", True)


playfield_canvas = tk.Canvas(
    app, width=width * cell_size, height=height * cell_size, bg="black")
playfield_canvas.pack(expand=1)


def new_piece():
    global actual_piece
    shape = rd.choice(tetrominos)
    color = rd.choice(list(colors.values()))
    actual_piece = {
        "forme": shape,
        "couleur": color,
        "x": width // 2 - len(shape[0]) // 2,
        "y": 0
    }

def draw_bordered_rectangle(x, y, fill_color):
    # Dessiner le rectangle principal avec un gradient de couleur
    grad_color_dark = darken_color(fill_color)
    grad_color_light = lighten_color(fill_color)
    playfield_canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill=grad_color_dark, outline="", tags="piece")
    
    # Ajouter une bordure avec une couleur contrastante
    playfield_canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, outline="black", width=2, tags="piece")

# Fonctions pour ajuster la couleur pour le gradient
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

def refresh_playfield():
    playfield_canvas.delete("piece")
    for y in range(height):
        for x in range(width):
            color_id = playfield[y][x]
            if color_id != 0 and color_id in colors:  
                draw_bordered_rectangle(x, y, colors[color_id])

    if actual_piece is not None:
        for y, ligne in enumerate(actual_piece["forme"]):
            for x, case in enumerate(ligne):
                if case != 0 and case in colors:  
                    piece_x = actual_piece["x"] + x
                    piece_y = actual_piece["y"] + y
                    draw_bordered_rectangle(piece_x, piece_y, colors[case])


def move_left(event):
    if actual_piece is not None:
        if actual_piece["x"] > 0 and not collision(-1):
            actual_piece["x"] -= 1
            refresh_playfield()


def move_right(event):
    if actual_piece is not None:
        if actual_piece["x"] < width - len(actual_piece["forme"][0]) and not collision(1):
            actual_piece["x"] += 1
            refresh_playfield()


def move_down_touch(event):
    if actual_piece is not None:
        if actual_piece["y"] < height - len(actual_piece["forme"]) and not collision(0, 1):
            actual_piece["y"] += 1
            refresh_playfield()


def move_down(event=None):
    global actual_piece
    if actual_piece is not None:
        if actual_piece["y"] < height - len(actual_piece["forme"]) and not collision(0, 1):
            actual_piece["y"] += 1
            refresh_playfield()
            app.after(1000, move_down)
        else:
            piece_fix()
            new_piece()
            refresh_playfield()
            app.after(1000, move_down)
    else:
        new_piece()
        refresh_playfield()
        app.after(1000, move_down)


def piece_rotation(event=None):
    if actual_piece is not None:
        ancienne_forme = actual_piece["forme"]
        actual_piece["forme"] = [[ancienne_forme[j][i] for j in range(
            len(ancienne_forme))] for i in range(len(ancienne_forme[0]))]
        if collision():
            actual_piece["forme"] = ancienne_forme
        refresh_playfield()


def collision(dx=0, dy=0):
    global actual_piece
    for y, ligne in enumerate(actual_piece["forme"]):
        for x, case in enumerate(ligne):
            if case != 0:
                new_x, new_y = actual_piece["x"] + \
                    x + dx, actual_piece["y"] + y + dy
                if not (0 <= new_x < width and 0 <= new_y < height) or playfield[new_y][new_x] != 0:
                    return True
    return False


# Modifiez la fonction clear_lines pour utiliser draw_bordered_rectangle si nécessaire
def clear_lines():
    global playfield
    complete_lines = []
    for y in range(height):
        if all(playfield[y]):
            complete_lines.append(y)

    for y in complete_lines:
        playfield.pop(y)
        playfield.insert(0, [0] * width)

    refresh_playfield()


def piece_fix():
    global actual_piece
    if actual_piece is not None:  # Vérifier si actual_piece est non None
        for y, line in enumerate(actual_piece["forme"]):
            for x, case in enumerate(line):
                if case != 0 and case in colors:  # Vérifier si case est une clé valide dans le dictionnaire colors
                    playfield[actual_piece["y"] + y][actual_piece["x"] + x] = case
                    print("pas draw")
                    draw_bordered_rectangle(actual_piece["x"] + x, actual_piece["y"] + y, colors[case])
                    print("Draw")
        clear_lines()


def game_loop():
    new_piece()
    refresh_playfield()
    app.after(500, move_down)


def threading_game_loop():
    game_thread = th.Thread(target=game_loop)
    game_thread.daemon = True
    game_thread.start()


def main():
    app.bind("<Left>", move_left)
    app.bind("<Right>", move_right)
    app.bind("<Down>", move_down_touch)
    app.bind("<Up>", piece_rotation)

    threading_game_loop()
    app.mainloop()


if __name__ == "__main__":
    main()
