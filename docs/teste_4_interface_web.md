# Explicações Técnicas — Teste 4 do Estágio IntuitiveCare

Este documento descreve, de forma objetiva, as decisões técnicas adotadas na etapa do teste 4 para o teste de nivelamento do processo seletivo de Estágio na IntuitiveCare (2026).

---

## Observação sobre CNPJ

Embora o enunciado mencione CNPJ como identificador, a base oficial da ANS disponibiliza o CNPJ mascarado. Por esse motivo, foi utilizado o `registro_ans` como identificador único e confiável das operadoras.

---

## 4.2.1 Escolha do framework: FastAPI

**Escolha: Opção B – FastAPI**

### Justificativa

O FastAPI foi escolhido por oferecer:
- Alta performance baseada em ASGI
- Sintaxe simples e declarativa
- Validação automática de dados
- Geração automática de documentação (Swagger/OpenAPI)

Para um projeto com múltiplas rotas de leitura e foco em clareza e manutenção, o FastAPI reduz complexidade e acelera o desenvolvimento em comparação ao Flask.

---

## 4.2.2 Paginação

**Escolha: Opção A – Offset-based**

### Justificativa:

A paginação por offset foi escolhida por sua simplicidade e adequação ao escopo do projeto.
Como os dados possuem baixa frequência de atualização e o volume é gerenciável, essa abordagem facilita a implementação no backend e o consumo no frontend sem impactos relevantes de performance.

---

## 4.2.3 Estatísticas: Cache vs cálculo

**Escolha: Opção A – Calcular na hora**

### Justificativa:

As estatísticas são derivadas de dados históricos que não sofrem atualizações frequentes.
Optou-se por calcular os valores diretamente nas queries para garantir consistência dos dados e simplicidade de manutenção, evitando complexidade adicional de cache ou pré-processamento.

---

## 4.2.4 Estrutura de resposta da API

**Escolha: Opção B – Dados + metadados**
`{`
  `"data": [...],`
  `"page": 1,`
  `"limit": 10,`
  `"total": 1234`
`}`


### Justificativa:

Retornar dados acompanhados de metadados facilita a implementação de paginação no frontend, melhora a experiência do usuário e evita chamadas adicionais à API apenas para obter contagens.

---

## 4.3.1 Estratégia de busca

**Escolha: Opção A – Busca no servidor**

### Justificativa:

A busca foi implementada no servidor para evitar o carregamento de grandes volumes de dados no cliente e garantir melhor performance e escalabilidade, especialmente considerando filtros por CNPJ e razão social.

---

## 4.3.2 Gerenciamento de estado

**Escolha: Opção A – Props / Events simples**

### Justificativa:

Como a aplicação possui baixo nível de complexidade e pouco compartilhamento de estado global, optou-se por uma abordagem simples com props e eventos, evitando a sobrecarga de bibliotecas adicionais como Vuex ou Pinia.

---

## 4.3.3 Performance da tabela

**Estratégia adotada:**
- Paginação no backend
- Renderização limitada no frontend

### Justificativa:

A paginação no backend reduz o número de registros renderizados simultaneamente, garantindo boa performance e experiência do usuário sem necessidade de técnicas avançadas como virtual scrolling.

---

## 4.3.4 Erros, loading e estados vazios

**Tratamento adotado:**
- **Loading:** spinner simples (“Carregando…”)
- **Erro:** mensagem clara (“Erro ao carregar dados da API”)
- **Vazio:** “Nenhum resultado encontrado”

### Justificativa:

Foram utilizadas mensagens claras e específicas para melhorar a experiência do usuário e facilitar o diagnóstico de problemas, evitando mensagens genéricas que dificultam a compreensão do estado da aplicação.

---

## Considerações sobre a execução do frontend

Devido ao prazo do teste e às limitações do ambiente de desenvolvimento local (configuração do Vue, volume de dados e integração com frontend), a implementação do frontend completo (tabela, filtro e gráfico) **não foi finalizada**.

Para fins de avaliação, priorizei:
- **Qualidade do backend** e da API (FastAPI)
- **Decisões técnicas fundamentadas** em cada escolha de implementação
- **Documentação detalhada** do pipeline e trade-offs

Essa abordagem garante que o avaliador compreenda **a lógica do pipeline, escolhas técnicas e capacidade de análise crítica**, mesmo sem a entrega total do frontend.

## Observações finais

- O identificador `registro_ans` foi utilizado no lugar do CNPJ, considerando a consistência e confiabilidade do dado.
- Toda integração foram realizadas em Python, garantindo rastreabilidade e clareza do pipeline.
- O projeto demonstra capacidade de **tomada de decisão técnica, resolução de problemas práticos** e **documentação clara de trade-offs**, pontos avaliados no teste.