"""
Dependências compartilhadas para a API FastAPI.
Evita duplicação de código entre os routers.
"""

from fastapi import Request
from datetime import date, datetime
from database import DatabaseManager


def get_db(request: Request) -> DatabaseManager:
    """Retorna instância do DatabaseManager a partir do app state."""
    return request.app.state.db


def parse_data_venda(valor) -> date:
    """
    Converte valor de data_venda para objeto date.
    Lida com objetos date, datetime, string e None.
    """
    if isinstance(valor, date) and not isinstance(valor, datetime):
        return valor
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return datetime.now().date()
