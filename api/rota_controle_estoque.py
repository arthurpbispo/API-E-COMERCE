from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.banco import pegar_conexao_SQL, atulizar_tabela_produto
from utils.ultils import verificar_usuario_logado

router = APIRouter(prefix="/estoque", tags=["Estoque"])

class ProdutoCadastro(BaseModel):
    nome: str
    descricao: str
    preco: float
    estoque: int
    categoria: str

@router.post("/adicionar")
def adicionar_produto(
    dados: ProdutoCadastro,
    db = Depends(pegar_conexao_SQL),
    usuario_atual: dict = Depends(verificar_usuario_logado)
):
    
    print(usuario_atual)
    
    if not usuario_atual.get("cargo"):
        raise HTTPException (
            status_code=403,
            detail="Acesso negado. Esta operação é permitida apenas para administradores."
        )





    atulizar_tabela_produto(
        db,  
        dados.nome.strip(),
        dados.descricao.strip(),
        dados.preco,
        dados.estoque,
        dados.categoria.strip()
    )
    
    return {"status": "sucesso", "mensagem": "Produto adicionado com sucesso"}