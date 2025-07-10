menu = """

[a] Depositar
[b] Sacar
[c] Extrato
[d] Sair

=> """

saldo = 4650
limite = 2000
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "a":
        valor = float(input("Qual o valor para depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Depósito não efetuado! O valor informado é inválido.")

    elif opcao == "b":
        valor = float(input("Qual o valor para saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Saque não realizado! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Saque não realizado! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Saque não realizado! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Saque não realizado! O valor informado é inválido.")

    elif opcao == "c":
        print("\n*********** EXTRATO ************")
        print("Sem movimentações no dia." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("*********************************")

    elif opcao == "d":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")