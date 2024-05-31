import os
import time

from datetime import datetime


LIMITE_SAQUES = 3
saques_dia = 0
conta_bancaria = 0.0
extrato_conta = {}

def exibir_menu():
    print("""
          [d] Depósito
          [s] Sacar
          [e] Extrato
          [q] Sair
          => """, end="")

def limpar_console():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def processar_transacao(operacao, valor):
    global conta_bancaria

    if operacao not in ['S', 'D']:
        raise ValueError("Tipo de operação inválida. Use 'Depósito' ou 'Saque'.")
    data_atual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    conta_bancaria += valor * (-1 if operacao == 'S' else 1)
    
    id_extrato = len(extrato_conta) + 1
    
    extrato_conta[id_extrato] = {
        'operacao': operacao,
        'data': data_atual,
        'valor': valor
    }

def menu_deposito():
    limpar_console()
    while True:
        print("""
            Deposito
            ####################################
            Digite um valor =>  """, end="")
        try:
            valor_digitado = float(input())
            if valor_digitado > 0:
                processar_transacao('D', valor_digitado)
                limpar_console()
                print(f"Depositado no valor R$ {valor_digitado:.2f} realizado com sucesso.")
                break;
            else:
                print("Somente valores positivos são aceitos para Depósito.")
        except ValueError:
             print("Entrada inválida. Por favor, insira um número.")

def menu_saque():
    global saques_dia

    limpar_console()
    while True:
        print("""
            Saque
            ####################################
            Digite o valor a ser sacado => """, end="")
        try:
            valor_digitado = float(input())
            if valor_digitado > 0:
                if valor_digitado < conta_bancaria:
                    if valor_digitado <= 500.00:
                        if saques_dia <= LIMITE_SAQUES:
                            saques_dia += 1
                            processar_transacao('S', valor_digitado)
                            limpar_console()
                            print(f'Saque no valor R$ {valor_digitado:.2f} realizado com sucesso.')
                            break;
                        else:
                            print("Quantidade de saques exedeu o permitido.")
                    else:
                        print("Não é permitido saque maior que R$ 500.00")
                else:
                    print("Valor maior do que você pussui em conta.")
                    break;
            else:
                print("Somente valores positivos são aceitos para Saque.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def menu_extrato():
    limpar_console()
    print("""
        Extrato
        ####################################
           """)
    soma = 0.0
    for id_extrato, extrato in extrato_conta.items():
        soma += extrato['valor'] * (-1 if extrato['operacao'] == 'S' else 1)
        print(f'{extrato['data']} {extrato['operacao']} R$ {extrato['valor']:.2f}')
    print(f"Valor total em conta R$ {soma:.2f}")

def processar_opcao(opcao):
    if opcao == "d":
        return menu_deposito()
    elif opcao == "s":
        return menu_saque()
    elif opcao == 'e':
        return menu_extrato()
    elif opcao == "q":
        return "Saindo"
    else:
        "Operação inválida, por favor selecione novamente a operação desejada."

def main():
    while True:
        limpar_console()
        exibir_menu()
        opcao = input()
        opcao_escolhida = processar_opcao(opcao)

        if opcao == "q":
            break
        time.sleep(4)
if __name__ == '__main__':

    main()
