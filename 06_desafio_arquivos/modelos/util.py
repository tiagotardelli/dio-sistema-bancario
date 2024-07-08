from datetime import datetime
from arquivos import LOG_FILE

import os
import functools

def limpar_console():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def log_transacao(func):
    @functools.wraps(func)
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        
        data_hora = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        gravar_log(f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. Retornou {resultado}\n")
       
        return resultado

    return envelope

def gravar_log(descricao):
    try:
        with LOG_FILE.open('a', encoding='utf-8') as arquivo:
            arquivo.write(descricao)
    except IOError as exc: 
        print("Erro ao abrir o arquivo {exc}")
    