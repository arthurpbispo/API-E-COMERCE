# from cryptography.fernet import Fernet
# import os
# import json

# senha = '12345'

# def criptografar_senha(senha):
#     chave = Fernet.generate_key()
#     fernet = Fernet(chave)

#     senha_byte = senha.encode("utf-8")

#     senha_cripto = fernet.encrypt(senha_byte).decode("utf-8")

#     chave_string = chave.decode("utf-8")

#     cadastro = {
#         'usuario': "admin",
#         'chave_senha': chave_string
#     }

#     caminho_json = 'utils/chaves.json'

#     if os.path.exists(caminho_json) and os.path.getsize(caminho_json) > 0:
#         with open(caminho_json, "r", encoding='utf-8') as arquivo:
#             lista_usuarios = json.load(arquivo)
#     else:
#         lista_usuarios = []
    
#     lista_usuarios.append(cadastro)

#     with open(caminho_json, "w", encoding='utf-8') as arquivo:
#         json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)

    
# criptografar_senha(senha)
