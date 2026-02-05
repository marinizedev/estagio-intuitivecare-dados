# Explicações Técnicas — Teste 3 do Estágio IntuitiveCare

Este documento descreve, de forma objetiva, as decisões técnicas adotadas na etapa do teste 3 para o teste de nivelamento do processo seletivo de Estágio na IntuitiveCare (2026).

---

## Arquivos Utilizados

Para a modelagem e criação das tabelas no banco de dados, foram utilizados os seguintes arquivos CSV, gerados nas etapas anteriores do pipeline:

- **consolidado_despesas.csv** (Teste 1.3): Dados consolidados de despesas por operadora, trimestre e ano, após tratamento de inconsistência na fonte.  
- **04_base_enriquecida_2025.csv** (Teste 2.2): Dados cadastrais das operadoras, resultantes do consolidado com informações da ANS (RegistroANS, Modalidade e UF), incluindo tratamento de falhas e duplicidades.  
- **despesas_agregadas.csv** (Teste 2.3): Dados agregados por Razão Social e UF, com métricas analíticas (total de despesas, média trimestral e desvio padrão).  

Esses arquivos representam diferentes níveis do pipeline (consolidado, enriquecido e agregado), permitindo tanto análises detalhadas quanto visões sumarizadas.

---

## Estratégia de Modelagem

### Abordagem escolhida: Tabelas Normalizadas

Foi adotada uma modelagem **normalizada**, com separação lógica entre:

- Dados cadastrais das operadoras  
- Dados consolidados de despesas  
- Dados agregados para análise  

### Justificativa da escolha

- **Volume de dados esperado**: Dados consolidados de despesas crescem continuamente, enquanto dados cadastrais mudam pouco. Normalização evita duplicação.  
- **Frequência de atualização**: Dados cadastrais pontuais, despesas recorrentes (trimestrais).  
- **Complexidade de queries analíticas**: Normalização mantém rastreabilidade e clareza, permitindo análises detalhadas e consultas rápidas.

---

## Estrutura das Tabelas

### Tabela `operadoras`

- **Chave primária**: `id_operadora`  
- **Índice**: `uf`  

Campos:

- `reg_ans`
- `cnpj`  
- `razao_social`  
- `modalidade`  
- `uf`  

---

### Tabela `despesas_consolidadas`

- **Chave primária técnica**: `id`  
- **Chave estrangeira**: `id_operadora` → `operadoras`  
- **UNIQUE**: (`id_operadora`, `ano`, `trimestre`)  
- **Índices**: `ano`, `trimestre` 

Campos:

- `id`
- `id_operadora`  
- `ano`  
- `trimestre`  
- `valor_despesas`  

**Justificativa do UNIQUE**: Garante que uma mesma operadora não tenha duplicidade no mesmo trimestre/ano.

---

### Tabela `despesas_agregadas`

- **Chave primária técnica**: `id`
- **Chave estrangeira**: `id_operadora` → `operadoras`
- **Índices**: `id_operadora`  

Campos:

- `id`  
- `id_operadora`  
- `total_despesas`  
- `media_trimestral`  
- `desvio_padrão`  

---

## Trade-off Técnico — Tipos de Dados

- **Valores monetários**: `DECIMAL(15,2)` (precisão, evita problemas do FLOAT)  
- **Ano**: `INT`  
- **Trimestre**: `VARCHAR(7)` (ex.: `2024-Q3`)  

Justificativa: compatível com os dados originais, facilita leitura e rastreabilidade.

---

## Abordagem em Camadas — Staging e Normalização

Devido à heterogeneidade estrutural dos arquivos CSV gerados nas etapas anteriores, foi adotada uma abordagem em **duas camadas**:

- **Camada de staging**: mantém estrutura fiel aos arquivos originais, sem alterações, garantindo ingestão segura mesmo diante de inconsistências (valores nulos, tipos divergentes, colunas redundantes).  
- **Camada analítica normalizada**: tabelas finais projetadas para integridade, performance e clareza das análises, separando operadoras, despesas consolidadas e agregadas.

Essa abordagem permite controle total sobre a transformação dos dados, preservando rastreabilidade e evitando perda de informações.

---

### Estratégia de Inserção de Dados

Devido a limitações do ambiente Windows (erros de driver e codificação) e questões de segurança, a carga dos CSVs para tabelas normalizadas foi realizada via **Python**:

- Inserção segura linha a linha ou em lotes  
- Tratamento de tipos de dados e valores nulos  
- Rastreamento de registros carregados  

Essa alternativa substituiu temporariamente o `LOAD DATA INFILE`, mantendo integridade e rastreabilidade sem depender de configurações específicas do banco.

---

## Queries Analíticas em SQL

### Bases Utilizadas

- `despesas_consolidadas`  
- `operadoras`  
- `despesas_agregadas`  

---

### Query 1 — Top 5 operadoras com maior crescimento percentual de despesas

**Objetivo**: Identificar as 5 operadoras com maior crescimento percentual entre o primeiro e último trimestre analisado.  

**Estratégia**:

- Considerar apenas operadoras com **valores válidos no primeiro e último trimestre**  
- Cálculo do crescimento percentual: `(Valor Final - Valor Inicial) / Valor Inicial * 100`  
- Evita divisão por zero e distorções  

**Justificativa**:

- Reflete a realidade dos dados  
- Evita exclusão indevida de operadoras  
- Query legível, auditável e performática

---

### Query 2 — Distribuição de despesas por UF

**Objetivo**: Identificar estados com maior despesa e calcular média por operadora.  

**Estratégia**:

- `SUM(valor_despesas)` por UF  
- Média: total de despesas dividido por `COUNT(DISTINCT id_operadora)`  
- Ordenar decrescente e limitar aos 5 maiores  

**Justificativa**:

- Explora normalização do modelo  
- Boa performance  
- Métricas claras de volume e comportamento médio

---

### Query 3 — Operadoras acima da média em pelo menos 2 trimestres

**Objetivo**: Contar operadoras com despesas acima da média geral em pelo menos 2 trimestres.  

**Estratégia**:

- **CTEs (Common Table Expressions)** para legibilidade  
- Etapa 1: calcular média geral por trimestre  
- Etapa 2: comparar cada operadora com a média  
- Etapa 3: contar trimestres acima da média  
- Etapa 4: filtrar ≥ 2 trimestres  

**Justificativa**:

- Alta legibilidade  
- Facilidade de manutenção  
- Boa performance e debug simples  
- Adequada para cenários analíticos

---

## Considerações Finais

- Modelagem mantém integridade referencial e evita redundância  
- Abordagem em camadas garante ingestão segura e rastreabilidade  
- Python permitiu carga segura devido a limitações do ambiente  
- Queries atendem aos requisitos analíticos do teste  
- Estrutura preparada para evolução futura do pipeline
