from pathlib import Path
from model import Endereco, Cliente, PessoFisica, Conta, ContaCorrente,Historico, Transacao, Saque, Deposito
from datetime import datetime

import os
import time
import re
import yaml

def limpar_console():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def menu_principal(config):
    print(config["menu"]["inicial"], end="")
    opcao = input(config["input"]["opcao"])
    limpar_console()
    return opcao

def menu_cliente(config, clientes):
    limpar_console()
    print(config["menu"]["cliente"], end="")
    opcao_menu = input(config["input"]["opcao"])

    match opcao_menu:
        case "n":
            limpar_console()
            print(config["novo"]["cliente"], end="")
            
            cliente =  preencher_campos_cliente(config, clientes) 
            cadastrar_cliente(config, clientes, cliente)
        
        case "l":
            if len(clientes) > 0:
                print(config["listar"]["cliente"], end="")
                for cliente in clientes:
                    print(f"{str(cliente)}", end="")
        
        case "v":
            return

def preencher_campos_cliente(config, clientes):
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
        
        endereco = Endereco(logradouro, numero, bairro, cidade, estado)

        if input(f"O endereco {endereco} está correto? [s]Sim [n]Não: ") == 's':
            break
            
    return PessoFisica(cpf, nome, data_nascimento, endereco)

def trazer_cliente_por_cpf(clientes, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def cadastrar_cliente(config, clientes, cliente):
    clientes.append(cliente)
    print(config["mensagem"]["cliente_criado"], end="")
    print(f"{cliente}")

def menu_conta(config, clientes, contas):
    limpar_console()
    print(config["menu"]["conta"], end="")
    opcao_menu = input(config["input"]["opcao"])
    
    match opcao_menu:
        case 'n':
            limpar_console()
            print(config["novo"]["conta"], end="")
            cpf = int(input(config["input"]["cpf_cliente"]))
            
            cliente = trazer_cliente_por_cpf(clientes, cpf)
            
            if not cliente:
                print(config["mensagem"]["cliente_inexistente"])
                return
            cadastrar_conta(contas, cliente)
            print(config["mensagem"]["conta_criada"], end="")
        case 'l':
            print(config["listar"]["conta"], end="")
            if len(contas) > 0:
                print(config["listar"]["conta"], end="")
                for conta in contas:
                    print(f"{str(conta)}")
            else:
                print(config["mensagem"]["conta_inexistente"], end="")
        case 's':
            pass
        case _:
            print(config["mensagem"]["opcao_invalida"])

def cadastrar_conta(contas, cliente):
    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print(f"{str(conta)} ")

def menu_depositar(config, clientes):
    limpar_console(),
    print(config["menu"]['depositar'], end="")
    cpf = int(input(config["input"]['cpf_cliente']))
    cliente = trazer_cliente_por_cpf(clientes, cpf)

    if not cliente:
        print(config["mensagem"]["cliente_inexistente"])
        
    valor = float(input(config["input"]["valor"]))
    transacao = Deposito(valor)
    
    conta = trazer_conta_cliente(config, cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
   
def trazer_conta_cliente(config, cliente):
    if not cliente.contas:
        print(config["mensagem"]["conta_inexistente"])
        return
    else:
        quantidade_conta = len(cliente.contas)
        
        contador = 0
        print(config["opcao"]["conta"])
        while contador < quantidade_conta:
            print(f"[{contador}] - Agência {cliente.contas[contador].agencia} C/C {cliente.contas[contador].numero}")
            contador += 1
        print("#############################")

        opcao = int(input(config["input"]["opcao"]))
        return cliente.contas[opcao]
    return None

def menu_sacar(config, clientes):
    limpar_console(),
    print(config["menu"]['sacar'], end="")
    cpf = int(input(config["input"]['cpf_cliente']))
    cliente = trazer_cliente_por_cpf(clientes, cpf)

    if not cliente:
        print(config["mensagem"]["cliente_inexistente"])
   
    valor = float(input(config["input"]["valor"]))
    transacao = Saque(valor)
    
    conta = trazer_conta_cliente(config, cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def menu_extrato(config, clientes):
    limpar_console()
    print(config["menu"]['extrato'], end="")
    cpf = int(input(config["input"]['cpf_cliente']))
    cliente = trazer_cliente_por_cpf(clientes, cpf)
    
    if not cliente:
        print(config["mensagem"]["cliente_inexistente"])
    
    conta = trazer_conta_cliente(config, cliente)
    if not conta:
        return

    limpar_console()
    print(config["menu"]['extrato'], end="")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = config["mensagem"]["extrato_sem_movimentacao"]
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")

def main() -> None:
    clientes = []
    contas = []
    caminho = Path(__file__).resolve().parent
    arquivo_yaml = caminho / "config.yaml"

    with arquivo_yaml.open('r', encoding='utf-8') as arquivo:
        config = yaml.safe_load(arquivo)

        while True:
            limpar_console()
            opcao = menu_principal(config)
            match opcao:
                case 'u':
                    menu_cliente(config, clientes)
                case 'c':
                    menu_conta(config, clientes, contas)
                case "d":
                    menu_depositar(config, clientes)
                case "a":
                    menu_sacar(config, clientes)
                case "e":
                    menu_extrato(config, clientes)
                case "s":
                    break
                case _:
                    print(config["mensagem"]["opcao_invalida"], end="")
            time.sleep(15)

if __name__ == "__main__":
    main()
