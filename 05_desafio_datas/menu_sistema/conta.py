from config import config
from modelos import model
from modelos.util import limpar_console, log_transacao
from filtro.cliente import trazer_cliente_por_cpf


def menu_conta(clientes, contas):
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
           
        case 'l':
            print(config["listar"]["conta"], end="")
            if len(contas) > 0:
                print(config["listar"]["conta"], end="")
               
                for conta in model.ContaIterador(contas):
                    print(conta)
            else:
                print(config["mensagem"]["conta_inexistente"], end="")
        case 's':
            pass
        case _:
            print(config["mensagem"]["opcao_invalida"])
            
@log_transacao
def cadastrar_conta(contas, cliente):
    numero_conta = len(contas) + 1
    conta = model.ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print(f"{str(conta)} ")
    print(config["mensagem"]["conta_criada"], end="")