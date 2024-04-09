import sys, os
import utils

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "login"))
import sign_up

if __name__ == "__main__":
    #sign_up.run()
    
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_root = os.path.join(root_path, "database")
    
    if not os.path.isdir(database_root):
        os.mkdir(database_root)
    
    dict_test = ["test@gmail.com", "oqjof^z", "test"]
    utils.write_csv(os.path.join(database_root, "database.csv"), dict_test)
        
    print(utils.get_users_csv(os.path.join(database_root, "database.csv")))
    
    print(utils.has_account("test"))
    
    print(utils.check_password("test", "oqjof^z"))