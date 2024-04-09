import os, re
from PIL import Image, ImageTk


chemin_images = os.path.abspath(os.path.join(os.getcwd(), "images"))


def is_valid_email(email):
    return re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$').match(email)

def center_window(app, window_width, window_height):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    
def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


def get_image(name: str, width: int, height: int) -> ImageTk.PhotoImage:
    """
    Opens an image from the images folder and resizes it to the specified dimensions.

    Args:
        name (str): The name of the image file, without the extension.
        width (int): The desired width of the image.
        height (int): The desired height of the image.

    Returns:
        ImageTk.PhotoImage: The resized image.

    """
    return ImageTk.PhotoImage(Image.open(f"{chemin_images}/{name}").resize((width, height)))
    
