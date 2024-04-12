import sys, os
import utils

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "login"))
import sign_up

if __name__ == "__main__":
    
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_root = os.path.join(root_path, "database")
    
    if not os.path.isdir(database_root):
        os.mkdir(database_root)
        utils.create_empty_csv()
    
    sign_up.run()