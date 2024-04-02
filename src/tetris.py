# Imports
import tkinter as tk
import playsound as ps
import time

# Grid size parameters
GRID_WIDTH = 10
GRID_HEIGHT = 24
CELL_SIZE = 30

# Colors parameters 
BACKGROUND_COLOR = "black"
GRID_COLOR = "gray"
BLOCK_COLORS = ["blue", "green", "red", "yellow", "orange", "purple", "cyan"]

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
    # Global canvas to use it in other functions
    global playfield_canvas 

    # Create the canvas to display the playfield and place it on the center of the screen
    playfield_canvas = tk.Canvas(app, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, bg=BACKGROUND_COLOR) 
    playfield_canvas.place(relx=0.5, rely=0.5, anchor="center") 

    # Calculate the starting position of the grid in the playfield
    start_x = 0
    start_y = 0

    # Draw the grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            x0, y0 = start_x + x * CELL_SIZE, start_y + y * CELL_SIZE # Calculate the starting position of the rectangle
            x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE # Calculate the ending position of the rectangle
            playfield_canvas.create_rectangle(x0, y0, x1, y1, outline=GRID_COLOR) # Draw the rectangle

def draw_block(x, y, color):
    """
    This function is used to draw a block on the tetris playfield.

    Args:
        x (int): La position x du bloc
        y (int): La position y du bloc
        color (str): La couleur du bloc

    Returns:
        None
    """
    # Coordinates of the upper left corner of the block
    x0 = x * CELL_SIZE
    y0 = y * CELL_SIZE

    # coordinates of the lower right corner of the block
    x1 = x0 + CELL_SIZE
    y1 = y0 + CELL_SIZE
    
    # Dessiner le bloc
    playfield_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

def draw_tetris_piece(x, y, shape_index):
    """
    This function draws a block on the tetris playfield .

    Args:
        x (int): The x position of the block
        y (int): The y position of the block
        color (str): The color of the block

    Returns:
        Piece

    """
    global piece, shape, color
    # Select color for the piece and get the shape of the piece
    color = BLOCK_COLORS[shape_index % len(BLOCK_COLORS)]  
    shape = TETRIS_SHAPES[shape_index]  
    
    # Draw each block of the piece
    for block in shape:
        piece = draw_block(x + block[0], y + block[1], color)
    return shape

def move_piece(direction):
    """
    This function moves the Tetris piece horizontally.

    Args:
        direction (str): The direction of movement ("left" or "right").

    Returns:
        None
    """
    global actual_piece

    if direction == "left":
        # Move the piece left
        actual_piece[0] -= 1
    elif direction == "right":
        # Move the piece right
        actual_piece[0] += 1
    elif direction == "down":
        actual_piece[1] += 1
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
        # Move the piece left when left arrow key is pressed
        move_piece("left")
    elif key == "Right":
        # Move the piece right when right arrow key is pressed
        move_piece("right")
    elif key == "Down":
        # Move the piece right when right arrow key is pressed
        move_piece("down")

def main():
    """
    This function is the main function of the application.

    Args:
        None

    Returns:
        None
    """
    global app, window_width, window_height, actual_piece 

    app = tk.Tk() 
    app.attributes("-fullscreen", True)
    window_width = app.winfo_screenwidth()
    window_height = app.winfo_screenheight()

    create_tetris_playfield()  
    actual_piece = [GRID_WIDTH // 2, 0, 0]  # Initial position of the piece

    draw_tetris_piece(actual_piece[0], actual_piece[1], actual_piece[2])

    # Bind key press events to the key_press function
    app.bind("<KeyPress>", key_press)

    app.mainloop() 

def game_loop():
    pass

if __name__ == "__main__":
    main()
    game_loop()