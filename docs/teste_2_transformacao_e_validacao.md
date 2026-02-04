# Explicações Técnicas — Teste 2 do Estágio IntuitiveCare

Este documento descreve, de forma objetiva, as decisões técnicas adotadas na etapa do teste 2 para o teste de nivelamento do processo seletivo de Estágio na IntuitiveCare (2026).

---

## Validação de Dados (Teste 2.1)

A partir do CSV consolidado gerado na etapa 1.3, foi implementada uma etapa de validação dos dados com o bjetivo de garantir consistência mínima antes das etapas de enriquecimento e agregação.

Foram aplicadas as seguintes validações:
- **CNPJ**: verificação de formato e cálculo dos dígitos verificadores, identificando registros inválidos;
- **Razão Social**: validação de preenchimento, considerando valores nulos, vazios ou compostos apenas por espaços;
- **Valor de Despesas**: verificação de valores numéricos positivos, identificando registros zerados ou negativos.

### Tratamento de CNPJs inválidos (Trade-off técnico)

Para CNPJs inválidos, optou-se por **não descatar os registros**, mas **marcá-los como inválidos por meio de flags de validação**.

Essa abordagem foi escolhida considerando:
- Preservação da rastreabilidade dos dados;
- Evitar perda de informação potencialmente relevante;
- Possibilidade de auditoria e reprocessamento futuro.

Os registros inválidos permanecem no dataset, porém explicitamente identificados, permitindo decisões posteriores mais conscientes nas etapas seguintes do pipeline.

---

## Teste Técnico (Itens 2.2 e 2.3)

### Visão Geral

Este documento descreve, de forma clara e estruturada, todo o raciocínio, decisões técnicas e desafios enfrentados durante a execução dos intens **2.2 (Enriquecimento dos Dados)** e **2.3 (Agregação dos Dados)** do teste técnico.

O objetivo principal foi demonstrar não apenas o resultado final, mas também a **capacidade de análise crítica diante de inconsistências entre o enunciado e os dados reais, algo comum em cenários reais de mercado (que descobri na prática no processo deste teste).

### Contexto Geral do Problema

O teste solicitava a construção de um pipeline de dados a partir de bases fornecidas, envolvendo:
- Consolidação de dados de despesas
- Enriquecimento com informações cadastrais das operadoras
- Agregação para geração de métricas analíticas

Durante a execução, foi identificado que **algumas expectativas do enunciado não correspondiam exatamente à estrutura e ao conteúdo dos arquivos fornecidos, exigindo análise exploratória, validações e ajustes técnicos.

## Item 2.2 — Enriquecimento dos Dados

### Objetivo

Enriquecer a base consolidada de despesas com informações cadastrais das operadoras de plano de saúde, utilizando como chave o registro da ANS.

### Fontes de Dados

- **Base consolidada de despesas** (02_base_consolidada_2025.csv)
- **Cadastro de opeadoras ativas** (operadoras_ativas.csv)

### Desafio Encontrado

O enunciado sugeria um relacionamento direto entre as bases, porém:
- As colunas de chave possuíam **nomes diferentes**:
    - `REG_ANS` na base de despesas
    - `REGISTRO_OPERADORA` no cadastro
- Os dados exigiram **padronização de tipo e limpeza** para garantir correspondência correta

Sem esse tratamento, o processo de `merge` resultava em registros sem correspondência (campos nulos).

### Estratégia Adotada

1. Leitura dos arquivos CSV com separador correto (;) e encoding `latin1`
2. Padronização das colunas-chave:
    - Conversão para `string`
    - Remoção de espaços em branco
3. Seleção apenas das colunas necessárias do cadastro
4. Remoção de duplicidades no cadastro
5. Realização de **LEFT JOIN**, garantindo a preservação de todos os registros de despesas
6. Tratamento de registros sem correspondência

### Validação do Resultado

Após as correções:
- Foram identificados **2.095.185 registros com correspondência válida** no cadastro
- As colunas `Razao_Social`, `Modalidade` e `UF` foram corretamente preenchidas
- O arquivo final `04_base_enriquecida_2025.csv` foi gerado com sucesso

Este resultado confirmou que o enriquecimento foi executado corretamente, apesar das inconsistências iniciais entre enunciado e dados reais.

## Item 2.3 — Agregação dos Dados

### Objetivo

Gerar uma base analítica agregada, consolidando os valores de despesas por operadora e unidade federativa, produzindo métricas estatísticas.


### Base Utilizada

- `04_base_enriquecida_2025.csv`

### Métricas Geradas

Para cada combinação de **Razão Social** e **UF**, foram calculados:
- **Total de despesas**
- **Média trimestral das despesas**
- **Desvio padrão**

### Desafio Encontrado

Durante a primeira execução:
- O arquivo agregado foi gerado corretamente
- Porém, ao abrir o CSV, aparentava conter apenas os cabeçalhos

Após análise, identificou-se que:
- O problema estava relacionado à **seleção incorreta do nome da coluna** (`RazaoSocial` vs `Razao_Social`)
- Isso resultava em um DataFrame vazio antes da agregação

### Correção Aplicada

- Ajuste dos nomes das colunas para refletirem exatamente o CSV enriquecido
- Inclusão de prints diagnósticos antes da agregação para validação do volume de dados
- Garantia de conversão correta da coluna `ValorDespesas` para tipo numérico

### Resultado Final

Após as correções:
- A agregação foi realizada com sucesso
- O arquivo `despesas_agregadas.csv` passou a conter dados válidos
- Valores nulos de desvio padrão (casos com apenas um trimestre) foram tratados

### Considerações Finais

Este teste evidenciou um cenário comum no mercado de dados: **enunciados nem sempre refletem perfeitamente a realidade dos dados disponíveis**.

A solução exigiu:
- Leitura crítica do problema 
- Exploração dos dados
- Validação contínua 
- Ajustes técnicos fundamentados

Mais do que gerar arquivos CSV, o processo demontrou capacidade analítica, resiliência e adaptação — competências essenciais para atuação profissional em dados.