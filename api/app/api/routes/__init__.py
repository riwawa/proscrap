from fastapi import APIRouter
from app.api.routes import movimentacoes, processos, sincronizar

api_router = APIRouter()
api_router.include_router(processos.router)
api_router.include_router(movimentacoes.router)
api_router.include_router(sincronizar.router)