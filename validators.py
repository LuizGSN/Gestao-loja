"""
Módulo de validações de entrada do usuário.
Garante que todos os dados inseridos sejam válidos antes de processar.
"""

from datetime import datetime


def validar_inteiro_positivo(mensagem):
    """
    Valida entrada de número inteiro positivo.
    Repete a pergunta até receber um valor válido.
    """
    while True:
        try:
            valor = input(mensagem).strip()
            numero = int(valor)
            if numero <= 0:
                print("❌ O valor deve ser maior que zero! Tente novamente.")
                continue
            return numero
        except ValueError:
            print("❌ Entrada inválida! Digite um número inteiro válido.")


def validar_inteiro_nao_negativo(mensagem):
    """
    Valida entrada de número inteiro não negativo (zero ou positivo).
    """
    while True:
        try:
            valor = input(mensagem).strip()
            numero = int(valor)
            if numero < 0:
                print("❌ O valor não pode ser negativo! Tente novamente.")
                continue
            return numero
        except ValueError:
            print("❌ Entrada inválida! Digite um número inteiro válido.")


def validar_float_positivo(mensagem):
    """
    Valida entrada de número float positivo.
    """
    while True:
        try:
            valor = input(mensagem).strip().replace(',', '.')
            numero = float(valor)
            if numero <= 0:
                print("❌ O valor deve ser maior que zero! Tente novamente.")
                continue
            return numero
        except ValueError:
            print("❌ Entrada inválida! Digite um número válido.")


def validar_preco(mensagem):
    """
    Valida entrada de preço (float positivo com até 2 casas decimais).
    """
    while True:
        try:
            valor = input(mensagem).strip().replace(',', '.')
            preco = float(valor)
            if preco < 0:
                print("❌ O preço não pode ser negativo! Tente novamente.")
                continue
            if preco > 999999999:
                print("❌ Preço muito alto! Verifique o valor digitado.")
                continue
            return round(preco, 2)
        except ValueError:
            print("❌ Entrada inválida! Digite um preço válido (ex: 29.90).")


def validar_string_nao_vazia(mensagem):
    """
    Valida entrada de string não vazia.
    """
    while True:
        valor = input(mensagem).strip()
        if not valor:
            print("❌ Este campo não pode ser vazio! Tente novamente.")
            continue
        if len(valor) > 150:
            print("❌ Texto muito longo! Máximo de 150 caracteres.")
            continue
        return valor


def validar_data(mensagem):
    """
    Valida entrada de data nos formatos DD/MM/AAAA ou YYYY-MM-DD.
    Se vazio, retorna None (usará data atual).
    Retorna data no formato YYYY-MM-DD para o banco.
    """
    while True:
        valor = input(mensagem).strip()
        
        # Se vazio, retorna None
        if not valor:
            return None
        
        # Tentar formato DD/MM/AAAA
        try:
            data = datetime.strptime(valor, "%d/%m/%Y")
            return data.strftime("%Y-%m-%d")
        except ValueError:
            pass
        
        # Tentar formato YYYY-MM-DD
        try:
            data = datetime.strptime(valor, "%Y-%m-%d")
            return data.strftime("%Y-%m-%d")
        except ValueError:
            pass
        
        # Se nenhum formato funcionou
        print("❌ Data inválida! Use o formato DD/MM/AAAA ou YYYY-MM-DD.")


def validar_sim_nao(mensagem):
    """
    Valida resposta Sim/Não.
    """
    while True:
        valor = input(mensagem).strip().upper()
        if valor in ("S", "SIM"):
            return "S"
        if valor in ("N", "NAO", "NÃO"):
            return "N"
        print("❌ Resposta inválida! Digite S (Sim) ou N (Não).")
