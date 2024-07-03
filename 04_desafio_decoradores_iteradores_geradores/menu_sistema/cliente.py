from config import config
from modelos import model
from datetime import datetime
from modelos.util import limpar_console, log_transacao

import re

def menu_cliente(clientes):
    limpar_console()
    print(config["menu"]["cliente"], end="")
    opcao_menu = input(config["input"]["opcao"])

    match opcao_menu:
        case "n":
            limpar_console()
            print(config["novo"]["cliente"], end="")
            
            cadastrar_cliente(clientes)
        
        case "l":
            if len(clientes) > 0:
                print(config["listar"]["cliente"], end="")
                for cliente in clientes:
                    print(f"{str(cliente)}", end="")
        
        case "v":
            return

@log_transacao
def cadastrar_cliente(clientes):
    cliente =  preencher_campos_cliente(clientes) 
    clientes.append(cliente)
    print(config["mensagem"]["cliente_criado"], end="")
    print(f"{cliente}")

def preencher_campos_cliente(clientes):
    cpf = 0
    while True:
        try:    
            cpf = int(input(config["input"]["cpf"]))
            
            tamanho_invalido = not len(str(abs(cpf))) == 11
            cpf_cadastrado = cpf in clientes

            if tamanho_invalido:
                print(config["mensagem"]["cpf_invalido"], end="")
            elif cpf_cadastrado:
                print(config["mensagem"]["cpf_duplicado"], end="")
            else:
                break
        except ValueError:
            print(config["mensagem"]["numero_invalido"], end="")
    
    nome = ""
    while True:
        nome = input(config["input"]["nome"])
        validar_nome = not re.match("^[A-Za-z ]+$", nome)

        if validar_nome:
            print(config["mensagem"]["nome_invalido"], end="")
        else:
            break
    
    data_nascimento = ""
    while True:
        try:
            data_nascimento = datetime.strptime(input(config["input"]["data_nascimento"]), '%d/%m/%Y')
            break
        except ValueError:
            print(config["mensagem"]["data_invalida"], end="")
    
    endereco = ""
    while True:
        logradouro = input(config["input"]["endereco_logradouro"])
        numero = input(config["input"]["endereco_numero"])
        bairro = input(config["input"]["endereco_bairro"])
        cidade = input(config["input"]["endereco_cidade"])
        estado = input(config["input"]["endereco_estado"])
        
        endereco = model.Endereco(logradouro, numero, bairro, cidade, estado)

        if input(f"O endereco {endereco} está correto? [s]Sim [n]Não: ") == 's':
            break
            
    return model.PessoFisica(cpf, nome, data_nascimento, endereco)