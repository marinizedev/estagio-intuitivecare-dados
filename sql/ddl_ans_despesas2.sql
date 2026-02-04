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
DROP TABLE operadoras;
CREATE TABLE operadoras (
    id_operadora INT PRIMARY KEY AUTO_INCREMENT,
    reg_ans INT NOT NULL,
    cnpj CHAR(14),
    razao_social VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2),
    
    UNIQUE (reg_ans),
    INDEX idx_operadoras_uf (uf)
);
SELECT COUNT(*) FROM operadoras;
drop table despesas_consolidadas;
CREATE TABLE despesas_consolidadas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cnpj CHAR(14),
    ano INT NOT NULL,
    trimestre VARCHAR(7) NOT NULL,
    valor_despesas DECIMAL(15,2) NOT NULL,
    id_operadora INT NOT NULL,
    
    INDEX idx_ano_trimestre (ano, trimestre),
    
    CONSTRAINT fk_despesas_operadora
    FOREIGN KEY (id_operadora)
    REFERENCES operadoras(id_operadora),
    
    UNIQUE (cnpj, ano, trimestre) 
);

CREATE VIEW vw_despesas_agregadas AS
SELECT
    o.razao_social,
    o.uf,
    SUM(da.vl_saldo_final) AS total_despesas,
    AVG(da.vl_saldo_final) AS media_trimestral,
    STDDEV(da.vl_saldo_final) AS desvio_padrao
FROM stg_despesas_agregadas da
JOIN operadoras o ON da.id_operadora = o.id_operadora
GROUP BY o.razao_social, o.uf;