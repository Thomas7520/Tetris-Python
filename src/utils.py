import os, re, csv
from PIL import Image, ImageTk


root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

image_path = os.path.join(root_path, "images")
database_path = os.path.join(root_path, "database")
database_name = "database.csv"

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
    return ImageTk.PhotoImage(Image.open(f"{image_path}\\{name}").resize((width, height)))
    

def get_users_csv(path: str) -> list:
    with open(path, 'r') as file:
        users_list = []
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            users_list.append(row)
    return users_list

def write_csv(new_user: list) -> None:
        with open(os.path.join(database_path, "database.csv"), 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(new_user)
            

def username_exist(username : str) -> bool:
    for user in get_users_csv(database_path + "\\" + database_name):
        if username in user:
            return True
    return False

def email_exist(email : str) -> bool:
    for user in get_users_csv(database_path + "\\" + database_name):
        if email in user:
            return True
    return False

def check_password(username : str, password : str) -> bool:
    for user in get_users_csv(database_path + "\\" + database_name):
        if username in user:
            if password == user[1]:
                return True
            else:
                return False
    return False