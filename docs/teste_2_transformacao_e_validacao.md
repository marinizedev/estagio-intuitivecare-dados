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

## Enriquecimento de Dados com Tratamento de Falhas (Teste 2.2)

Nesta etapa, o CSV consolidado resultante do Teste 2.1 foi enriquecido com informações cadastrais da ANS, por meio da adição das colunas **RegistroANS, Modalidade e UF**.

### Estratégia adotada

- Padronização dos CNPJs em ambos os datasets (remoção de caracteres não numéricos) para garantir consistência na chave de junção;
- Utilização de **left join** com base no campo `CNPJ_limpo`, preservando integralmente os registros do CSV consolidado;
- Registros sem correspondência no cadastro da ANS receberam o valor **"Não encontrado"** nas colunas adicionadas;
- Duplicidades no cadastro da ANS foram tratadas mantendo-se a primeira ocorrência por CNPJ.

### Trade-offs técnicos

- A escolha do **left join** garante rastreabilidade total dos dados originais, evitando perda de informações do consolidado;
- A resolução simples de duplicatas no cadastro prioriza clareza e previsibilidade, adequada ao contexto e volume de dados do teste;
- O registro explícito de valores ausentes facilita análises posteriores, validações adicionais e auditoria dos dados enriquecidos.

---

## Agregação de Despesas por Operadora e UF

Para consolidar e analisar os gastos, foi realizada a agregação dos dados a partir do CSV enriquecido, conforme os critérios estabelecidos no teste.

### Estratégia de agregação

- **Agrupamento**: realizado por `RazaoSocial` e `UF`;
- **Cálculos aplicados**:
    - `total_despesas`: soma total das despesas por operadora e UF;
    - `media_trimestral`: média das despesas com base nos registros disponíveis;
    - `desvio_padrao`: cálculo do desvio padrão para identificar variações relevantes nos valores de despesas;
- **Ordenação**: os resultados foram ordenados pelo `total_despesas`, do maior para o menor, facilitando a identificação das operadoras com maiores gastos;
- **Tratamento de dados**: valores não numéricos na coluna `ValorDespesas` foram convertidos para zero, evitando falhas durante o processo de agregação;
- **Saída**: geração do arquivo final `despesas_agregadas.csv`.

### Justificativa técnica:

- O processamento em memória foi considerado adequado, dado o volume de dados envolvido no teste;
- A utilização do método `groupby` do pandas garante simplicidade, clareza e rastreabilidade dos cálculos realizados;
-  A abordagem mantém consistência com as etapas anteriores de validação e enriquecimento, permitindo análises futuras sem perda de informação ou integridade dos dados.

### Organização dos arquivos processados

Os arquivos na pasta `data/processed` seguem uma numeração incremental (`01_, 02_, 03_, 04_`) para representar cada etapa do pipeline de dados. Essa abordagem foi adotada para garantir rastreabilidade, clareza do fluxo de processamento e facilidade de auditoria. **Os nomes exigidos no enunciado foram respeitados nos artefatos finais de entrega, enquanto os arquivos intermediários seguem uma convenção técnica para organização do pipeline**.

### Compactação dos arquivos

Embora o enunciado mencione a compactação do CSV ao final do teste 1.3, optou-se por manter os arquivos intermediários em formato CSV durante o desenvolvimento para facilitar inspeção, validação e rastreabilidade do pipeline. Para fins de entrega, todos os artefatos finais e intermediários foram compactados em um único arquivo `Teste_Marinize_Santana.zip`, conforme solicitado ao final do teste 2.3.