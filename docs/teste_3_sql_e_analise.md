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