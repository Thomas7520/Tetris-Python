import re, csv, os
import subprocess
import bcrypt
import tkinter
from customtkinter import CTkImage
from PIL import Image
import ast

from tempfile import NamedTemporaryFile
import shutil

from pathlib import Path

global root_path, image_path, database_path, database_name
root_path = Path(__file__).resolve().parent.parent
image_path = root_path / "images"

database_path = root_path / "database"

# 0: username, 1: email, 2: password
database_users = "database_users.csv"
# 0: username, 1: highscore, 2: bind
database_options = "database_options.csv"

default_bind_options = [['Rotation', (80, 'Up')], ['Chute lente', (40,'Down')],['Gauche', (37,'Left')],['Droite', (39,'Right')],['Chute rapide', (32, 'Space')], ['Garder', (67, 'C')]]

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
    if not os.path.exists(database_path / database_users):
        return []
    
    with open(path, 'r') as file:
        users_list = []
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            users_list.append(row)
    return users_list

def add_user_csv(new_user: list) -> None:
        with open(database_path / database_users, 'a', newline='') as file_users:
            new_user[2] = bcrypt.hashpw(new_user[2].encode('utf-8'), bcrypt.gensalt())
            writer = csv.writer(file_users, delimiter=';')
            writer.writerow(new_user)

def add_user_options_csv(new_user: list):
    with open(database_path / database_options, 'a', newline='') as file_options:
            user_options = [new_user[0], 0, default_bind_options]
            writer = csv.writer(file_options, delimiter=';')
            writer.writerow(user_options)
            
def username_exist(username : str) -> bool:
    for user in get_users_csv(database_path / database_users):
        if username in user:
            return True
    return False

def email_exist(email : str) -> bool:
    for user in get_users_csv(database_path / database_users):
        if email in user:
            return True
    return False

def check_password(username : str, password : str) -> bool:
    for user in get_users_csv(database_path / database_users):
        if username in user:
            if bcrypt.checkpw(password.encode("utf-8"), bytes(user[2][2:-1], 'utf8')): # Pas le choix ainsi car le str est déjà encodé mais si on le reconverti il sera doublement encodé, ce que bcrypt ne va pas apprécier
                return True
            else:
                return False
    raise ValueError('Could not find user with username %s' % username)

def get_highscore(username: str):
    for user_options in get_users_csv(database_path / database_options):
        if username in user_options:
            return user_options[1]
        
    raise ValueError('Could not find user with username %s' % username)

def add_highscore(username: str, score: int):
    temp_file = NamedTemporaryFile(mode='w', delete=False, newline='', dir=database_path)

    with open(database_path / database_options, 'r', newline='') as csvfile, temp_file:
        reader = csv.reader(csvfile, delimiter=';')
        writer = csv.writer(temp_file, delimiter=';')
        
        for row in reader:
            if row[0] == username:
                writer.writerow([row[0], score, ast.literal_eval(row[2])])
            else:
                writer.writerow([row[0], row[1], ast.literal_eval(row[2])])

    shutil.move(temp_file.name, database_path / database_options)

def get_bind_options(username : str):
    for user_options in get_users_csv(database_path / database_options):
        if username in user_options:
            return ast.literal_eval(user_options[2])
        
    raise ValueError('Could not find user with username %s' % username)

def update_bind_options(username: str, bind_options: list):
    temp_file = NamedTemporaryFile(mode='w', delete=False, newline='', dir=database_path)

    with open(database_path / database_options, 'r', newline='') as csvfile, temp_file:
        reader = csv.reader(csvfile, delimiter=';')
        writer = csv.writer(temp_file, delimiter=';')
        
        for row in reader:
            if row[0] == username:
                writer.writerow([row[0], row[1], bind_options])
            else:
                writer.writerow([row[0], row[1], ast.literal_eval(row[2])])

    shutil.move(temp_file.name, database_path / database_options)
    


def create_empty_csv(file_name: str):
    with open(database_path / file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([])
        
        
def reset_grids(app : tkinter.Tk):
    for slave in app.grid_slaves():
        slave.destroy()
    
    for i in range(app.grid_size()[0]):
        app.grid_columnconfigure(i, weight=0, minsize=0)
    
    for i in range(app.grid_size()[1]):
        app.grid_rowconfigure(i, weight=0, minsize=0)