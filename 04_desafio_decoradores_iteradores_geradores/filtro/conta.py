from config import config

def trazer_conta_cliente(cliente):
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