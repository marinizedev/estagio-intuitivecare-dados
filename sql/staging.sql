-- ==========================================
-- Staging table
-- Utilizadas para cargas temporárias e
-- tratamento inicial dos dados
-- ==========================================

CREATE TABLE stg_despesas_consolidadas (
    data DATE,
    reg_ans INT,
    cd_conta_contabil BIGINT,
    descricao VARCHAR(255),
    vl_saldo_inicial DECIMAL(15,2),
    vl_saldo_final DECIMAL(15,2)
) CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE TABLE str_base_enriquecida (
    data DATE,
    reg_ans INT,
    cd_conta_contabil BIGINT,
    descricao VARCHAR(255),
    vl_saldo_inicial DECIMAL(15,2),
    vl_saldo_final DECIMAL(15,2),
    cnpj CHAR(14),
    razaoSocial VARCHAR(255),
    trimestre VARCHAR(7),
    ano INT,
    valorDespesas DECIMAL(15,2),
    registro_operadora INT,
    razao_social VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2)
) CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE TABLE stg_despesas_agregadas (
    razao_social VARCHAR(255),
    uf CHAR(2),
    total_despesas DECIMAL(15,2),
    media_trimestral DECIMAL(15,2),
    desvio_padrao DECIMAL(15,2)
) CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;