from abc import ABC, abstractmethod
from datetime import datetime


class Usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas_vinculadas = []

    def executar_movimentacao(self, conta, operacao):
        operacao.processar(conta)

    def vincular_conta(self, conta):
        self.contas_vinculadas.append(conta)


class Pessoa(Usuario):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = nascimento
        self.cpf = cpf


class ContaBancaria:
    def __init__(self, numero, titular):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._titular = titular
        self._registro = RegistroTransacoes()

    @classmethod
    def criar_conta(cls, titular, numero):
        return cls(numero, titular)

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
    def titular(self):
        return self._titular

    @property
    def registro(self):
        return self._registro

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para saque. @@@")
            return False

        if valor > self._saldo:
            print("\n@@@ Saldo insuficiente para saque. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque efetuado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor de depósito inválido. @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito efetuado com sucesso! ===")
        return True


class ContaComum(ContaBancaria):
    def __init__(self, numero, titular, limite=500, max_saques=3):
        super().__init__(numero, titular)
        self.limite_valor = limite
        self.saques_disponiveis = max_saques

    def sacar(self, valor):
        saques_efetuados = len([
            op for op in self.registro.historico
            if op["tipo"] == "Retirada"
        ])

        if valor > self.limite_valor:
            print("\n@@@ Limite máximo de valor para saque excedido. @@@")
            return False

        if saques_efetuados >= self.saques_disponiveis:
            print("\n@@@ Número máximo de saques atingido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""
        Agência:   {self.agencia}
        Conta Nº:  {self.numero}
        Cliente:   {self.titular.nome}
        """


class RegistroTransacoes:
    def __init__(self):
        self._eventos = []

    @property
    def historico(self):
        return self._eventos

    def incluir(self, operacao):
        self._eventos.append({
            "tipo": operacao.__class__.__name__,
            "valor": operacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


class Operacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def processar(self, conta):
        pass


class Retirada(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def processar(self, conta):
        if conta.sacar(self.valor):
            conta.registro.incluir(self)


class Inclusao(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def processar(self, conta):
        if conta.depositar(self.valor):
            conta.registro.incluir(self)