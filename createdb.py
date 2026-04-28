import mysql.connector
from mysql.connector import Error
from configdb import DB_CONFIG

def create_database():
    config_without_db = DB_CONFIG.copy()
    config_without_db.pop('database')
    try:
        conn = mysql.connector.connect(**config_without_db)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Banco de dados '{DB_CONFIG['database']}' criado/verificado!")
        return conn
    except Error as e:
        print(f"Erro ao criar banco: {e}")
        return None

def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS categorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL UNIQUE,
            slug VARCHAR(50) NOT NULL UNIQUE,
            descricao TEXT,
            cor VARCHAR(7) DEFAULT '#92400e',
            ordem INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS conteudos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            categoria_id INT NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            descricao TEXT NOT NULL,
            imagem_url TEXT,
            destaque BOOLEAN DEFAULT FALSE,
            ordem INT DEFAULT 0,
            ativo BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
            INDEX idx_categoria (categoria_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS favoritos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            conteudo_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE,
            UNIQUE KEY unique_favorite (usuario_id, conteudo_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
    ]
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        for sql in tables:
            cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabelas criadas!")
    except Error as e:
        print(f"Erro: {e}")

def insert_initial_data():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        categorias = [
            ('Historia', 'historia', 'Conteudo historico do RN', '#662c09', 1),
            ('Turismo', 'turismo', 'Pontos turisticos do RN', '#92400e', 2),
            ('Cultura', 'cultura', 'Cultura potiguar', '#b98260', 3),
            ('Gastronomia', 'gastronomia', 'Restaurantes e culinaria', '#d4a574', 4)
        ]
        cursor.executemany("INSERT IGNORE INTO categorias (nome, slug, descricao, cor, ordem) VALUES (%s,%s,%s,%s,%s)", categorias)
        cursor.execute("SELECT id, nome FROM categorias")
        cat_ids = {row[1]: row[0] for row in cursor.fetchall()}
        historias = [
            (cat_ids['Historia'], 'Velha Barra de Santana', 'A antiga comunidade de Barra de Santana, localizada em Jucurutu, tornou-se um simbolo de transformacao.', 'https://images.unsplash.com/photo-1601582580200-3c8b4aa3ac32', False, 1),
            (cat_ids['Historia'], 'Cruzeiro das Almas', 'O Cruzeiro das Almas e um importante ponto historico e de devocao popular na cidade de Cruzeta.', 'https://images.unsplash.com/photo-1491553895911-0055eca6402d', False, 2),
            (cat_ids['Historia'], 'Casa Forte do Cuo', 'A Casa Forte do Cuo e considerada a construcao colonial mais antiga da cidade de Caico.', 'https://images.unsplash.com/photo-1530038466036-8792b1a5d7e6', False, 3),
            (cat_ids['Historia'], 'Castelo do Engady', 'O Castelo de Engady e uma edificacao localizada nos arredores da cidade de Caico.', 'https://images.unsplash.com/photo-1501785888041-af3ef285b470', False, 4),
            (cat_ids['Historia'], 'Museu do Serido', 'O Museu do Serido, vinculado a Universidade Federal do Rio Grande do Norte, e uma importante instituicao historica.', 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee', False, 5),
            (cat_ids['Historia'], 'Igreja Matriz de Nossa Senhora dos Remedios', 'A Igreja Matriz de Nossa Senhora dos Remedios e o principal templo catolico de Cruzeta.', 'https://images.unsplash.com/photo-1491553895911-0055eca6402d', False, 6)
        ]
        cursor.executemany("INSERT INTO conteudos (categoria_id, titulo, descricao, imagem_url, destaque, ordem) VALUES (%s,%s,%s,%s,%s,%s)", historias)
        turismos = [
            (cat_ids['Turismo'], 'Acude Gargalheiras', 'Ponto turistico do Serido com vista deslumbrante.', 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee', True, 1),
            (cat_ids['Turismo'], 'Serra de Santana', 'Vista incrivel da regiao com trilhas.', 'https://images.unsplash.com/photo-1501785888041-af3ef285b470', True, 2)
        ]
        cursor.executemany("INSERT INTO conteudos (categoria_id, titulo, descricao, imagem_url, destaque, ordem) VALUES (%s,%s,%s,%s,%s,%s)", turismos)
        culturas = [
            (cat_ids['Cultura'], 'Festa da Colheita', 'Tradicao agricola de Cruzeta.', 'https://images.unsplash.com/photo-1491553895911-0055eca6402d', False, 1),
            (cat_ids['Cultura'], 'Filarmonica de Cruzeta', 'Orquestra tradicional da regiao.', 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee', False, 2),
            (cat_ids['Cultura'], 'Casa da Cultura de Caico', 'Centro cultural de Caico.', 'https://images.unsplash.com/photo-1501785888041-af3ef285b470', False, 3),
            (cat_ids['Cultura'], 'Museu do Serido', 'Instituicao historica e cultural.', 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee', False, 4),
            (cat_ids['Cultura'], 'Centro de Artesanato de Jucurutu', 'Arte local e trabalhos manuais.', 'https://images.unsplash.com/photo-1491553895911-0055eca6402d', False, 5),
            (cat_ids['Cultura'], 'Casa de Pedra', 'Formacao geologica natural.', 'https://images.unsplash.com/photo-1501785888041-af3ef285b470', False, 6)
        ]
        cursor.executemany("INSERT INTO conteudos (categoria_id, titulo, descricao, imagem_url, destaque, ordem) VALUES (%s,%s,%s,%s,%s,%s)", culturas)
        gastronomias = [
            (cat_ids['Gastronomia'], 'Recanto da Tapera', 'Gastronomia afetiva com pratos regionais do Serido.', 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e', False, 1),
            (cat_ids['Gastronomia'], 'Gastrobar', 'Refeicao com vista na Serra do Joao do Vale.', 'https://images.unsplash.com/photo-1501785888041-af3ef285b470', False, 2),
            (cat_ids['Gastronomia'], 'Praca dos Trailers', 'Gastronomia de rua em Caico.', 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee', False, 3),
            (cat_ids['Gastronomia'], 'Tempor da Terra', 'Referencia em comida caseira.', 'https://images.unsplash.com/photo-1491553895911-0055eca6402d', False, 4),
            (cat_ids['Gastronomia'], 'Mozafla', 'Comida caseira no Serido.', 'https://images.unsplash.com/photo-1501785888041-af3ef285b470', False, 5),
            (cat_ids['Gastronomia'], 'Restaurante do Zorro', 'Culinaria regional as margens da BR-226.', 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee', False, 6)
        ]
        cursor.executemany("INSERT INTO conteudos (categoria_id, titulo, descricao, imagem_url, destaque, ordem) VALUES (%s,%s,%s,%s,%s,%s)", gastronomias)
        conn.commit()
        cursor.close()
        conn.close()
        print("Dados inseridos!")
    except Error as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    print("Criando banco Memoria Potiguar...")
    create_database()
    print("Criando tabelas...")
    create_tables()
    print("Inserindo dados...")
    insert_initial_data()
    print("Concluido! Banco pronto.")
