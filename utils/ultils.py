import os
import json
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

security = HTTPBearer()


def tratar_nome_usuario(nome):
    #Retira espacos
    nome_sem_espacos = nome.strip()

    if len(nome_sem_espacos) < 2 or len(nome_sem_espacos) > 30:
        return None
    
    else:
        return nome_sem_espacos

def tratar_email_usuario(email):
    email_sem_espacos = email.strip().lower()

    return email_sem_espacos

def criptografar_senha(usuario, senha):
    chave = Fernet.generate_key()
    fernet = Fernet(chave)

    senha_str = str(senha)

    senha_byte = senha_str.encode("utf-8")

    senha_cripto = fernet.encrypt(senha_byte)

    chave_string = chave.decode("utf-8")

    cadastro = {
        'usuario': usuario,
        'chave_senha': chave_string
    }

    caminho_json = 'utils/chaves.json'

    if os.path.exists(caminho_json) and os.path.getsize(caminho_json) > 0:
        with open(caminho_json, "r", encoding='utf-8') as arquivo:
            lista_usuarios = json.load(arquivo)
    else:
        lista_usuarios = []
    
    lista_usuarios.append(cadastro)

    with open(caminho_json, "w", encoding='utf-8') as arquivo:
        json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)
    
    return senha_cripto

def verificar_senha(usuario, senha_banco, senha_digitada):
    caminho_json = 'utils/chaves.json'
    
    if os.path.exists(caminho_json) and os.path.getsize(caminho_json) > 0:
        with open(caminho_json, "r", encoding='utf-8') as arquivo:
            lista_cadastros = json.load(arquivo)
    else:
        return False
        
    chave_senha_usuario = None
    for cadastro in lista_cadastros:
        if cadastro.get("usuario") == usuario:
            chave_senha_usuario = cadastro.get("chave_senha")
            break
            
    if not chave_senha_usuario:
        return False
        
    if isinstance(chave_senha_usuario, str):
        chave_senha_byte = chave_senha_usuario.encode()
        
    if isinstance(senha_banco, str):
        senha_banco = senha_banco.encode()
        
    try:
        fernet = Fernet(chave_senha_byte)
        senha_descripto_byte = fernet.decrypt(senha_banco)
        senha_descripto = senha_descripto_byte.decode("utf-8")
        
        if senha_descripto == senha_digitada:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"ERRO NA CRIPTOGRAFIA DO LOGIN: {e}")
        return False

def cria_token_acesso(dados_usuario: dict, tempo_expiracao: int = 60):
    payload = dados_usuario.copy()

    expiracao = datetime.now(timezone.utc) + timedelta(minutes=tempo_expiracao)

    payload.update({"exp": expiracao})

    token_gerado = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_gerado


def verificar_usuario_logado(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="O token expirou. Faça login novamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido ou corrompido.")