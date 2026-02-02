# Explicações Técnicas — Teste de Estágio IntuitiveCare

Este documento descreve, de forma objetiva, as decisões técnicas adotadas ao longo da solução proposta para o teste de nivelamento do processo seletivo de Estágio na IntuitiveCare (2026).

---

## 1. Fonte dos Dados

Os dados utilizados são provenientes das Demonstrações Contábeis disponibilizadas publicamente pela ANS (Agência Nacional de Saúde Suplementar), conforme link indicado no enunciado do teste.

Foram considerados os três trimestres mais recentes disponíveis no momento da análise, correspondentes ao ano de 2025.

---

## 2. Análise Inicial da Fonte de Dados

Durante a etapa de exploração dos arquivos disponibilizados pela ANS, foi realizada uma análise inicial da estrutura dos dados, incluindo:
- Identificação do formato dos arquivos;
- Consulta ao dicionário de dados oficial;
- Verificação das colunas efetivamente presentes nos arquivos trimestrais.

Foi identificado que alguns campos exigidos nas etapas posteriores do teste (como **CNPJ, Razão Social, Trimestre, Ano** e **Valor de Despesas**) **não estão explicitamente presentes** nos arquivos patrimoniais originais fornecidos pela fonte.

Essa característica foi tratada como uma limitação estrutural da fonte, e não como erro de processamento.

---

## 3. Decisão Técnica: Padronização Estrutural dos Dados (Trade-off)

Diante da ausência de alguns campos exigidos nas etapas posteriores do teste, optou-se por realizar uma **padronização estrutural do conjunto de dados consolidado**, criando explicitamente as colunas requeridas pelo domínio do problema, mesmo quando essas informações não estavam disponíveis nos arquivos originais.

A estratégia adotada foi:
- Criar todas as colunas exigidas pelo teste (**CNPJ, RazaoSocial, Trimestre, Ano, ValorDespesas**);
- Preencher com valores nulos (`null`) os campos cuja informação não pudesse ser obtida diretamente a partir da fonte original;
- Preservar integralmente os dados originais existentes, sem inferências, enriquecimento externo ou suposições não suportadas pela fonte.

Essa abordagem foi escolhida considerando que:
- A padronização estrutural é essencial para viabilizar as etapas posteriores de **validação de dados (Teste 2.1), enriquecimento por join com dados cadastrais (Teste 2.2)** e **agregação analítica (Teste 2.3)**;
- A existência prévia das colunas permite aplicar regras de validação e tratamento de inconsistências de forma explícita e controlada;
- O pipeline torna-se mais previsível, extensível e aderente às especificações do teste, mesmo diante de limitações da fonte original.


---

## 4. Processamento dos Arquivos

Os arquivos trimestrais foram processados utilizando Python e a biblioteca Pandas, seguindo as etapas:
1. Leitura automática dos arquivos CSV presentes na pasta `data/raw`;
2. Verificação da consistência estrutural das colunas entre os diferentes trimestres;
3. Consolidação dos dados em um único DataFrame;
4. Geração de um arquivo CSV consolidado para uso nas etapas subsequentes do teste.

Como parte da consolidação (teste 1.3), o arquivo gerado foi padronizado para conter todas as colunas exigidas pelo enunciado do teste, ainda que algumas delas não estivessem disponíveis na fonte original. Nessas situações, os campos foram explicitamente criados e preenchidos com valores nulos, garantindo consistência estrutural e preparando o dataset para as etapas de validação e enriquecimento posteriores.

Para fins de entrega do teste, o arquivo CSV consolidado é compactado em um arquivo ZIP conforme especificado no enunciado.

---

## 5. Trade-off Técnico: Processamento em Memória

Optou-se pelo processamento dos arquivos em memória, considerando:
- Volume de dados compatível com o ambiente local de execução;
- Simplicidade e clareza do pipeline de dados;
- Facilidade de leitura, manutenção e entendimento do código, alinhada ao contexto de um teste técnico para estágio.

Essa abordagem foi considerada adequada ao escopo do projeto.

---

## 6. Versionamento e Arquivos de Dados

Arquivos de grande volume (como CSVs consolidados e arquivos brutos) não foram versionados no repositório GitHub, respeitando as limitações da plataforma.

Esses arquivos são gerados automaticamente a partir dos scripts disponíveis no projeto, garantindo reprodutividade sem comprometer o versionamento do código.

---

## 7. Validação de Dados (Teste 2.1)

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

## 8. Enriquecimento de Dados com Tratamento de Falhas (Teste 2.2)

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

## 9. Agregação de Despesas por Operadora e UF

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