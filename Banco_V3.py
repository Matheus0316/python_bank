from abc import ABC, abstractmethod
from datetime import datetime

class Cliente():
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def lista_contas(self):
        for conta in self.contas:
            print(conta)

    def realizar_transacao(self, transacao, conta):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    def __str__(self):
        return f"{self.__class__.__name__}: {self._nome}"



class Conta():
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        excede_saldo = valor > self._saldo
        if excede_saldo:
            print("O valor informado excede o saldo atual")
            return False
        elif valor > 0:
            self._saldo -= valor
            return True

        else:
            print("Informe valido")

        return False

    def depositar(self, valor):
        self._saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limites_saques = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limites_saques

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self._historico._transacoes if transacao["Tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_limite_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("O valor excerde o limite")
            return False

        elif  excedeu_limite_saques:
            print("O limite de saques foi atingido")
            return False

        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""Numero: {self._numero}
Agencia: {self._agencia}
Saldo: R${self._saldo:.2f}
        """


class Historico():
    def __init__(self,):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "Data": datetime.now().strftime("%D-%M-%Y %H:%M:%S")
            }
        )


class Transacao(ABC):
    @abstractmethod
    def registrar():
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)



class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


def verificar(cpf, clientes):
    clientes_existentes = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_existentes[0] if clientes_existentes else None


def criar_cliente(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente_existe = verificar(cpf, clientes)
    if not cliente_existe:
        nome = input("Informe o nome do cliente: ")
        data_nascimento = input("Informe a data de nascimento do cliente: ")
        endereco = input("Informe o endereço do cliente: ")

        clientes.append(PessoaFisica(cpf, nome, data_nascimento, endereco))

    else:
        print("Esse cpf já está vinculado")

def listar_clientes(clientes):
    if not clientes:
        print("Não existem clientes no momento")
    else:
        for c in clientes:
            print(c)


def criar_conta(numero, clientes):
    cpf = input("Insira o cpf: ")
    cliente = verificar(cpf, clientes)
    if cliente:
        conta = ContaCorrente(numero, cliente)
        cliente.adicionar_conta(conta)
        print(f"conta criada com sucesso")
        return conta
    else:
        print("O cpf informado não está vinculado")
        return


def listar_contas(contas):
    if not contas:
        print("Não existem contas no momento")
    else:
        for c in contas:
            print(c)


def conta_cliente(cpf, clientes):
    cliente = verificar(cpf, clientes)

    if not cliente.contas[0]:
        print("O cliente não possui conta")
        return

    elif len(cliente.contas) > 1:
        conta = int(input("Informe o numero da conta: "))
        return cliente.contas[conta-1]

    else:
        return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = verificar(cpf, clientes)

    if not cliente:
        print("Não existe um cliente com esse cpf")

    else:
        valor = float(input("Informe o valor do deposito: "))

        if not cliente.contas[0]:
            print("O cliente não possui conta")

        elif len(cliente.contas) > 1:
            conta = int(input("Informe a conta que receberá o deposito: "))
            cliente.realizar_transacao(Deposito(valor), cliente.contas[conta-1])
        else:
            cliente.realizar_transacao(Deposito(valor), cliente.contas[0])

def sacar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = verificar(cpf, clientes)

    if not cliente:
        print("Não existe um cliente com esse cpf")

    else:
        valor = float(input("Informe o valor do saque: "))

        if not cliente.contas[0]:
            print("O cliente não possui conta")

        elif len(cliente.contas) > 1:
            conta = int(input("Informe o numero da conta que receberá o saque: "))
            cliente.realizar_transacao(Saque(valor), cliente.contas[conta-1])
        else:
            cliente.realizar_transacao(Saque(valor), cliente.contas[0])


def extrato(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = verificar(cpf, clientes)

    if not cliente:
        print("Não existe um cliente com esse cpf")
        return
    else:
        conta = conta_cliente(cpf, clientes)

        if not conta:
            return

        print("\n<==========Extrato==========>")

        transacoes = conta.historico.transacoes

        extrato = ""

        if not transacoes:
            extrato = "Não foram feitas movimentações"

        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['Tipo']} no valor de: R${transacao['Valor']:.2f} em {transacao['Data']}"

        print(extrato)
        print(f"Saldo: R${conta.saldo:.2f}")


def main():
    MENU = """
    [D] Depositar
    [S] Sacar
    [E] Extrato
    [CC] Cadastrar cliente
    [LC] Listar clientes
    [NC] Nova conta
    [EC] Exibir contas
    [Q] Sair
    """
    clientes = []
    contas = []

    while True:
        esc = input(MENU).upper()

        if esc == "D":
           depositar(clientes)

        elif esc == "S":
            sacar(clientes)

        elif esc == "E":
            extrato(clientes)

        elif esc == "CC":
            criar_cliente(clientes)

        elif esc == "LC":
            listar_clientes(clientes)

        elif esc == "NC":
            numero = len(contas) + 1
            conta = criar_conta(numero, clientes)

            if conta:
                contas.append(conta)

        elif esc == "EC":
            listar_contas(contas)

        elif esc == "Q":
            break
        else:
            print(
                "Operação invalida, por favor selecione novamente a operação desejada")


main()
