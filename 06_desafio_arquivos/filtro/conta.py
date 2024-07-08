from config import CONFIG

def trazer_conta_cliente(cliente):
    if not cliente.contas:
        print(CONFIG["mensagem"]["conta_inexistente"])
        return
    else:
        quantidade_conta = len(cliente.contas)
        
        contador = 0
        print(CONFIG["opcao"]["conta"])
        while contador < quantidade_conta:
            print(f"[{contador}] - Agência {cliente.contas[contador].agencia} C/C {cliente.contas[contador].numero}")
            contador += 1
        print("#############################")

        opcao = int(input(CONFIG["input"]["opcao"]))
        return cliente.contas[opcao]
    return None