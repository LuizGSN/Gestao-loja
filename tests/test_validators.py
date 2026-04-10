"""
Testes unitários para o módulo validators.
"""

import pytest
from unittest.mock import patch
from datetime import datetime

from validators import (
    validar_inteiro_positivo,
    validar_inteiro_nao_negativo,
    validar_float_positivo,
    validar_preco,
    validar_string_nao_vazia,
    validar_data,
    validar_sim_nao
)


class TestValidarInteiroPositivo:
    def test_valor_valido(self):
        with patch("builtins.input", return_value="10"):
            assert validar_inteiro_positivo("Digite: ") == 10

    def test_valor_invalido_depois_valido(self):
        with patch("builtins.input", side_effect=["abc", "5"]):
            assert validar_inteiro_positivo("Digite: ") == 5

    def test_valor_negativo_depois_valido(self):
        with patch("builtins.input", side_effect=["-3", "7"]):
            assert validar_inteiro_positivo("Digite: ") == 7

    def test_zero_rejeitado(self):
        with patch("builtins.input", side_effect=["0", "1"]):
            assert validar_inteiro_positivo("Digite: ") == 1

    def test_string_vazia_rejeitada(self):
        with patch("builtins.input", side_effect=["", "42"]):
            assert validar_inteiro_positivo("Digite: ") == 42


class TestValidarInteiroNaoNegativo:
    def test_zero_aceito(self):
        with patch("builtins.input", return_value="0"):
            assert validar_inteiro_nao_negativo("Digite: ") == 0

    def test_valor_positivo(self):
        with patch("builtins.input", return_value="15"):
            assert validar_inteiro_nao_negativo("Digite: ") == 15

    def test_negativo_depois_valido(self):
        with patch("builtins.input", side_effect=["-1", "3"]):
            assert validar_inteiro_nao_negativo("Digite: ") == 3


class TestValidarFloatPositivo:
    def test_valor_valido(self):
        with patch("builtins.input", return_value="3.14"):
            assert validar_float_positivo("Digite: ") == 3.14

    def test_valor_com_virgula(self):
        with patch("builtins.input", return_value="2,5"):
            assert validar_float_positivo("Digite: ") == 2.5

    def test_valor_invalido_depois_valido(self):
        with patch("builtins.input", side_effect=["xyz", "1.5"]):
            assert validar_float_positivo("Digite: ") == 1.5

    def test_negativo_rejeitado(self):
        with patch("builtins.input", side_effect=["-1.0", "2.0"]):
            assert validar_float_positivo("Digite: ") == 2.0


class TestValidarPreco:
    def test_preco_valido(self):
        with patch("builtins.input", return_value="29.90"):
            assert validar_preco("Digite: ") == 29.90

    def test_preco_com_virgula(self):
        with patch("builtins.input", return_value="19,99"):
            assert validar_preco("Digite: ") == 19.99

    def test_preco_zero_permitido(self):
        with patch("builtins.input", return_value="0"):
            assert validar_preco("Digite: ") == 0.0

    def test_preco_negativo_rejeitado(self):
        with patch("builtins.input", side_effect=["-50", "10.00"]):
            assert validar_preco("Digite: ") == 10.00

    def test_preco_muito_alto_rejeitado(self):
        with patch("builtins.input", side_effect=["9999999999", "100.00"]):
            assert validar_preco("Digite: ") == 100.00

    def test_preco_texto_invalido(self):
        with patch("builtins.input", side_effect=["abc", "5.50"]):
            assert validar_preco("Digite: ") == 5.50

    def test_arredonda_para_2_casas(self):
        with patch("builtins.input", return_value="10.555"):
            resultado = validar_preco("Digite: ")
            assert abs(resultado - 10.55) < 0.01 or abs(resultado - 10.56) < 0.01


class TestValidarStringNaoVazia:
    def test_string_valida(self):
        with patch("builtins.input", return_value="Produto Teste"):
            assert validar_string_nao_vazia("Digite: ") == "Produto Teste"

    def test_string_vazia_depois_valida(self):
        with patch("builtins.input", side_effect=["", "Notebook"]):
            assert validar_string_nao_vazia("Digite: ") == "Notebook"

    def test_string_com_whitespace(self):
        with patch("builtins.input", return_value="  Produto  "):
            assert validar_string_nao_vazia("Digite: ") == "Produto"

    def test_string_muito_longa(self):
        texto_longo = "A" * 151
        with patch("builtins.input", side_effect=[texto_longo, "Válido"]):
            assert validar_string_nao_vazia("Digite: ") == "Válido"

    def test_string_limite_150_caracteres(self):
        texto_valido = "A" * 150
        with patch("builtins.input", return_value=texto_valido):
            assert validar_string_nao_vazia("Digite: ") == texto_valido


class TestValidarData:
    def test_data_formato_ddmmaaaa(self):
        with patch("builtins.input", return_value="25/12/2024"):
            assert validar_data("Digite: ") == "2024-12-25"

    def test_data_formato_iso(self):
        with patch("builtins.input", return_value="2024-01-15"):
            assert validar_data("Digite: ") == "2024-01-15"

    def test_data_vazia_retorna_none(self):
        with patch("builtins.input", return_value=""):
            assert validar_data("Digite: ") is None

    def test_data_invalida_depois_valida(self):
        with patch("builtins.input", side_effect=["32/13/2024", "01/01/2024"]):
            assert validar_data("Digite: ") == "2024-01-01"

    def test_data_texto_invalido(self):
        with patch("builtins.input", side_effect=["ontem", "10/10/2024"]):
            assert validar_data("Digite: ") == "2024-10-10"


class TestValidarSimNao:
    def test_resposta_sim(self):
        with patch("builtins.input", return_value="S"):
            assert validar_sim_nao("Digite: ") == "S"

    def test_resposta_sim_extenso(self):
        with patch("builtins.input", return_value="SIM"):
            assert validar_sim_nao("Digite: ") == "S"

    def test_resposta_nao(self):
        with patch("builtins.input", return_value="N"):
            assert validar_sim_nao("Digite: ") == "N"

    def test_resposta_nao_extenso(self):
        with patch("builtins.input", return_value="NAO"):
            assert validar_sim_nao("Digite: ") == "N"

    def test_resposta_nao_com_acento(self):
        with patch("builtins.input", return_value="NÃO"):
            assert validar_sim_nao("Digite: ") == "N"

    def test_resposta_invalida_depois_valida(self):
        with patch("builtins.input", side_effect=["X", "S"]):
            assert validar_sim_nao("Digite: ") == "S"
