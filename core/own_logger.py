import os

class Logger():
    def __init__(self):
        pass
    
    def info(self, message: str):
        print(f"[INFO]: {message}")
    
    def error(self, message: str):
        print(f"[ERROR]: {message}")
    
    def log(self, message: str):
        print(f"[LOG]: {message}")
    
    def debug(self, message: str):
        print(f"[DEBUG]: {message}")
    
    def warning(self, message: str):
        print(f"[WARNING]: {message}")
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')