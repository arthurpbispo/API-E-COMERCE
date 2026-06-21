import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def iniciar_banco():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def criar_tabelas():
    conexao = iniciar_banco()
    if not conexao:
        print("Não foi possível conectar ao banco para criar as tabelas.")
        return
        
    try:
        cursor = conexao.cursor()
        
        # 1. Tabela de Usuários
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL
        );
        """)
        
        # 2. Tabela de Produtos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(150) UNIQUE NOT NULL,
            descricao TEXT,
            preco DECIMAL(10, 2) NOT NULL,
            estoque INT DEFAULT 0,
            categoria VARCHAR(100)
        );
        """)
        
        # 3. Tabela de Pedidos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            status_pedido VARCHAR(50) NOT NULL,
            data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # 4. Tabela de Itens do Pedido
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pedido_id INT NOT NULL,
            produto_id INT NOT NULL,
            quantidade INT NOT NULL,
            preco_unidade DECIMAL(10, 2) NOT NULL
        );
        """)
        
        conexao.commit()
        print("Todas as tabelas foram verificadas/criadas com sucesso no MySQL!")
        
    except Error as e:
        print(f"Erro ao criar tabelas no MySQL: {e}")
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def salvar_cadastro_banco(conexao, nome_usuario, email_usuario, senha_usuario):
    if not conexao:
        print("Sem conexão com o banco de dados.")
        return False
        
    try:
        cursor = conexao.cursor()

        comando = """
            INSERT INTO usuarios (usuario, email, senha) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(comando, (nome_usuario, email_usuario, senha_usuario))
        conexao.commit()
        print("Usuário cadastrado com sucesso no MySQL!")
        return True
    except Error as e:
        print(f"Erro ao salvar cadastro: {e}")
        return False
    finally:
        cursor.close()

def usuario_existe_retorna_senha(conexao, usuario, email):
    if not conexao:
        print("Sem conexão com o banco de dados.")
        return None
        
    try:
        cursor = conexao.cursor()

        comando = """
            SELECT senha FROM usuarios 
            WHERE usuario = %s AND email = %s
        """
        cursor.execute(comando, (usuario, email))
        resultado = cursor.fetchone()
        
        if resultado is None:
            return None
            
        senha_banco = resultado[0]
        
        if isinstance(senha_banco, bytes):
            senha_banco = senha_banco.decode('utf-8')
            
        return senha_banco
    except Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        cursor.close()