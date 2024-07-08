from config import CONFIG
from modelos import model
from datetime import datetime
from modelos.util import limpar_console, log_transacao

import re

def menu_cliente(clientes):
    limpar_console()
    print(CONFIG["menu"]["cliente"], end="")
    opcao_menu = input(CONFIG["input"]["opcao"])

    match opcao_menu:
        case "n":
            limpar_console()
            print(CONFIG["novo"]["cliente"], end="")
            
            cadastrar_cliente(clientes)
        
        case "l":
            if len(clientes) > 0:
                print(CONFIG["listar"]["cliente"], end="")
                for cliente in clientes:
                    print(f"{str(cliente)}", end="")
        
        case "v":
            return

@log_transacao
def cadastrar_cliente(clientes):
    cliente =  preencher_campos_cliente(clientes) 
    clientes.append(cliente)
    print(CONFIG["mensagem"]["cliente_criado"], end="")
    print(f"{cliente}")

def preencher_campos_cliente(clientes):
    cpf = 0
    while True:
        try:    
            cpf = int(input(CONFIG["input"]["cpf"]))
            
            tamanho_invalido = not len(str(abs(cpf))) == 11
            cpf_cadastrado = cpf in clientes

            if tamanho_invalido:
                print(CONFIG["mensagem"]["cpf_invalido"], end="")
            elif cpf_cadastrado:
                print(CONFIG["mensagem"]["cpf_duplicado"], end="")
            else:
                break
        except ValueError:
            print(CONFIG["mensagem"]["numero_invalido"], end="")
    
    nome = ""
    while True:
        nome = input(CONFIG["input"]["nome"])
        validar_nome = not re.match("^[A-Za-z ]+$", nome)

        if validar_nome:
            print(CONFIG["mensagem"]["nome_invalido"], end="")
        else:
            break
    
    data_nascimento = ""
    while True:
        try:
            data_nascimento = datetime.strptime(input(CONFIG["input"]["data_nascimento"]), '%d/%m/%Y')
            break
        except ValueError:
            print(CONFIG["mensagem"]["data_invalida"], end="")
    
    endereco = ""
    while True:
        logradouro = input(CONFIG["input"]["endereco_logradouro"])
        numero = input(CONFIG["input"]["endereco_numero"])
        bairro = input(CONFIG["input"]["endereco_bairro"])
        cidade = input(CONFIG["input"]["endereco_cidade"])
        estado = input(CONFIG["input"]["endereco_estado"])
        
        endereco = model.Endereco(logradouro, numero, bairro, cidade, estado)

        if input(f"O endereco {endereco} está correto? [s]Sim [n]Não: ") == 's':
            break
            
    return model.PessoFisica(cpf, nome, data_nascimento, endereco)