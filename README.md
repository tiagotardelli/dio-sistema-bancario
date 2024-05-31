# dio-sistema-bancario
Sitema bancário para entrega do projeto de desafio

# Escopo
Criar um sistema bancário com as operações: sacar, depositar e visualizar extrato
##
### Operação Depósito:
Deve ser possível depositar valores positivos para conta bancária. A v1 do projeto deve trabalhar apenas com 1 usuário, dessa forma não é necessário se preocupar com identificação do número da agência e conta bancária. Todos os depósitos devem ser armazenados em uma variável e exibidos na operação de extrato.
### Operação de Saque:
O sistema deve permitir realizar 3 saques diários com limite máximo de R$500,00 por saque. Caso o usuário não tenha saldo em conta, o sistema deve exibir uma mensagem informando que não será possível sacar o dinheiro por falta de saldo. Todos os sques devem ser armazenados em uma variável e exibidos na operação de extrato.
### Operação de extrato
Essa operação deve listar todos os depósitos e saques realizados na conta. No fim da listagem deve ser exibido o saldo atual da conta.
Os valores devem ser exibidos utilizando o formato R$ XXX.XX, exemplo:
1500.45 = R$ 1500.45

### Diário de Usuário
O sistema pede para que seja selecionada uma das opções em tela
Aloke seleciona a opção de [d] Depósito, o sistema abre a tela de deposito
Aloke digita o valor a ser depositado e o sitema valida se é um valor positivo
Caso seja um valor negativo uma mensagem aparece na tela
o sistema registra o tipo de operação, a data da operação e o valor
Aloke seleciona a opção de [s] Saque, o sistema abre a tela de saque
Na tela de saque é exibido o valor disponível em conta e a quantiade de saques ainda restantes
Aloke digita o valor a ser sacado, caso a quantidade de saques ou o valor a ser sacado seja maior
que o disponível em conta, será exibida uma mensagem. Se estiver tudo certo será exibido o valor
sacado e registrada o tipo de operação, a data da operação e o valor
Aloke digita a opção de extrato para validar o que tem em conta
O Sistema abre a tela de extrato e exibe todas as operações executadas e sua respectiva data
Ao final do extrato é exibido o valor do saldo atual da conta 
Valores devem ser exibidos como R$ XXX.XX