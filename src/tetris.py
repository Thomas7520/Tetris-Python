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
    7: "#00FFFF"
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
     ]
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


def refresh_playfield():
    playfield_canvas.delete("piece")
    for y in range(height):
        for x in range(width):
            color = colors[playfield[y][x]]
            playfield_canvas.create_rectangle(
                x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill=color, tags="piece")

    if actual_piece is not None:
        for y, ligne in enumerate(actual_piece["forme"]):
            for x, case in enumerate(ligne):
                if case != 0:
                    couleur = actual_piece["couleur"]
                    playfield_canvas.create_rectangle((actual_piece["x"] + x) * cell_size, (actual_piece["y"] + y) * cell_size,
                                                      (actual_piece["x"] + x + 1) * cell_size, (
                                                          actual_piece["y"] + y + 1) * cell_size,
                                                      fill=couleur, tags="piece")

# Fonction pour déplacer la pièce actuelle vers la gauche


def move_left(event):
    if actual_piece is not None:
        if actual_piece["x"] > 0 and not collision(-1):
            actual_piece["x"] -= 1
            refresh_playfield()

# Fonction pour déplacer la pièce actuelle vers la droite


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
    for y, line in enumerate(actual_piece["forme"]):
        for x, case in enumerate(line):
            if case != 0:
                playfield[actual_piece["y"] + y][actual_piece["x"] +
                                                 x] = list(colors.values()).index(actual_piece["couleur"])
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
