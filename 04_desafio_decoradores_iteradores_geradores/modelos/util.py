from datetime import datetime

import os
import functools

def limpar_console():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def log_transacao(funcao):
    @functools.wraps(funcao)
    def envelope(*args, **kwargs):
        funcao(*args, **kwargs)
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}: {funcao.__name__}")
    return envelope