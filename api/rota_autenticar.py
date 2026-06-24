from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.banco import pegar_conexao_SQL, salvar_cadastro_banco
from utils.banco import usuario_existe_retorna_senha, verifica_cargo_usuario
from utils.ultils import tratar_nome_usuario, tratar_email_usuario, criptografar_senha
from utils.ultils import verificar_senha, cria_token_acesso


#Rota para autenticacao
router = APIRouter(prefix="/autenticacao", tags=["Autenticacao"])

class Cadastro(BaseModel):
    usuario: str
    email: str
    senha: str
    cargo: str

class Login(BaseModel):
    usuario: str
    email: str
    senha: str

# Rota de cadastro (novo_usuario)
@router.post("/cadastrar")
def cadastrar_usuario(dados: Cadastro, db = Depends(pegar_conexao_SQL)):
    nome_tratado = tratar_nome_usuario(dados.usuario)
    email_tratado = tratar_email_usuario(dados.email)
    senha_cripto = criptografar_senha(nome_tratado, dados.senha)
    cargo_tratado = tratar_nome_usuario(dados.cargo)

    salvar_cadastro_banco(db, nome_tratado, email_tratado, senha_cripto, cargo_tratado)

    return {"status": "sucesso"}

@router.post("/login")
def login(dados: Login, db = Depends(pegar_conexao_SQL)):
    nome_tratado = tratar_nome_usuario(dados.usuario)
    email_tratado = tratar_email_usuario(dados.email)
    senha_cripto = usuario_existe_retorna_senha(db, nome_tratado, email_tratado)

    if senha_cripto is None:
        raise HTTPException(status_code=401, detail="Usuário ou e-mail incorretos")

    usuario_logado = verificar_senha(nome_tratado, senha_cripto, dados.senha)

    if not usuario_logado:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    usuario_admin = verifica_cargo_usuario(db, nome_tratado, email_tratado)

    dados_para_o_token = {
        "sub": nome_tratado,
        "email": email_tratado,
        "cargo": usuario_admin
    }

    token_jwt = cria_token_acesso(dados_usuario=dados_para_o_token)

    return {
        "status": "sucesso",
        "access_token": token_jwt,
        "token_type": "bearer"
    }

    


    
