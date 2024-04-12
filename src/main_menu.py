import sys, argparse

def run():
    pass

if "__main__" == __name__:
    parser = argparse.ArgumentParser(description="Username")
    parser.add_argument("username", type=str, help="Username connected")
    args = parser.parse_args()
    
    print(args.username)
    