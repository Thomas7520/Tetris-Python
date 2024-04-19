import os
import utils
import login

if __name__ == "__main__":    
    if not os.path.isdir(utils.database_path):
        os.mkdir(utils.database_path)
        
    login.run()