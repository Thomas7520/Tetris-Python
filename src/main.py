import sys, os
import utils

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "login"))
import sign_up

if __name__ == "__main__":    
    if not os.path.isdir(utils.database_path):
        os.mkdir(utils.database_path)
        utils.create_empty_csv()
    
    if not os.path.exists(utils.database_path / utils.database_name):
        utils.create_empty_csv()
        
    sign_up.run()