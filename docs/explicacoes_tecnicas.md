# Explicações Técnicas — Teste de Estágio IntuitiveCare

Este documento descreve, de forma objetiva, as decisões técnicas adotadas ao longo da solução proposta para o teste de nivelamento do processo seletivo de Estágio na IntuitiveCare (2026).

---

## 1. Fonte dos Dados

Os dados utilizados são provenientes das Demonstrações Contábeis disponibilizadas publicamente pela ANS (Agência Nacional de Saúde Suplementar), conforme link indicado no enunciado do teste.

Foram considerados os três trimestres mais recentes disponíveis no momento da análise, correspondentes ao ano de 2025.

---

## 2. Análise Inicial e Validações dos Dados

Durante a etapa de exploração da fonte, foi realizada uma validação inicial dos arquivos disponibilizados, incluindo:
- Identificação do formatação dos arquivos;
- Leitura do dicionário de dados oficial;
- Verificação das colunas efetivamente existentes.

Foi constatado que alguns campos mencionados no enunciado do tesete (como CNPJ, razão social e valore de despesas) não estão presentes nos arquivos fornecidos pela fonte oficial.

Essa ausência foi interpretada como **missing by design**, e não como erro de processamento.

---

## 3. Decisão Técnica diante da Inconsistência

Diante da inexistência dos campos citados no enunciado, optou-se por:
- Trabalhar exclusivamente com os dados efetivamente disponíveis nos arquivos patrimoniais;
- Garantir consistência estrutural, rastreabilidade e transparência na solução;
- Evitar inferências ou dados externos não fornecidos pela fonte oficial.

Essa decisão prioriza a integridade dos dados e a aderência à fonte pública original.

---

## 4. Processamento dos Arquivos

Os arquivos trimestrais foram processados utilizando Python e Pandas, seguindo as etapas:
1. Leitura automática dos arquivos CSV presentes na pasta `data/raw`;
2. Verificação da consistência estrutural das colunas entre os trimestres;
3. Consolidação dos dados em um único DataFrame;
4. Geração de um arquivo CSV base consolidado para uso nas estapas seguintes.

---

## 5. Trade-off Técnico: Processamento em Memória

Optou-se por processar os arquivos em memória, considerando:
- Volume de dados compatível com o ambiente local;
- Simplicidade e clareza do pipeline;
- Facilidade de leiturae manutenção do código para fins de teste técnico.

Essa decisão foi considerada adequada ao escopo do projeto e ao contexto de um teste de estágio.

---

## 6. Versionamento e Arquivos de Dados

Arquivos de grande volume (CSV consolidados e arquivos brutos) não foram versionados no repositório GitHub, respeitando as limitações da plataforma.

Esses arquivos são gerados automaticamente a partir dos scripts disponíveis no projeto, garantindo reprodutividade sem comprometer o versionamento.

---
