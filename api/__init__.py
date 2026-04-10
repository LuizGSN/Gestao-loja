"""
Pacote da API - schemas e rotas.
"""

from api.routes.produtos import router as produtos_router
from api.routes.vendas import router as vendas_router


def configure_api_routes(app):
    """
    Configura todas as rotas da API no app FastAPI.
    
    Args:
        app: Instância do FastAPI
    """
    app.include_router(produtos_router, prefix="/api/v1")
    app.include_router(vendas_router, prefix="/api/v1")
