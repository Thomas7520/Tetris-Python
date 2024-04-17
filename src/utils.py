import re, csv
import subprocess
import bcrypt
from customtkinter import CTkImage
from PIL import Image

from pathlib import Path

global root_path, image_path, database_path, database_name
root_path = Path(__file__).resolve().parent.parent
image_path = root_path / "images"

database_path = root_path / "database"
database_name = "database.csv"

def is_valid_email(email):
    return re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$').match(email)

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


def get_image(name: str, width: int, height: int) -> CTkImage:
    """
    Opens an image from the images folder and resizes it to the specified dimensions.

    Args:
        name (str): The name of the image file, without the extension.
        width (int): The desired width of the image.
        height (int): The desired height of the image.

    Returns:
        CTkImage: The resized image.

    """
    
    return CTkImage(light_image=Image.open(image_path / name),
                                  dark_image=Image.open(image_path / name),
                                  size=(width * 0.8, height * 0.8))    

def exec_python(path_script: str, args=[]) -> None:
    try:
        subprocess.Popen(['python', path_script] + args)
    except FileNotFoundError:
        subprocess.Popen(['python3', path_script] + args)

    
def get_users_csv(path: str) -> list:
    with open(path, 'r') as file:
        users_list = []
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            users_list.append(row)
    return users_list

def write_csv(new_user: list) -> None:
        with open(database_path / database_name, 'a', newline='') as file:
            new_user[2] = bcrypt.hashpw(new_user[2].encode('utf-8'), bcrypt.gensalt())
            writer = csv.writer(file, delimiter=';')
            writer.writerow(new_user)
            

def username_exist(username : str) -> bool:
    for user in get_users_csv(database_path / database_name):
        if username in user:
            return True
    return False

def email_exist(email : str) -> bool:
    for user in get_users_csv(database_path / database_name):
        if email in user:
            return True
    return False

def check_password(username : str, password : str) -> bool:
    for user in get_users_csv(database_path / database_name):
        if username in user:
            if bcrypt.checkpw(password.encode("utf-8"), bytes(user[2][2:-1], 'utf8')): # Pas le choix ainsi car le str est déjà encodé mais si on le reconverti il sera doublement encodé, ce que bcrypt ne va pas apprécier
                return True
            else:
                return False
    return False

def create_empty_csv():
    with open(database_path / database_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([])