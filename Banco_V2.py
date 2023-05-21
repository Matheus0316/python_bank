def depositar(saldo, deposito, extrato, /):
    if deposito < 0:
        print("Não foi possivel realizar a operação. Deposito negativo")
    else:
        saldo += deposito
        extrato += f"\nDeposito de R$ {deposito:.2f}"
        return saldo, extrato


def sacar(*, saldo, saque, limite, saques, saques_diarios, extrato):

    if saque > limite:
        print(
            "Não foi possivel realizar a operação. O saque excedeu o limite de saque."
        )

    elif saques == saques_diarios:
        print(
            "Não foi possivel realizar a operação. O limite de saques diarios foi atingido."
        )

    elif saque < 0:
        print("Não foi possivel realizar a operação. Saque negativo.")

    elif saque > saldo:
        print(
            "Não foi possivel realizar a operação. Você não possui saldo o suficiente."
        )

    else:
        saques += 1
        saldo -= saque
        extrato += f"\nSaque de R$ {saque:.2f}"
        return saldo, extrato, saques


def exibir_extrato(saldo, extrato):
    print(f"O saldo atual é de R$ {saldo:.2f} \n")
    print("Não foram realizadas transações" if not extrato else extrato)


def criar_user(users):
    cpf = input("Insira o cpf: ")
    if verificar(cpf, users):
        print("Erro: esse cpf já está cadastrado")
        return
    else:
        nome = input("Insira o nome: ")
        data_de_nascimento = input("Insira a data de nascimento: ")
        endereco = input("Insira o endereco: ")
        print(f"Usuario cadastrado com sucesso")
        users.append({"Nome": nome,
                      "data_de_nascimento": data_de_nascimento,
                      "cpf": cpf,
                      "endereco": endereco})


def verificar(cpf, users):
    usuarios_existentes = [user for user in users if user["CPF"] == cpf]
    return usuarios_existentes[0] if usuarios_existentes else None


def listar_users(users):
    for c in users:
        print(c)


def criar_conta(agencia, numero, users):
    cpf = input("Insira o cpf: ")
    usuario = verificar(cpf, users)
    if usuario:
        print(f"conta criada com sucesso")
        return {"agencia": agencia, "numero": numero, "usuario": usuario}


def listar_contas(contas):
    for c in contas:
        print(c)


def main():
    MENU = """
    [D] Depositar
    [S] Sacar
    [E] Extrato
    [CU] Cadastrar usuario
    [LU] Listar usuarios
    [CC] Cadastrar conta
    [LC] Listar conta
    [Q] Sair
    """

    LIMITE = 500
    SAQUES_DIARIOS = 3
    AGENCIA = "0001"
    saldo = 0
    transacoes = []
    extrato = ""
    users = []
    contas = []
    numero_de_saques = 0

    while True:
        esc = input(MENU).upper()

        if esc == "D":
            deposito = float(input("Insira o valor do deposito: "))
            saldo, extrato = depositar(saldo, deposito, extrato)

        elif esc == "S":
            saque = float(input("Insira o valor a ser sacado: "))
            saldo, extrato, numero_de_saques = sacar(saldo=saldo,
                                                     saque=saque,
                                                     limite=LIMITE,
                                                     saques=numero_de_saques,
                                                     saques_diarios=SAQUES_DIARIOS,
                                                     extrato=extrato)

        elif esc == "E":
            exibir_extrato(saldo, extrato)

        elif esc == "CU":
            criar_user(users)

        elif esc == "LU":
            listar_users(users)

        elif esc == "CC":
            numero = len(contas) + 1
            conta = criar_conta(AGENCIA, numero, users)

            if conta:
                contas.append(conta)

        elif esc == "LC":
            listar_contas(contas)

        elif esc == "Q":
            break
        else:
            print(
                "Operação invalida, por favor selecione novamente a operação desejada")


main()
