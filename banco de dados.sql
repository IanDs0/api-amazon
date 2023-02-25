CREATE DATABASE historico_produtos;

USE historico_produtos;

CREATE TABLE categorias (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(50) NOT NULL
);

CREATE TABLE empresas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(50) NOT NULL
);

CREATE TABLE produtos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  url VARCHAR(255) NOT NULL,
  image_url VARCHAR(255) NOT NULL,
  frete_prime BOOLEAN NOT NULL,
  id_categoria INT NOT NULL,
  id_empresa INT NOT NULL,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id),
  FOREIGN KEY (id_empresa) REFERENCES empresas(id)
);

CREATE TABLE precos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_produto INT NOT NULL,
  preco DECIMAL(10,2) NOT NULL,
  data_hora DATETIME NOT NULL,
  FOREIGN KEY (id_produto) REFERENCES produtos(id)
);
