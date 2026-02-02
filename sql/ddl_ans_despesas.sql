-- ==============================================================================
-- Teste 3 - Criação das tabelas
-- Banco compatível: MySQL 8.0.32.0
-- Origem dos dados:
-- - 02_base_consolidada_2025.csv (consolidado_despesas.csv | Teste 1.3)
-- - 04_base_enriquecida_2025.csv (dados cadastrais tratados | Teste 2.2)
-- - despesas_agregadas.csv (Teste 2.3)
-- Objetivo:
-- Criar a estrutura de tabelas para carga e análise dos dados de despesas da ANS
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS ans_despesas
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ans_despesas;

CREATE TABLE operadoras (
    cnpj CHAR(14) PRIMARY KEY,
    razao_social VARCHAR(255) NOT NULL,
    registro_ans VARCHAR(20),
    modalidade VARCHAR(100),
    uf CHAR(2),
    
    INDEX idx_operadoras_uf (uf)
);

CREATE TABLE despesas_consolidadas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cnpj CHAR(14) NOT NULL,
    ano INT NOT NULL,
    trimestre VARCHAR(7) NOT NULL,
    valor_despesas DECIMAL(15,2) NOT NULL,
    
    INDEX idx_cnpj (cnpj),
    INDEX idx_ano_trimestre (ano, trimestre),
    
    CONSTRAINT fk_despesas_operadora
    FOREIGN KEY (cnpj)
    REFERENCES operadoras(cnpj),
    
    UNIQUE (cnpj, ano, trimestre) 
);

CREATE TABLE despesas_agregadas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    razao_social VARCHAR(255) NOT NULL,
    uf CHAR(2) NOT NULL,
    total_despesas DECIMAL(15,2) NOT NULL,
    media_trimestral DECIMAL(15,2),
    desvio_padrao DECIMAL(15,2),
    
    INDEX idx_agregadas_uf_total (uf, total_despesas)
);