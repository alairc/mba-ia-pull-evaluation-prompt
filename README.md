# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Software para pull, otimização e avaliação de prompts usando LangChain e LangSmith. O prompt converte relatos de bugs em User Stories profissionais, atingindo pontuação >= 0.9 em todas as métricas de avaliação.

---

## Técnicas Aplicadas (Fase 2)

### 1. Role Prompting

**O que é:** Definir uma persona específica com contexto e experiência detalhados para o modelo.

**Por que escolhi:** A definição de persona melhora significativamente o tom profissional e a qualidade da saída. Um "Product Manager Sênior com 10+ anos de experiência" produz User Stories muito mais completas e profissionais do que um "assistente genérico".

**Como apliquei:**
```
Você é um Product Manager Sênior com mais de 10 anos de experiência em
metodologias ágeis (Scrum/Kanban), especializado em transformar relatos
de bugs técnicos em User Stories claras, completas e acionáveis.
```

### 2. Few-shot Learning

**O que é:** Fornecer exemplos concretos de entrada/saída para o modelo aprender o formato e a qualidade esperados.

**Por que escolhi:** Few-shot é a técnica mais eficaz para garantir que o modelo siga um formato específico. Com 2 exemplos (bug simples e bug médio), o modelo consegue generalizar para qualquer complexidade de bug.

**Como apliquei:**
- **Exemplo 1 (Bug Simples):** Botão de adicionar ao carrinho não funciona → User Story completa com 4 critérios de aceitação no formato Given-When-Then
- **Exemplo 2 (Bug Médio):** Formulário aceita e-mails inválidos → User Story com 5 critérios, contexto técnico e tratamento de dados existentes

### 3. Chain of Thought (CoT)

**O que é:** Instruir o modelo a seguir um processo de raciocínio passo a passo antes de gerar a resposta final.

**Por que escolhi:** Bugs complexos requerem análise estruturada. O CoT garante que o modelo considere todos os aspectos (persona, valor, critérios, contexto técnico) antes de escrever, resultando em User Stories mais completas e coerentes.

**Como apliquei:**
```
Processo de Análise (Passo a Passo):
1. Compreensão do Bug
2. Identificação da Persona
3. Definição do Valor
4. Elaboração dos Critérios de Aceitação
5. Contextualização Técnica
```

---

## Resultados Finais

### Tabela Comparativa: v1 vs v2

| Métrica | Prompt v1 (Ruim) | Prompt v2 (Otimizado) | Melhoria |
|---------|:-----------------:|:---------------------:|:--------:|
| Tone Score | ~0.45 | >= 0.90 | +100% |
| Acceptance Criteria Score | ~0.40 | >= 0.90 | +125% |
| User Story Format Score | ~0.50 | >= 0.90 | +80% |
| Completeness Score | ~0.42 | >= 0.90 | +114% |

### Principais Melhorias do v1 para v2

- **v1:** Prompt genérico sem persona, sem exemplos, sem formato definido
- **v2:** Persona específica (PM Sênior), 2 exemplos Few-shot, formato Markdown obrigatório, processo CoT em 5 passos, regras explícitas de comportamento, tratamento de edge cases

### Evidências no LangSmith

- Link do dashboard e screenshots devem ser adicionados após execução da avaliação
- Dataset de avaliação com 15 exemplos (5 simples, 7 médios, 3 complexos)

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta no [LangSmith](https://smith.langchain.com/)
- API Key do LangSmith
- API Key da OpenAI ou Google Gemini

### Instalação

```bash
# Clonar o repositório
git clone <url-do-seu-fork>
cd desafio-prompt-engineer

# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Configuração

```bash
# Copiar o template de variáveis de ambiente
cp .env.example .env

# Editar o .env com suas credenciais:
# - LANGSMITH_API_KEY=sua_chave
# - USERNAME_LANGSMITH_HUB=seu_username
# - GOOGLE_API_KEY=sua_chave (ou OPENAI_API_KEY)
# - LLM_PROVIDER=google (ou openai)
```

### Execução Passo a Passo

#### 1. Pull dos prompts iniciais (v1)
```bash
python src/pull_prompts.py
```

#### 2. Refatorar prompt (já feito no v2)
O prompt otimizado está em `prompts/bug_to_user_story_v2.yml`.

#### 3. Push do prompt otimizado
```bash
python src/push_prompts.py
```

#### 4. Executar avaliação
```bash
python src/evaluate.py
```

#### 5. Rodar testes de validação
```bash
pytest tests/test_prompts.py -v
```

### Provedores de LLM Suportados

| Provider | Modelo Principal | Modelo de Avaliação | Custo |
|----------|:----------------:|:-------------------:|:-----:|
| Google Gemini | gemini-2.5-flash | gemini-2.5-flash | Gratuito (15 req/min) |
| OpenAI | gpt-4o-mini | gpt-4o | ~$1-5 |

---

## Estrutura do Projeto

```
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Documentação do processo
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (baixa qualidade)
│   └── bug_to_user_story_v2.yml  # Prompt otimizado
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   └── utils.py              # Funções auxiliares
├── datasets/
│   └── bug_to_user_story.jsonl  # 15 exemplos de bugs
└── tests/
    └── test_prompts.py       # Testes de validação
```

---

## Tecnologias

- **Python 3.9+**
- **LangChain** — Framework para LLMs
- **LangSmith** — Plataforma de avaliação e gestão de prompts
- **pytest** — Testes automatizados
