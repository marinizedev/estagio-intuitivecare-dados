-- =================================================================
-- Queries Analíticas 
-- Banco: MySQL 8.0
-- Objetivo: Análise de despesas das operadoras de planos de saúde
-- =================================================================

-- Query 1 - Top 5 operadoras com maior crescimento percentual de despesas

WITH despesas_por_trimestre AS (
    SELECT
        d.cnpj,
        o.razao_social,
        CONCAT(d.ano, '-', d.trimestre) AS periodo,
        SUM(d.valor_despesas) AS total_despesas
    FROM despesas_consolidadas d 
    JOIN operadoras o ON o.cnpj = d.cnpj
    GROUP BY d.cnpj, o.razao_social, d.ano, d.trimestre
),
periodos_extremos AS (
    SELECT
        cnpj,
        MIN(periodo) AS primeiro_periodo,
        MAX(periodo) AS ultimo_periodo
    FROM despesas_por_trimestre
    GROUP BY cnpj
),
comparativo AS (
    SELECT 
        d1.cnpj,
        d1.razao_social,
        d1.total_despesas AS despesas_inicio,
        d2.total_despesas AS despesas_fim,
        ((d2.total_despesas - d1.total_despesas) / d1.total_despesas) * 100 AS crescimento_percentual
    FROM periodos_extremos p 
    JOIN despesas_por_trimestre d1 ON d1.cnpj = p.cnpj AND d1.periodo = p.primeiro_periodo
    JOIN despesas_por_trimestre d2 ON d2.cnpj = p.cnpj AND d2.periodo = p.ultimo_periodo
    WHERE d1.total_despesas > 0
)
SELECT *
FROM comparativo
ORDER BY crescimento_percentual DESC LIMIT 5;

-- Query 2 - Distribuição e média de despesas por UF

SELECT
    o.uf,
    SUM(d.valor_despesas) AS total_despesas_uf,
    AVG(d.valor_despesas) AS media_despesas_por_operadora
FROM despesas_consolidadas d
JOIN operadoras o ON o.cnpj = d.cnpj
GROUP BY o.uf
ORDER BY total_despesas_uf DESC LIMIT 5;

-- Query 3 - Operadoras acima da média geral em pelo menos dois trimestres

WITH media_geral AS (
    SELECT AVG(valor_despesas) AS media_global
    FROM despesas_consolidadas
),
acima_media AS (
    SELECT 
        d.cnpj,
        COUNT(*) AS trimestres_acima_media
    FROM despesas_consolidadas d
    CROSS JOIN media_geral m
    WHERE d.valor_despesas > m.media_global
    GROUP BY d.cnpj
)
SELECT COUNT(*) AS total_operadoras
FROM acima_media
WHERE trimestres_acima_media >= 2;