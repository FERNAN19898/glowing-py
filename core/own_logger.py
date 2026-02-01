import os

class Logger():
    
    def info(message: str):
        print(f"[INFO]: {message}")
    
    def error(message: str):
        print(f"[ERROR]: {message}")
    
    def log(message: str):
        print(f"[LOG]: {message}")
    
    def debug(message: str):
        print(f"[DEBUG]: {message}")
    
    def warning(message: str):
        print(f"[WARNING]: {message}")
    
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')