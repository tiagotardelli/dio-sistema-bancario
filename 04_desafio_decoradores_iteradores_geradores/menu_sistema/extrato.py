from config import config
from modelos.util import limpar_console, log_transacao
from modelos import model
from filtro.cliente import trazer_cliente_por_cpf
from filtro.conta import trazer_conta_cliente


def menu_extrato(clientes):
    limpar_console()
    print(config["menu"]['extrato'], end="")
    cpf = int(input(config["input"]['cpf_cliente']))
    cliente = trazer_cliente_por_cpf(clientes, cpf)
    
    if not cliente:
        print(config["mensagem"]["cliente_inexistente"])
    
    conta = trazer_conta_cliente(cliente)
    if not conta:
        return

    limpar_console()
    print(config["menu"]['extrato'], end="")
    
        
    extrato = ""
    tem_trascao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_trascao = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    if not tem_trascao:
        extrato = "Não foram realizadas movimentações"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")