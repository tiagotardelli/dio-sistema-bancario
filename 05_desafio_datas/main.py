from config import config
from modelos.util import limpar_console
from menu_sistema import principal, cliente, conta, transacao, extrato

import time

def main() -> None:
    clientes = []
    contas = []

    while True:
        limpar_console()
        opcao = principal.menu_principal()
        match opcao:
            case 'u':
                cliente.menu_cliente(clientes)
            case 'c':
                conta.menu_conta(clientes, contas)
            case "d":
                transacao.menu_transacao(clientes, 'D')
            case "a":
                transacao.menu_transacao(clientes, 'S')
            case "e":
                extrato.menu_extrato(clientes)
            case "s":
                break
            case _:
                print(config["mensagem"]["opcao_invalida"], end="")
        time.sleep(10)

if __name__ == "__main__":
    main()
