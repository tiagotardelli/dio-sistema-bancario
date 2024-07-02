import os
import time
import re

from datetime import datetime

def limpar_console():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def menu_usuario(configuracao, usuarios):
    limpar_console()
    print(configuracao["menu"]["cadastro_usuario"]["inicial"], end="")
    opcao = input()

    match opcao:
        case 'n':
            usuario = cadastrar_usuario(usuarios=usuarios,
                                        cpf=preencher_cpf(configuracao, usuarios),
                                        nome=preencher_nome(configuracao),
                                        data_nascimento=preencher_data_nascimento(configuracao),
                                        endereco=preencher_endereco(configuracao))
            print("Usuário cadastrado com sucesso!\n"+
                  f"{usuario["nome"]}")
        case 'l':
            if len(usuarios) > 0:
                for chave in usuarios:
                    print(f"{usuarios[chave]["cpf"]} " +
                        f"{usuarios[chave]["nome"]} " +
                        f"{usuarios[chave]["data_nascimento"]} " +
                        f"{usuarios[chave]["endereco"]}")
            else:
                print("Não existem usuários cadastrados.")
        case 's':
            pass
        case _:
            print("Nenhuma opção valida para o digitado. Favor escolher novamente.")

def cadastrar_usuario(*,usuarios, cpf, nome, data_nascimento, endereco):
    usuarios.update({str(cpf):{"cpf": str(cpf), "nome": nome, "data_nascimento": data_nascimento,
                               "endereco": endereco}})
    return usuarios.get(str(cpf), {})

def preencher_cpf(configuracao, usuarios):
    while True:
        limpar_console()
        print(configuracao["menu"]["cadastro_usuario"]["cpf"], end="")
        try:    
            cpf = int(input())

            tamanho_invalido = not len(str(abs(cpf))) == 11
            cpf_cadastrado = cpf in usuarios

            if tamanho_invalido:
                print("CPF deve conter 11 dígitos.")
            elif cpf_cadastrado:
                print("CPF já cadastrado.")
            else:
                return cpf

        except ValueError:
            print("Entrada inválida. Favor insira somente números")

        time.sleep(4)
        limpar_console()
        print(configuracao["menu"]["cadastro_usuario"]["inicial"], end="")

def preencher_nome(configuracao):
    while True:
        limpar_console()
        print(configuracao["menu"]["cadastro_usuario"]["nome"], end="")

        nome = input()

        validar_nome = not re.match("^[A-Za-z ]+$", nome)

        if validar_nome:
            print("Digite nome e sobrenome. Somente letras são permitidas.")
        else:
            return nome
        
        time.sleep(4)

def preencher_data_nascimento(configuracao):
    while True:
        limpar_console()
        print(configuracao["menu"]["cadastro_usuario"]["data_nascimento"], end="")
        try:
            data_nascimento = datetime.strptime(input(), '%d/%m/%Y')
            return data_nascimento
        except ValueError:
            print("Entrada inválida. Favor insira uma data valida.")

    time.sleep(4)

def preencher_endereco(configuracao):
    while True:
        limpar_console()
        print(configuracao["menu"]["cadastro_usuario"]["endereco"]["logradouro"], end="")
        logradouro = input()
        print(configuracao["menu"]["cadastro_usuario"]["endereco"]["numero"], end="")
        numero = input()
        print(configuracao["menu"]["cadastro_usuario"]["endereco"]["bairro"], end="")
        bairro = input()
        print(configuracao["menu"]["cadastro_usuario"]["endereco"]["cidade_estado"], end="")
        cidade_estado = input()
        endereco = logradouro + ", " + numero + " - " + bairro + " - " + cidade_estado
        print(f"O endereço {endereco} está correto? [s]Sim [n]Não\n=>", end="")
        if input() == 's':
            return endereco

def menu_conta(configuracao, usuarios, contas, AGENCIA):
    limpar_console(),
    print(configuracao["menu"]["cadastro_conta"]["inicial"], end="")
    opcao = input()

    match opcao:
        case 'n':
            print(configuracao["menu"]["cadastro_conta"]["cpf"], end="")
            cpf = input()
            usuario = usuarios.get(str(cpf), None)
            if usuario == None:
                print("Usuário não cadastrado.")
            else:
                id_conta = len(contas) + 1
                conta = cadastrar_conta(contas, AGENCIA, id_conta, usuario["cpf"])
                print(f"Agência: {conta["agencia"]}\n" +
                      f"Conta: {conta["conta"]}\n" +
                      f"Usuário: {conta["usuario"]}\n" +
                      "Cadastrado com sucesso!")
        case 'l':
            if len(contas) > 0:
                for chave in contas:
                    print(f"{contas[chave]["agencia"]} " +
                        f"{contas[chave]["conta"]} " +
                        f"{contas[chave]["usuario"]} " +
                        f"{contas[chave]["saldo"]:.2f}")
            else:
                print("Nenhuma conta cadastrada.", end="")
        case 's':
            pass
        case _:
            print("Nenhuma opção valida para o digitado. Favor escolher novamente.")

def cadastrar_conta(contas, agencia, conta, cpf, /):
    contas.update({conta:{"agencia":agencia,"conta":conta,"usuario":cpf,"saques_feitos":0, "saldo":0.0,"extratos":{}}})
    return contas.get(int(conta), {})

def menu_depositar(configuracao, contas):
    limpar_console(),
    print(configuracao["menu"]["depositar"]["inicial"], end="")
    print(configuracao["menu"]["depositar"]["agencia"], end="")
    numero_agencia = input()
    
    agencia_valida = not any(numero_agencia in subdict.values() for subdict in contas.values())

    if agencia_valida:
        print("Agência não existe.")
        pass

    print(configuracao["menu"]["depositar"]["conta"], end="")
    numero_conta = int(input())
    conta = contas.get(numero_conta, None)

    if conta == None:
        print("Conta inválida.")
        pass

    try:
        print(configuracao["menu"]["depositar"]["valor"], end="")
        valor = float(input())
        if valor > 0:
            saldo, extrato  = depositar(conta, valor, conta["extratos"])
            limpar_console()
            print(f"Deposito no valor R$ {valor:.2f} realizado com sucesso.")
            print(f"Efetuado o {extrato["operacao"]} no dia {extrato["data"]}" +
                  f" no valor de R$ {extrato["valor"]:.2f}")
            print(f"Seus saldo em conta é de {saldo}")
        else:
            print("Somente valores positivos são aceitos para Depósito.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")

def depositar(conta, valor, extratos, /):
    conta["saldo"] = conta["saldo"] + valor
    data_atual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    id_extrato = len(extratos) + 1
    extratos[id_extrato] = {
        'operacao': "Depósito",
        'data': data_atual,
        'valor': valor
    }
    extrato = extratos.get(id_extrato, {})
    return conta["saldo"], extrato

def menu_sacar(configuracao, contas, LIMITE_SAQUES):
    limpar_console(),
    print(configuracao["menu"]["sacar"]["inicial"], end="")
    print(configuracao["menu"]["sacar"]["agencia"], end="")
    numero_agencia = input()
    
    agencia_valida = not any(numero_agencia in subdict.values() for subdict in contas.values())

    if agencia_valida:
        print("Agência não existe.")
        pass

    print(configuracao["menu"]["sacar"]["conta"], end="")
    numero_conta = int(input())
    conta = contas.get(numero_conta, None)

    if conta == None:
        print("Conta inválida.")
        pass

    try:
        print(configuracao["menu"]["sacar"]["valor"], end="")
        valor = float(input())
        
        if valor > 0:
            if valor <= conta["saldo"]:
                if valor <= 500.00:
                    if conta["saques_feitos"] <= LIMITE_SAQUES:
                        conta["saques_feitos"] += 1
                        saldo, extrato  = sacar(conta=conta, valor=valor, extratos=conta["extratos"])
                        limpar_console()
                        print(f"Saque no valor R$ {valor:.2f} realizado com sucesso.")
                        print(f"Efetuado o {extrato["operacao"]} no dia {extrato["data"]}" +
                              f" no valor de R$ {extrato["valor"]:.2f}")
                        print(f"Seus saldo em conta é de {saldo}")
                    else:
                        print("Quantidade de saques exedeu o permitido.")
                else:
                    print("Não é permitido saque maior que R$ 500.00")
            else:
                print("Valor maior do que você pussui em conta.")
                pass;
        else:
            print("Somente valores positivos são aceitos para Saque.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")

def sacar(*, conta, valor, extratos):
    conta["saldo"] = conta["saldo"] - valor
    data_atual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    id_extrato = len(extratos) + 1
    extratos[id_extrato] = {
        'operacao': "Saque",
        'data': data_atual,
        'valor': valor
    }
    extrato = extratos.get(id_extrato, {})
    return conta["saldo"], extrato

def menu_extrato(configuracao, contas):
    limpar_console(),
    print(configuracao["menu"]["sacar"]["inicial"], end="")
    print(configuracao["menu"]["sacar"]["agencia"], end="")
    numero_agencia = input()
    
    agencia_valida = not any(numero_agencia in subdict.values() for subdict in contas.values())

    if agencia_valida:
        print("Agência não existe.")
        pass

    print(configuracao["menu"]["sacar"]["conta"], end="")
    numero_conta = int(input())
    conta = contas.get(numero_conta, None)

    if conta == None:
        print("Conta inválida.")
        pass

    if len(conta["extratos"]) > 0: 
        extratos = conta["extratos"]
        limpar_console()
        for chave in extratos:   
            print(f"Data {extratos[chave]["data"]} Operação {extratos[chave]["operacao"]} Valor {extratos[chave]["valor"]:.2f}")
        print(f"Saldo em conta de {conta["saldo"]:.2f}")
    else:
        print("Não existe extrato.")

def menu(configuracao):
    print(configuracao["menu"]["inicial"], end="")
    opcao = input()
    limpar_console()
    return opcao

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "001"

    configuracao = {
        "menu": {
            "inicial": "[u] Castrar Usuário\n[c] Cadatrar Conta\n[d] Depósito\n[s] Sacar\n""[e] Extrato\n[s] Sair\n=> ",
            "cadastro_usuario": {
                "inicial": "Cadastrar Usuário\n##########################\n" +
                        "[n] Novo Usuário\n[l] Listar Usuário\n[s] Sair\n=>",
                "cpf": "Digite o CPF\n=>",
                "nome": "Digite o Nome\n=>",
                "data_nascimento": "Digite a Data de Nascimento (DD/MM/YYYY)\n=>",
                "endereco": {
                    "logradouro": "Digite o logradouro\n=>",
                    "numero": "Digite o número\n=>",
                    "bairro": "Digite o bairro\n=>",
                    "cidade_estado": "Digite a cidade/estado\n=>" 
                }
            },
            "cadastro_conta": {
                "inicial": "Cadastrar Conta\n##########################\n" + 
                        "[n] Nova Conta\n[l] Listar Contas\n[s] Sair\n=>",
                "cpf": "Digite o CPF do usuário\n=>"
            },
            "depositar": {
                "inicial": "Despositar\n##########################\n",
                "agencia": "Digite a agência\n=>",
                "conta": "Digite a conta\n=>",
                "valor": "Digite o valor a ser depositado\n=>"
            },
            "sacar": {
                "inicial": "Sacar\n##########################\n",
                "agencia": "Digite a agência\n=>",
                "conta": "Digite a conta\n=>",
                "valor": "Digite o valor a ser sacado\n=>"
            },
            "extrato": {
                "inicial": "Extrato\n##########################\n",
                "agencia": "Digite a agência\n=>",
                "conta": "Digite a conta\n=>",
            }
        }
    }
    usuarios = {}
    contas = {}

    while True:
        opcao = menu(configuracao)
        match opcao:
            case 'u':
                menu_usuario(configuracao, usuarios)
            case 'c':
                menu_conta(configuracao, usuarios, contas, AGENCIA)
            case 'd':
                menu_depositar(configuracao, contas)
            case "s":
                menu_sacar(configuracao, contas, LIMITE_SAQUES)
            case "e": 
                menu_extrato(configuracao, contas)
            case "s":
                break;
            case _:
                print("Nenhuma opção valida para o digitado. Favor escolher novamente.")

        time.sleep(4)
        limpar_console()
if __name__ == "__main__":
    main()
