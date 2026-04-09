"""
Módulo de funções utilitárias diversas.
"""

import os
import platform


def limpar_tela():
    """Limpa a tela do terminal de acordo com o sistema operacional."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def formatar_moeda(valor):
    """
    Formata valor float para formato de moeda brasileira.
    
    Args:
        valor: Valor numérico
        
    Returns:
        String formatada como R$ XX,XX
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_data(data_iso):
    """
    Formata data de YYYY-MM-DD para DD/MM/AAAA.
    
    Args:
        data_iso: Data no formato ISO (YYYY-MM-DD)
        
    Returns:
        Data formatada (DD/MM/AAAA) ou data original se inválida
    """
    if not data_iso:
        return "N/A"
    
    try:
        from datetime import datetime
        data = datetime.strptime(str(data_iso), "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return str(data_iso)


def pausar(mensagem="Pressione ENTER para continuar..."):
    """Exibe mensagem e aguarda pressionar ENTER."""
    input(mensagem)


def centralizar_texto(texto, largura=60):
    """Centraliza texto na tela."""
    return texto.center(largura)


def criar_barra(largura=60, caractere="="):
    """Cria barra de separação."""
    return caractere * largura
