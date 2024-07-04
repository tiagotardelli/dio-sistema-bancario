from config import config
from modelos import model
from modelos.util import limpar_console, log_transacao
from filtro.cliente import trazer_cliente_por_cpf
from filtro.conta import trazer_conta_cliente

def menu_transacao(clientes, tipo_transcao):
    limpar_console()
   
    if tipo_transcao == 'D':
        print(config["menu"]['depositar'], end="")
        cpf = int(input(config["input"]['cpf_cliente']))
        
        efetivar_transcao(cpf, clientes, 'D')
    elif tipo_transcao == 'S':
        print(config["menu"]['sacar'], end="")
        cpf = int(input(config["input"]['cpf_cliente']))
        
        efetivar_transcao(cpf, clientes, 'S')

@log_transacao
def efetivar_transcao(cpf, clientes, tipo_transcao):
    cliente = trazer_cliente_por_cpf(clientes, cpf)
    
    if not cliente:
        print(config["mensagem"]["cliente_inexistente"])
        
    valor = float(input(config["input"]["valor"]))
    
    transacao = (model.Saque(valor) if tipo_transcao == 'S' else model.Deposito(valor))

    conta = trazer_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)