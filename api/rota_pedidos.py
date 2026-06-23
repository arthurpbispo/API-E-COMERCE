from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.banco import pegar_conexao_SQL, adicionar_pedido_tabela_pedidos
from utils.ultils import verificar_usuario_logado

router = APIRouter(prefix="/pedidos", tags=['Pedidos'])

class RegistroProduto(BaseModel):
    nome_usuario: str
    email: str
    nome_produto: str
    status_pedido: str

@router.post("/registrarpedido")
def registrar_produto(
    dados: RegistroProduto,
    db = Depends(pegar_conexao_SQL),
    usuario_atual: dict = Depends(verificar_usuario_logado)
):
    adcionou_banco = adicionar_pedido_tabela_pedidos(db, dados.nome_produto, dados.nome_usuario, dados.email, dados.status_pedido)

    if not adcionou_banco:
        return {"status": "Erro", "mensagem": "Nao foi possivel adicionar pedido ao banco"}
    
    return {"status": "Sucesso", "mensagem": "Pedido registrado"}
