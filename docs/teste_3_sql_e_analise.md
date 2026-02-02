# Explicações Técnicas — Teste 3 do Estágio IntuitiveCare

Este documento descreve, de forma objetiva, as decisões técnicas adotadas na etapa do teste 3 para o teste de nivelamento do processo seletivo de Estágio na IntuitiveCare (2026).

---

## 3.1. Arquivos Utilizados

Para a modelagem e criação das tabelas no banco de dados, foram utilizados os seguintes arquivos CSV, gerados nas etapas anteriores do pipeline:
- **consolidado_despesas.csv** (Teste 1.3) Contém os dados consolidados de despesas por operadora, trimestre e ano, após tratamento de inconsistência na fonte.
- **04_base_enriquecida_2025.csv** (Teste 2.2) Dados cadastrais das operadoras, resultantes do consolidado com informações da ANS (RegistroANS, Modalidade e UF), incluindo tratamento de falhas e duplicidades.
- **despesas_agregadas.csv** (Teste 2.3) Dados agregados por Razão Social e UF, contendo métricas analíticas (total de despesas, média trimestral e desvio padrão).

Esses arquivos representam **diferentes níveis do pipeline** (consolidado, enriquecido e agregado), permitindo tanto análises detalhadas quanto visões sumarizadas.

---

## Estratégia de Modelagem

### Abordagem escolhida: Opção B — Tabelas Normalizadas

Foi adotada uma modelagem **normalizada**, com separação lógica entre:
- Dados cadastrais das operadoras
- Dados consolidados de despesas
- Dados agregados para análise

### Justificativa da escolha

#### Volume de dados esperado

Os dados consolidados de despesas tendem a crescer continuamente a cada novo trimestre,enquanto os dados cadastrais das operadoras mudam com baixa frequência. A normalização evita duplicação desnecessária dessas informações.

#### Frequência de atualização

- Dados cadastrais: atualizações pontuais
- Dados de despesas: carga recorrente (trimestral)

Separa essas entidades reduz impacto de atualizações e facilita manutenção.

#### Complexidade das queries analíticas

A estrutura normalizada mantém clareza e rastreabilidade, permitindo:
- Análises detalhadas a partir das tabelas consolidadas
- Consultas analíticas rápidas usando a tabela agregada
- Evolução futura do modelo sem retrabalho estrutural

---

## Estrutura das Tabelas

### Tabela `operadoras`

Armazena os dados cadastrais das operadoras de planos de saúde.

### Principais decisões técnicas:

- `cnpj` definido como **chave primária**
- Índice por `uf` para facilitar análises regionais

Campos:
- cnpj
- razao_social
- registro_ans
- modalidade
- uf

### Tabela `despesas_consolidadas`

Armazena as despesas consolidadas por operadora e período.

### Principais decisões técnicas:

- Chave primária técnica (`id`) para facilitar carga e manutenção
- Chave estrangeira (`cnpj`) referenciando a tabela `operadoras`
- Constraint `UNIQUE` (`cnpj`, `ano`, `trimestre`) garantindo integridade temporal dos dados
- Índices para acelerar consultas por operadoras e período

Campos:
- id
- cnpj
- ano
- trimestre
- valor_despesas

### Justificativa do `UNIQUE`:
Garante que uma mesma operadora não possua mais de um registro de despesas para o mesmo ano e trimestre, prevenindo duplicações na carga de dados.

### Tabela `despesas_agregadas`

Tabelda analítica com dados já sumarizados para consultas rápidas.

### Principais decisões técnicas:

- Dados mantidos separados da base transacional
- Estrutura otimizada para leitura e ranking de despesas
- Índice composto por `uf` e `total_despesas`

Campos:
- id
- razao_social
- uf
- total_despesas
- media_trimestral
- desvio_padrão

---

## Trade-off Técnico — Tipos de Dados

### Valores monetários

**Escolha**: `DECIMAL(15,2)`

### Justificativa:

- Evita problemas de precisão do tipo `FLOAT`
- Mantém exatidão necessária para valores financeiros
- Suporta valores elevados sem perda de informação

### Datas e períodos

**Ano**: `INT`
**Trimestre**: `VARCHAR(7)` (ex: `2024-Q3`)

### Justificativa:

- Mantém compatibilidade com o formato original dos dados
- Facilita leitura humana e rastreabilidade 
- Evita conversões desnecessárias em um cenário analítico

## Considerações Finais

A modelagem proposta:
- Mantém integridade referencial
- Evita redundância de dados
- Facilita cargas recorrentes 
- Atende aos requisitos analíticos do teste
- Está preparada para evolução futura do pipeline

---

Durante a etapa de carga dos CSVs no MySQL (Teste 3.3), foi utilizada a estratégia `LOAD DATA`, adequada para grandes volumes de dados.

No ambiente Windows com MySQL Workbench, foram identificadas limitações do driver de importação (`charmap codec error`) mesmo após:
- conversão explícita de encoding para UTF-8
- remoção de caracteres de controle ASCII

Esses erros são conhecidos no Workbench em ambientes Windows.

Como alternativa viável e comum em produção, a carga poderia ser realizada via:
- `LOAD DATA LOCAL INFILE` com cliente configurado
- importação via linha de comando (`mysql < script.sql`)
- ou ingestão intermediária via ETL (Python -> INSERTs em lote)

Para fins do teste, foram elaborados os scripts SQL completos, garantindo rastreabilidade do processo.


---

# Teste 3.4 - Queries Analíticas em SQL 

## Objetivo

Desenvolver queries analíticas a partir dos dados carregados no banco de dados, com foco em extração de insights financeiros, respeitando integridade dos dados, performance e clareza de leitura do código.

As queries foram escritas em SQL compatível com **MySQL 8.0**, utilizando os dados importados nas etapas anteriores do Teste 3.3.

---

## Bases Utilizadas

As análises utilizam as seguintes tabelas:
- `despesas_consolidadas` Dados consolidados de despesas por operadora, ano e trimestre.
- `operadoras` Dados cadastrais das operadoras (CNPJ, Razão Social, UF, Modalidade, Registro ANS).
- `despesas_agregadas` Dados previamente agregados por Razão Social e UF, com métricas estatísticas.

---

## Query 1
### Top 5 operadoras com maior crescimento percentual de despesas

**Pergunta:** Quais são as 5 operadoras com maior crescimento percentual de despesas entre o primeiro e o último trimestre analisado?

### Estratégia adotada

- Identificação do **primeiro** e do **último trimestre disponível** para cada operadora.
- Cálculo da variação percentual entre esses dois períodos.
- Uso de `JOIN` entre as tabelas de despesas e operadoras para recuperar informações cadastrais.
- Exclusão de divisões por zero para evitar erros matemáticos.

### Tratamento do desafio

Operadoras que não possuem dados em todos os trimestres:
- Foram considerados apenas aquelas que possuem **valores válidos tanto no primeiro quanto no último trimestre**.
- Essa decisão evita distorções no cálculo do crescimento percentual.

### Justicativa técnica

- Garante comparabilidade real entre períodos.
- Evita crescimento artificial causado por ausência de dados intermediários.
- Mantém a query clara e auditável.

---

## Query 2
### Distribuição e média de despesas por UF 

**Pergunta:** Qual a distribuição de despesas por UF? Quais são os 5 estados com maiores despesas totais?

**Desafio adicional:** Calcular também a **média de despesas por operadora em cada UF**.

### Estratégia adotada

- O agrupamento direto em SQL reduz necessidade de pós-processamento.
- Permite análises comparativas entre estados.
- Aproveita índices definidos na modelagem para melhorar performance.

---

## Query 3
### Operadoras com despesas acima da média em pelo menos 2 trimestres

**Pergunta:** Quantas operadoras tiveram despesas acima da média geral em pelo menos 2 dos 3 trimestres analisados?

### Estratégia adotada

- Cálculo da **média geral de despesas** considerando todos os registros.
- Comparação das despesas de cada operadora por trimestre com essa média.
- Contagem de quantos trimestres cada operadora ficou acima da média.
- Seleção apenas das operadores que atenderam ao critério mínimo de 2 trimestres.

### Trade-off técnico

**Abordagem escolhida:** subqueries e agregações controladas.

**Alternativas consideradas:** 
- Uso de janelas analíticas (`OVER()`).
- Pré-agregações em tabelas temporárias.

**Motivo da escolha:**
- Melhor legibilidade do código.
- Compatibilidade total com MySQL 8.
- Facilidade de manutenção e explicação.

---

## Considerações de Performance

- As queries foram desenhadas considerando o **volume de dados esperado para o teste**, priorizando clareza e corretude.
- Índices definidos nas tabelas (`cnpj`, `uf`, `ano`, `trimestre`) auxiliam na execução eficiente das consultas.
- Para volumes muito maiores, seria possível evoluir para:
    - Materialized views
    - Paricionamento por período
    - Uso mais intensivo de funções analíticas

---

## Conclusão

As queries analíticas desenvolvidas atendem integralmente aos requisitos do Teste 3.4, oferecendo:
- Respostas claras às perguntas de negócio 
- Tratamento explícito de inconsistências e ausências de dados 
- Código SQL legível, justificável e alinhado às boas práticas

Essas análises demonstram domínio tanto de modelagem de dados quanto de raciocínio analítico em SQL.

---