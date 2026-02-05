# Explicações Técnicas — Teste 1 do Estágio IntuitiveCare

Este documento descreve, de forma objetiva, as decisões técnicas adotadas na etapa do **Teste 1** do processo seletivo de Estágio na IntuitiveCare (2026).

---

## Fonte dos Dados

Os dados utilizados são provenientes das **Demonstrações Contábeis** disponibilizadas publicamente pela ANS (Agência Nacional de Saúde Suplementar), conforme o link indicado no enunciado do teste.

Foram considerados os **três trimestres mais recentes** disponíveis no momento da análise, correspondentes ao ano de 2025.

---

## Análise Inicial da Fonte de Dados

Durante a exploração dos arquivos disponibilizados pela ANS, foi realizada uma análise inicial da estrutura dos dados, incluindo:  

- Identificação do formato dos arquivos;  
- Consulta ao dicionário de dados oficial;  
- Verificação das colunas efetivamente presentes nos arquivos trimestrais.

Foi identificado que alguns campos exigidos nas etapas posteriores do teste (**CNPJ, Razão Social, Trimestre, Ano, Valor de Despesas**) **não estão explicitamente presentes** nos arquivos originais.  
Essa característica foi tratada como uma **limitação da fonte**, não como erro de processamento.

---

## Decisão Técnica: Padronização Estrutural dos Dados

Para lidar com a ausência de alguns campos, optou-se por **padronizar o dataset consolidado**, criando explicitamente todas as colunas requeridas pelo teste, mesmo quando os dados não estavam disponíveis.  

**Estratégia adotada:**  

- Criar as colunas: `cnpj`, `razao_social`, `trimestre`, `ano` e `valor_despesas`;  
- Preencher com `null` os campos sem informação na fonte original;  
- Preservar todos os dados originais existentes sem inferências externas.

**Justificativa:**  

- Facilita a aplicação das etapas seguintes (**validação, enriquecimento e agregação**);  
- Garante que joins e regras de negócio não quebrem mesmo com dados faltantes;  
- Mantém o pipeline previsível, extensível e aderente às especificações do teste.

---

## Processamento dos Arquivos

Os arquivos trimestrais foram processados com **Python** e **Pandas**, seguindo estas etapas:  

1. Leitura automática dos arquivos CSV em `data/raw`;  
2. Verificação da consistência das colunas entre os trimestres;  
3. Consolidação em um único DataFrame;  
4. Geração de um CSV consolidado para uso nas etapas seguintes.  

**Observação:**  

- Campos faltantes foram preenchidos com `null` para manter consistência;  
- O arquivo consolidado é compactado em ZIP para entrega, conforme solicitado.

---

## Trade-off Técnico: Processamento em Memória

O processamento foi realizado **em memória**, por motivos de:  

- Volume de dados compatível com a execução local;  
- Simplicidade e clareza do pipeline;  
- Facilidade de manutenção e entendimento do código, adequado ao contexto de teste para estágio.

**Alternativa:** utilizar chunking ou banco de dados, mas foi descartada por não ser necessária neste cenário.

---

## Versionamento e Arquivos de Dados

Arquivos de grande volume, como CSVs consolidados e arquivos brutos, **não foram adicionados ao repositório GitHub**.  
Essa decisão segue boas práticas de versionamento e evita ultrapassar limites da plataforma (arquivos maiores que 100 MB).  

Esses arquivos são **gerados automaticamente** a partir dos scripts disponíveis no projeto, garantindo que qualquer pessoa consiga reproduzir os dados sem precisar subir arquivos pesados.  

> **Justificativa:** Essa abordagem mantém o repositório limpo e funcional, permitindo versionamento apenas do código e documentação, enquanto os dados podem ser recriados conforme necessário.
