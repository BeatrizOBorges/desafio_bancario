import textwrap

def exibir_menu():
    opcoes = """
    ========== MENU PRINCIPAL ==========
    [1]\tAdicionar saldo
    [2]\tRealizar saque
    [3]\tMostrar extrato
    [4]\tCadastrar nova conta
    [5]\tExibir contas cadastradas
    [6]\tRegistrar novo cliente
    [0]\tEncerrar programa
    => """
    return input(textwrap.dedent(opcoes))


def adicionar_saldo(saldo_atual, valor_adicionado, historico, /):
    if valor_adicionado > 0:
        saldo_atual += valor_adicionado
        historico += f"Depósito:\tR$ {valor_adicionado:.2f}\n"
        print(">>> Depósito concluído com sucesso!")
    else:
        print("!!! Valor inválido. Operação cancelada.")

    return saldo_atual, historico


def realizar_saque(*, saldo_atual, valor_retirado, historico, limite_valor, total_saques, max_saques):
    falta_saldo = valor_retirado > saldo_atual
    ultrapassou_limite = valor_retirado > limite_valor
    excedeu_quantidade = total_saques >= max_saques

    if falta_saldo:
        print("!!! Saldo insuficiente.")

    elif ultrapassou_limite:
        print("!!! O valor do saque excede o limite permitido.")

    elif excedeu_quantidade:
        print("!!! Limite de saques atingido.")

    elif valor_retirado > 0:
        saldo_atual -= valor_retirado
        historico += f"Saque:\t\tR$ {valor_retirado:.2f}\n"
        total_saques += 1
        print(">>> Saque realizado com sucesso.")
    else:
        print("!!! Valor inválido para saque.")

    return saldo_atual, historico


def mostrar_extrato(saldo_atual, /, *, historico):
    print("\n=========== EXTRATO ==========")
    print("Sem movimentações registradas." if not historico else historico)
    print(f"\nSaldo atual:\tR$ {saldo_atual:.2f}")
    print("=================================")


def registrar_cliente(lista_clientes):
    cpf_input = input("CPF (apenas números): ")
    if encontrar_cliente(cpf_input, lista_clientes):
        print("!!! CPF já cadastrado.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, número - bairro - cidade/UF): ")

    lista_clientes.append({
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf_input,
        "endereco": endereco
    })

    print(">>> Cliente registrado com sucesso!")


def encontrar_cliente(cpf, lista_clientes):
    for cliente in lista_clientes:
        if cliente["cpf"] == cpf:
            return cliente
    return None


def cadastrar_conta_padrao(codigo_agencia, numero_conta, clientes):
    cpf_cliente = input("CPF do titular: ")
    cliente = encontrar_cliente(cpf_cliente, clientes)

    if cliente:
        print(">>> Conta cadastrada com sucesso!")
        return {"agencia": codigo_agencia, "conta": numero_conta, "cliente": cliente}
    
    print("!!! Cliente não localizado. Encerrando criação de conta.")


def exibir_contas(contas_registradas):
    for conta in contas_registradas:
        dados = f"""
            Agência:\t{conta['agencia']}
            Conta Nº:\t{conta['conta']}
            Titular:\t{conta['cliente']['nome']}
        """
        print("=" * 80)
        print(textwrap.dedent(dados))


def iniciar_sistema():
    LIMITE_MAX_SAQUES = 3
    NUMERO_AGENCIA = "0001"

    saldo = 0
    limite_saque = 500
    historico_movimentacao = ""
    total_saques_realizados = 0
    clientes = []
    contas = []

    while True:
        escolha = exibir_menu()

        if escolha == "1":
            valor = float(input("Valor do depósito: "))
            saldo, historico_movimentacao = adicionar_saldo(saldo, valor, historico_movimentacao)

        elif escolha == "2":
            valor = float(input("Valor do saque: "))
            saldo, historico_movimentacao = realizar_saque(
                saldo_atual=saldo,
                valor_retirado=valor,
                historico=historico_movimentacao,
                limite_valor=limite_saque,
                total_saques=total_saques_realizados,
                max_saques=LIMITE_MAX_SAQUES
            )

        elif escolha == "3":
            mostrar_extrato(saldo, historico=historico_movimentacao)

        elif escolha == "4":
            numero_nova_conta = len(contas) + 1
            nova_conta = cadastrar_conta_padrao(NUMERO_AGENCIA, numero_nova_conta, clientes)
            if nova_conta:
                contas.append(nova_conta)

        elif escolha == "5":
            exibir_contas(contas)

        elif escolha == "6":
            registrar_cliente(clientes)

        elif escolha == "0":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")


iniciar_sistema()