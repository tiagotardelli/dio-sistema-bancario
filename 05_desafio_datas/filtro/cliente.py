def trazer_cliente_por_cpf(clientes, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None