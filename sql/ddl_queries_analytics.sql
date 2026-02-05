-- =================================================================
-- Queries Analíticas 
-- Banco: MySQL 8.0
-- Objetivo: Análise de despesas das operadoras de planos de saúde
-- =================================================================

-- Query 1 - Top 5 operadoras com maior crescimento percentual de despesas

WITH base AS (
    SELECT
        id_operadora,
        ano,
        trimestre,
        valor_despesas,
        (ano * 10 +
            CASE trimestre
                WHEN 'T1' THEN 1
                WHEN 'T2' THEN 2
                WHEN 'T3' THEN 3
                WHEN 'T4' THEN 4
            END
        ) AS ordem_periodo
    FROM despesas_consolidadas
),
periodos AS (
    SELECT
        id_operadora,
        MIN(ordem_periodo) AS primeiro_periodo,
        MAX(ordem_periodo) AS ultimo_periodo
    FROM base
    GROUP BY id_operadora
    HAVING MIN(ordem_periodo) <> MAX(ordem_periodo)
),
valores AS (
    SELECT
        p.id_operadora,
        b_ini.valor_despesas AS despesa_inicial,
        b_fim.valor_despesas AS despesa_final
    FROM periodos p
    JOIN base b_ini
        ON b_ini.id_operadora = p.id_operadora
       AND b_ini.ordem_periodo = p.primeiro_periodo
    JOIN base b_fim
        ON b_fim.id_operadora = p.id_operadora
       AND b_fim.ordem_periodo = p.ultimo_periodo
)
SELECT
    o.razao_social,
    despesa_inicial,
    despesa_final,
    ROUND(
        CASE
            WHEN despesa_inicial = 0 THEN NULL
            ELSE ((despesa_final - despesa_inicial) / despesa_inicial) * 100
        END,
        2
    ) AS crescimento_percentual
FROM valores v
JOIN operadoras o
    ON o.id_operadora = v.id_operadora
ORDER BY crescimento_percentual DESC
LIMIT 5;


-- Query 2 - Distribuição de despesas por UF com total e média por operadora

SELECT
    o.uf,
    SUM(dc.valor_despesas) AS total_despesas,
    ROUND(
        SUM(dc.valor_despesas) / COUNT(DISTINCT dc.id_operadora),
        2
    ) AS media_por_operadora
FROM despesas_consolidadas dc
JOIN operadoras o
    ON o.id_operadora = dc.id_operadora
GROUP BY o.uf
ORDER BY total_despesas DESC
LIMIT 5;


-- Query 3 - Operadoras acima da média geral em pelo menos dois trimestres

WITH media_trimestre AS (
    SELECT
        ano,
        trimestre,
        AVG(valor_despesas) AS media_geral
    FROM despesas_consolidadas
    GROUP BY ano, trimestre
),
comparacao AS (
    SELECT
        dc.id_operadora,
        dc.ano,
        dc.trimestre,
        dc.valor_despesas,
        mt.media_geral
    FROM despesas_consolidadas dc
    JOIN media_trimestre mt
        ON dc.ano = mt.ano
       AND dc.trimestre = mt.trimestre
),
contagem AS (
    SELECT
        id_operadora,
        COUNT(*) AS qtd_trimestres_acima_media
    FROM comparacao
    WHERE valor_despesas > media_geral
    GROUP BY id_operadora
)
SELECT
    COUNT(*) AS total_operadoras
FROM contagem
WHERE qtd_trimestres_acima_media >= 2;