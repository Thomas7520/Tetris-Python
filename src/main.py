import sys, os
import utils
import login

if __name__ == "__main__":    
    if not os.path.isdir(utils.database_path):
        os.mkdir(utils.database_path)
        utils.create_empty_csv()
    
    if not os.path.exists(utils.database_path / utils.database_name):
        utils.create_empty_csv()
        
    login.run()