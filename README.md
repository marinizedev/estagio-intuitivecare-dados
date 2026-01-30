# Estágio IntuitiveCare 2026 — Projeto de Dados
Este repositório contém a solução para o **teste técnico de nivelamento** do processo seletivo de **Estágio na IntuitiveCare (2026)**.

O objetivo do projeto é demonstrar conhecimentos fundamentais em **manipulação de dados, organização de pipelines, boas práticas de desenvolvimento e capacidade analítica**, conforme as orientações fornecidas no enunciado oficial do teste.

---

## Objetivo do Projeto
Desenvolver uma solução de dados a partir de fontes públicas, contemplando etapas de **extração, tratamento, consolidação, consultas e visualização**, conforme os requisitos do teste técnico proposto pela IntuitiveCare.

O projeto tem como foco a construção de um pipeline de dados **claro, reproduzível, organizado e bem documentado**, priorizando qualidade técnica e transparência nas decisões adotadas.

---

## Contexto dos Dados
Os dados utilizados neste projeto são provenientes das **Demonstrações Contábeis** disponibilizadas publicamente pela **ANS (Agência Nacional de Saúde Suplementar)**.

Durante a análise da fonte oficial, foi identificado que alguns campos citados no enunciado do teste (como **CNPJ, razão social e despesas**) **não estão disponíveis nos arquivos fornecidos**. Dessa forma, as decisões técnicas foram adaptadas para utilizar exclusivamente os dados efetivamente existentes, garantindo **consistência, rastreabilidade, transparência e clareza** ao longo da solução.

Foram considerados os **três trimestres mais recentes disponíveis na fonte**, correspondentes ao ano de **2025**.

---

## Visão Geral da Solução
A solução foi estruturada em etapas, seguindo boas práticas de projetos de dados:

1. Leitura e extração dos arquivos trimestrais das Demonstrações Contábeis;
2. Validação da estrutura e integridade dos dados;
3. Consolidação dos dados em um **arquivo CSV base**;
4. Transformações adicionais para geração de um **CSV final**, conforme solicitado no teste;
5. Criação de consultas e agregações utilizando **SQL**;
6. Implementação de camadas adicionais (back-end e front-end) para exposição e análise dos dados;
7. Documentação das decisões técnicas adotadas ao longo do processo.

---

## Tecnologias Utilizadas
- Python
- Pandas
- CSV
- SQL
- MySQL (ou outro banco relacional, conforme aplicação)
- Git / GitHub

---

## Estruturas do Repositório

- /estagio-intuitivecare-dados/
- |
- |---- data/
    - |---- raw/     # arquivos originais (ou links)
    - |---- processed/      # CSV base e CSV final
- |
- |---- scripts/
    - |---- extracao/    # Teste 1
    - |---- transform/   # Teste 2
- |
- |---- sql/
    - |---- consultas.sql
- |
- |---- docs/
    - |---- explicacoes_tecnicas.md
- |---- README.md

---

## Observações
Este projeto prioriza **clareza, organização, coerência técnica e justificativa das decisões**, evitando complexidade desnecessária e mantendo  alinhamento com o escopo e os objetivos do processo seletivo.

Todas as etapsa foram desenvolvidas com foco em **reprodutibilidade, legibilidade e boas práticas**, refletindo o processo de aprendizado e aplicação prática dos conhecimentos adquiridos.

## Autora
Projeto desenvolvido por **Marinize Santana**, como parte do teste técnico de nivelamento do processo seletivo de **Estágio na IntuitiveCare (2026)**.

Este repositório reflete o processo de aprendizado, análise e aplicação prática de conceitos de dados, com foco em organização, clareza e boas práticas.
