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
