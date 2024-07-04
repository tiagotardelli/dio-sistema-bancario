from config import config
from modelos.util import limpar_console

def menu_principal():
    print(config["menu"]["inicial"], end="")
    opcao = input(config["input"]["opcao"])
    limpar_console()
    
    return opcao