LOAD DATA INFILE '/C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/04_base_enriquecida_2025.csv'
INTO TABLE operadoras
CHARACTER SET utf8mb4 
FIELDS TERMINATED BY ';'
ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS (
    cnpj,
    razao_social,
    @registro_ans,
    @modalidade,
    @uf
)
SET
    registro_ans = NULLIF(@registro_ans, ''),
    modalidade   = NULLIF(@modalidade, ''),
    uf           = NULLIF(@uf, '');
    
LOAD DATA INFILE '/C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/02_base_consolidada_2025.csv'
INTO TABLE despesas_consolidadas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '\n'
IGNORE 1 ROWS (
    cnpj,
    razao_social,
    @ano,
    @trimestre,
    @valor
)
SET
    ano = CAST(@ano AS UNSIGNED),
    trimestre = @trimestre, valor_despesas = 
      CASE
          WHEN @valor REGEXP '^[0-9]+(\\.[0-9]{1,2})?$'
          THEN CAST(@valor AS DECIMAL(15,2))
          ELSE 0
      END;
      
LOAD DATA INFILE '/C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/despesas_agregadas.csv'
INTO TABLE despesas_agregadas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS (
    razao_social,
    uf,
    total_despesas,
    media_trimestral,
    desvio_padrao
);