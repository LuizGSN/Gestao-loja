"""
Testes unitários para o módulo utils.
"""

import pytest
from unittest.mock import patch
from utils import formatar_moeda, formatar_data, centralizar_texto, criar_barra


class TestFormatarMoeda:
    def test_valor_simples(self):
        assert formatar_moeda(29.90) == "R$ 29.90"

    def test_valor_com_milhares(self):
        assert formatar_moeda(4500.00) == "R$ 4.500,00"

    def test_valor_zero(self):
        assert formatar_moeda(0) == "R$ 0.00"

    def test_valor_grande(self):
        assert formatar_moeda(1000000.50) == "R$ 1.000.000,50"

    def test_valor_negativo(self):
        assert formatar_moeda(-50.00) == "R$ -50.00"


class TestFormatarData:
    def test_data_iso_valida(self):
        assert formatar_data("2024-12-25") == "25/12/2024"

    def test_data_vazia(self):
        assert formatar_data("") == "N/A"

    def test_data_none(self):
        assert formatar_data(None) == "N/A"

    def test_data_formato_invalido(self):
        assert formatar_data("25/12/2024") == "25/12/2024"


class TestCentralizarTexto:
    def test_centralizar_padrao(self):
        resultado = centralizar_texto("OLÁ")
        assert resultado == "                           OLÁ                           "

    def test_centralizar_largura_customizada(self):
        resultado = centralizar_texto("X", largura=10)
        assert len(resultado) == 10

    def test_centralizar_texto_longo(self):
        resultado = centralizar_texto("Texto muito longo que ultrapassa a largura")
        assert "Texto muito longo que ultrapassa a largura" in resultado


class TestCriarBarra:
    def test_barra_padrao(self):
        assert criar_barra() == "=" * 60

    def test_barra_largura_customizada(self):
        assert criar_barra(40) == "=" * 40

    def test_barra_caractere_customizado(self):
        assert criar_barra(10, "-") == "-" * 10

    def test_barra_vazia(self):
        assert criar_barra(0) == ""
