import tkinter as tk
import random as rd
import threading as th
import time as t


# Grid size parameters
GRID_WIDTH = 10
GRID_HEIGHT = 24
CELL_SIZE = 30

# Colors parameters
BACKGROUND_COLOR = "black"
GRID_COLOR = "gray"
BLOCK_COLORS = ["#0077D3", "#53DA3F", "#FD3F59",
                "#FF910C", "#FE4819", "#78256F", "#485DC5"]

# Template of the tetris blocks for each shape
TETRIS_SHAPES = [
    # L piece
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    # Square piece
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    # T piece
    [(0, 0), (1, 0), (2, 0), (1, 1)],
    # Z piece
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    # S piece
    [(1, 0), (2, 0), (0, 1), (1, 1)],
    # J piece
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    # I piece
    [(0, 0), (0, 1), (0, 2), (0, 3)]
]


def create_tetris_playfield():
    """
    This function creates the tetris playfield on the screen.

    Args:
        None

    Returns:
        None
    """
    global playfield_canvas

    # Create the canvas to display the playfield and place it on the center of the screen
    playfield_canvas = tk.Canvas(
        app, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, bg=BACKGROUND_COLOR)
    playfield_canvas.place(relx=0.5, rely=0.5, anchor="center")

    # Draw the grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            x0, y0 = x * CELL_SIZE, y * CELL_SIZE
            x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
            playfield_canvas.create_rectangle(
                x0, y0, x1, y1, outline=GRID_COLOR)


def draw_block(x, y, color):
    """
    This function draws a block on the tetris playfield.

    Args:
        x (int): The x position of the block
        y (int): The y position of the block
        color (str): The color of the block

    Returns:
        None
    """
    x0, y0 = x * CELL_SIZE, y * CELL_SIZE
    x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
    playfield_canvas.create_rectangle(
        x0, y0, x1, y1, fill=color, outline="black", tag="maPiece")
       
def draw_tetris_piece(x, y, shape_index, state=True):
    """
    This function draws a tetris piece on the playfield.

    Args:
        x (int): The x position of the piece
        y (int): The y position of the piece
        shape_index (int): The index of the shape in the TETRIS_SHAPES list
        state (bool): True to draw the piece, False to delete it

    Returns:
        None
    """
    if state:
        color = BLOCK_COLORS[shape_index % len(BLOCK_COLORS)]
        shape = TETRIS_SHAPES[shape_index]
        for block in shape:
            draw_block(x + block[0], y + block[1], color)
    else:
        for block in TETRIS_SHAPES[shape_index]:
            draw_block(x + block[0], y + block[1], BACKGROUND_COLOR)

def draw_block_definitly(x, y, color):
    """
    This function draws a block on the tetris playfield.

    Args:
        x (int): The x position of the block
        y (int): The y position of the block
        color (str): The color of the block

    Returns:
        None
    """
    x0, y0 = x * CELL_SIZE, y * CELL_SIZE
    x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
    playfield_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

def draw_tetris_pieces_definitly(x,y,shape_index):
    """
    This function draws a tetris piece on the playfield.

    Args:
        x (int): The x position of the piece
        y (int): The y position of the piece
        shape_index (int): The index of the shape in the TETRIS_SHAPES list
        state (bool): True to draw the piece, False to delete it

    Returns:
        None
    """
    color = BLOCK_COLORS[shape_index % len(BLOCK_COLORS)]
    shape = TETRIS_SHAPES[shape_index]
    for block in shape:
        draw_block_definitly(x + block[0], y + block[1], color)

locked_blocks = []

def lock_piece():
    global actual_piece

    secondary_list = []
    for block in TETRIS_SHAPES[actual_piece[2]]:
        abs_x = actual_piece[0] + block[0]
        abs_y = actual_piece[1] + block[1]
        secondary_list.append((abs_x, abs_y))
    locked_blocks.append(secondary_list)

    draw_tetris_pieces_definitly(actual_piece[0], actual_piece[1]-1, actual_piece[2])
    actual_piece = generate_piece()
    draw_tetris_piece(actual_piece[0], actual_piece[1], actual_piece[2])
    print(locked_blocks)
    
def piece_colision(piece):
   pass
   
def piece_hits_side(piece, direction):
    """
    Cette fonction vérifie si la pièce atteint le côté gauche ou droit du terrain de jeu.

    Args:
        piece (list): La pièce actuelle.
        direction (str): La direction à vérifier ("left" ou "right").

    Returns:
        bool: True si la pièce atteint le côté, False sinon.
    """
    for block in TETRIS_SHAPES[piece[2]]:
        abs_x = piece[0] + block[0]
        if direction == "left" and abs_x <= 0:
            return True
        elif direction == "right" and abs_x >= GRID_WIDTH - 1:
            return True
    return False

def move_piece(direction):
    global actual_piece

    if direction == "left":
        if not piece_hits_side(actual_piece, "left"):
            actual_piece[0] -= 1
    elif direction == "right":
        if not piece_hits_side(actual_piece, "right"):
            actual_piece[0] += 1
    elif direction == "down":
        if not piece_hits_bottom(actual_piece):
            actual_piece[1] += 1

    if piece_hits_bottom(actual_piece):
        lock_piece()
        
    del_piece(actual_piece)
    draw_tetris_piece(actual_piece[0], actual_piece[1], actual_piece[2])


def key_press(event):
    """
    This function handles the key press events.

    Args:
        event (tk.Event): The event object containing information about the key press.

    Returns:
        None
    """
    key = event.keysym
    if key == "Left":
        move_piece("left")
    elif key == "Right":
        move_piece("right")
    elif key == "Down":
        move_piece("down")


def del_piece(piece):
    """
    This function deletes a tetris piece from the playfield.

    Args:
        piece (list): The piece to be deleted.

    Returns:
        None
    """
    playfield_canvas.delete("maPiece")


"""def piece_collides(piece):
    
    This function checks if the current piece collides with other pieces on the playfield.

    Args:
        piece (list): The current piece.

    Returns:
        bool: True if collision occurs, False otherwise.
    
    for block in TETRIS_SHAPES[piece[2]]:
        abs_x = piece[0] + block[0]
        abs_y = piece[1] + block[1]
        if abs_x < 0 or abs_x >= GRID_WIDTH or abs_y >= GRID_HEIGHT or (abs_y >= 0 and playfield_canvas.find_enclosed(abs_x * CELL_SIZE, abs_y * CELL_SIZE, (abs_x + 1) * CELL_SIZE, (abs_y + 1) * CELL_SIZE)):
            return True
    return False"""


def piece_hits_bottom(piece):
    """
    This function checks if the current piece hits the bottom of the playfield.

    Args:
        piece (list): The current piece.

    Returns:
        bool: True if the piece hits the bottom, False otherwise.
    """
    for block in TETRIS_SHAPES[piece[2]]:
        abs_y = piece[1] + block[1]
        if abs_y >= GRID_HEIGHT:
            return True
    return False

def generate_piece():
    """
    This function generates a new tetris piece.

    Args:
        None

    Returns:
        list: The newly generated piece.
    """
    return [GRID_WIDTH // 2, 0, rd.randint(0, len(TETRIS_SHAPES) - 1)]


def move_piece_down():
    """
    Move the current piece down one step.

    Args:
        None

    Returns:
        None
    """
    global actual_piece

    move_piece("down")

    # Check if the piece has reached the bottom
    if not piece_hits_bottom(actual_piece):
        # Schedule the next movement down after a delay
        app.after(10, move_piece_down)

def start_new_piece():
    global actual_piece
    actual_piece = generate_piece()
    draw_tetris_piece(actual_piece[0], actual_piece[1], actual_piece[2])

def game_loop():
    create_tetris_playfield()
    start_new_piece()

    while True:
        move_piece("down")
        if piece_hits_bottom(actual_piece):
            lock_piece()
            start_new_piece()
        app.update()
        t.sleep(0.5)
        
def start_game_loop_in_thread():
    """
    This function starts the game loop in a separate thread.

    Args:
        None

    Returns:
        None
    """
    game_thread = th.Thread(target=game_loop)
    game_thread.daemon = True
    game_thread.start()


def main():
    """
    This function initializes the game.

    Args:
        None

    Returns:
        None
    """
    global app, actual_piece

    app = tk.Tk()
    app.attributes("-fullscreen", True)

    app.bind("<KeyPress>", key_press)
    start_game_loop_in_thread()

    app.mainloop()


if __name__ == "__main__":
    main()
