#quando for escever no banco a biblioteca utilizada foi a https://pypi.org/project/PyMySQL/
import pymysql.cursors
import pymysql


class Conexao:
    def __init__(self, host, usuario, senha, db):
        self.conexao = pymysql.connect(
            host=host,
            user=usuario,
            password=senha,
            db=db,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __enter__(self):
        return self.conexao

    def __exit__(self, exc_type, exc_value, traceback):
        self.conexao.close()


class Modelo:
    def __init__(self, conexao):
        self.conexao = conexao

    def criar_usuario(self, nome, email):
        with self.conexao.cursor() as cursor:
            sql = "INSERT INTO usuarios (nome, email) VALUES (%s, %s)"
            cursor.execute(sql, (nome, email))
        self.conexao.commit()

    def buscar_usuario(self, id):
        with self.conexao.cursor() as cursor:
            sql = "SELECT * FROM usuarios WHERE id = %s"
            cursor.execute(sql, id)
            usuario = cursor.fetchone()
        return usuario

    def atualizar_usuario(self, id, nome, email):
        with self.conexao.cursor() as cursor:
            sql = "UPDATE usuarios SET nome = %s, email = %s WHERE id = %s"
            cursor.execute(sql, (nome, email, id))
        self.conexao.commit()

    def deletar_usuario(self, id):
        with self.conexao.cursor() as cursor:
            sql = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(sql, id)
        self.conexao.commit()


class Visualizacao:
    def mostrar_usuario(self, usuario):
        if usuario:
            print(f"Usuário encontrado: {usuario['id']}: {usuario['nome']} ({usuario['email']})")
        else:
            print("Usuário não encontrado.")

    def mostrar_usuarios(self, usuarios):
        print("Lista de usuários:")
        for usuario in usuarios:
            print(f"{usuario['id']}: {usuario['nome']} ({usuario['email']})")


class Controlador:
    def __init__(self, modelo, visualizacao):
        self.modelo = modelo
        self.visualizacao = visualizacao

    def criar_usuario(self, nome, email):
        self.modelo.criar_usuario(nome, email)
        print("Usuário criado com sucesso.")

    def buscar_usuario(self, id):
        usuario = self.modelo.buscar_usuario(id)
        self.visualizacao.mostrar_usuario(usuario)

    def atualizar_usuario(self, id, nome, email):
        self.modelo.atualizar_usuario(id, nome, email)
        print("Usuário atualizado com sucesso.")

    def deletar_usuario(self, id):
        self.modelo.deletar_usuario(id)
        print("Usuário deletado com sucesso.")

    def listar_usuarios(self):
        with self.modelo.conexao as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios")
                usuarios = cursor.fetchall()
        self.visualizacao.mostrar_usuarios(usuarios)


# Categorias

INSERT INTO categorias (nome) VALUES (%s);

SELECT * FROM categorias;

UPDATE categorias SET nome = 'Livros' WHERE id = 1;

DELETE FROM categorias WHERE id = 1;

# Empresas

INSERT INTO empresas (nome) VALUES ('Amazon');

SELECT * FROM empresas;

SELECT * FROM empresas WHERE id = 1;

UPDATE empresas SET nome = 'Magazine Luiza' WHERE id = 1;

DELETE FROM empresas WHERE id = 1;

# Produtos

INSERT INTO produtos (nome, url, image_url, frete_prime, id_empresa, id_categoria) VALUES ('Smartphone Samsung Galaxy S21', 'https://www.exemplo.com/produtos/samsung-galaxy-s21', 'https://www.exemplo.com/imagens/samsung-galaxy-s21.jpg', true, 1, 1);

SELECT * FROM produtos;

SELECT * FROM produtos WHERE id = 1;

DELETE FROM produtos WHERE id = 1;

# Precos

INSERT INTO precos (id_produto, data, preco) VALUES (1, '2021-08-30', 1999.99);

SELECT * FROM precos;

SELECT * FROM precos WHERE id = 1;

UPDATE precos SET preco = 2099.9 WHERE id = 1;

DELETE FROM precos WHERE id = 1;
