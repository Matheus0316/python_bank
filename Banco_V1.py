menu = f"""
[D] Depositar
[S] Sacar
[E] Extrato
[Q] Sair

"""

LIMITE = 500
SAQUES_DIARIOS = 3
saldo = 0
deposito = 0
saque = 0
extrato = f"""O saldo atual é de R$ {saldo:.2f}
Movimentação:
        """
numero_de_saques = 0

escolha = input(menu).upper()

while True:
    if escolha == "D":
        deposito = float(input("Insira o valor do deposito: "))
        if deposito < 0:
            print("Não foi possivel realizar a operação. Deposito negativo")
        else:
            saldo += deposito
            extrato += f"\nDeposito de R$ {deposito:.2f}"

    elif escolha == "S":
        saque = float(input("Insira o valor a ser sacado: "))

        if saque > LIMITE:
            print(
                "Não foi possivel realizar a operação. O saque excedeu o limite de saque.")

        elif numero_de_saques == SAQUES_DIARIOS:
            print(
                "Não foi possivel realizar a operação. O limite de saques diarios foi atingido.")

        elif saque < 0:
            print("Não foi possivel realizar a operação. Saque negativo.")

        elif saque > saldo:
            print(
                "Não foi possivel realizar a operação. Você não possui saldo o suficiente.")

        else:
            saldo -= saque
            numero_de_saques += 1
            extrato += f"\nSaque de R$ {saque:.2f}"

    elif escolha == "E":
        print(extrato)

    elif escolha == "Q":
        break

    else:
        print("Operação invalida, por favor selecione novamente a operação desejada")

    escolha = input(menu).upper()
