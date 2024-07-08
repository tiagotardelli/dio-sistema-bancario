from config import CONFIG
from modelos.util import limpar_console

def menu_principal():
    print(CONFIG["menu"]["inicial"], end="")
    opcao = input(CONFIG["input"]["opcao"])
    limpar_console()
    
    return opcao