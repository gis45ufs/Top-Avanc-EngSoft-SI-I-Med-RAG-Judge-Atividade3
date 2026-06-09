# 🩺 RAG-Judge: Resolução Temporal em Domínio Médico

[![Status: Concluído](https://img.shields.io/badge/Status-Concluído-brightgreen.svg)]()
[![Tecnologia: Mistral AI](https://img.shields.io/badge/LLM-Mistral-blue.svg)]()

> **Projeto Final - Atividade 3**
> **Disciplina:** Tópicos Especiais em Engenharia de Software e SI I
> **Instituição:** Universidade Federal de Sergipe (UFS) - Pós-Graduação em Ciência da Computação

---

# 👥 Equipe

* **Gilson Inácio da Silva**

---

# 🌐 Dashboard Analítico

🔗 **Dashboard Interativo da Atividade 3:**
https://rag-analytics-ufs-atividade3.vercel.app/

---

# 🔗 Atividades Relacionadas

## 📘 Atividade 1

🔗 Repositório GitHub:
https://github.com/gis45ufs/Top-Avanc-EngSoft-SI-I-26-1-Gilson-Inacio-Silva-Med-Ativ1

## 📙 Atividade 2

🔗 Repositório GitHub:
https://github.com/gis45ufs/Top-Avanc-EngSoft-SI-I-26-1-Gilson-Silva-Med-Ativ2

---

# 🔗 Links e Documentação

## 🎥 Vídeo Demonstrativo

[Acessar vídeo da apresentação](COLOQUE_AQUI_O_LINK_DO_YOUTUBE)

## 📄 Relatório Final

[Ver relatório (PDF)](./Atividade_3/Relatorio_Atividade_3.pdf)

---

# 🎯 Objetivo do Projeto

Solucionar a **"cegueira temporal" (knowledge cutoff)** de Modelos de Linguagem utilizando a técnica de **Retrieval-Augmented Generation (RAG)**.

O sistema compara o *baseline* de modelos treinados até 2023 com um pipeline RAG alimentado por literatura médica atualizada (**Diretrizes AHA 2024 e FDA 2025**), garantindo respostas clínicas baseadas em evidências recentes.

---

# 🧠 Arquitetura do Sistema

O pipeline integra quatro componentes principais:

## 1. Ingestão de Dados

* PDFs médicos convertidos em embeddings vetoriais utilizando `ChromaDB`.

## 2. Recuperação Semântica

* Busca contextual baseada em similaridade usando `LangChain`.

## 3. Geração de Resposta

* Utilização da API da `Mistral AI` para síntese clínica.

## 4. Juiz (LLM-as-a-Judge)

* Agente avaliador baseado em *Chain-of-Thought* responsável por comparar:

  * Resposta Base
  * Resposta RAG
  * Resposta Ouro

---

# 📊 Resultados Alcançados

A introdução do RAG elevou significativamente a acurácia do sistema, superando limitações de modelos estáticos.

| Métrica                        | Resultado    |
| ------------------------------ | ------------ |
| **Média Base (Sem RAG)**       | 2.43         |
| **Média RAG (Mistral)**        | **3.46**     |
| **Ganho Absoluto**             | **+42.3%**   |
| **Correlação de Spearman (ρ)** | 0.1377       |
| **Casos Avaliados**            | 16.596 pares |
| **Ruído Semântico Detectado**  | 17.15%       |

---

# 🚀 Guia de Execução

## 1. Pré-requisitos

* Python 3.10+
* PostgreSQL instalado
* pgAdmin instalado
* API Key válida da Mistral AI

---

## 2. Clone do Repositório

```bash id="6k39l4"
git clone https://github.com/gis45ufs/Top-Avanc-EngSoft-SI-I-Med-RAG-Judge-Atividade3.git

cd Top-Avanc-EngSoft-SI-I-Med-RAG-Judge-Atividade3
```

---

## 3. Criação do Ambiente Virtual

### Windows

```bash id="9kw9zw"
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash id="q8zt8k"
python3 -m venv venv

source venv/bin/activate
```

---

## 4. Instalação das Dependências

```bash id="4gdbb7"
pip install langchain
pip install langchain-community
pip install chromadb
pip install psycopg2-binary
pip install scipy
pip install pandas
pip install openai
```

Ou utilize:

```bash id="xh7x0x"
pip install -r requirements.txt
```

---

# 🗄️ Configuração do Banco de Dados

1. Abra o **pgAdmin**.

2. Crie um novo banco chamado:

```text id="o5vzxp"
poc_atividade1_grupo
```

3. O usuário e senha padrão utilizados no código são:

```text id="ls4i1v"
Usuário: postgres
Senha: postgres
```

4. Clique com o botão direito no banco criado:

```text id="2x0c4q"
Restore...
```

5. Selecione o arquivo:

```text id="k4d13p"
backup_atividade_3.sql
```

localizado na pasta:

```text id="61x31e"
Atividade_3/
```

6. Execute a restauração do banco.

---

# 🔑 Configuração da API

Abra o arquivo:

```text id="zkpygk"
Atividade_3/pipeline_rag.py
```

Localize a variável:

```python id="x2b57u"
MISTRAL_API_KEY
```

Substitua pelo valor da sua chave válida da Mistral AI.

Exemplo:

```python id="a8o9yw"
MISTRAL_API_KEY = "sua_chave_aqui"
```

---

# ▶️ Execução do Projeto

Após configurar a API Key, execute:

## Pipeline Principal (RAG + Juiz)

```bash id="c4utfx"
python Atividade_3/pipeline_rag.py
```

## Análise Estatística

```bash id="yhn4yc"
python Atividade_3/calcular_evolucao_rag.py
```

---

# 📂 Estrutura de Artefatos

```text id="9f4t6u"
Atividade_3/
│
├── pdfs_medicos/
├── Relatorio_Atividade_3.pdf
├── backup_atividade_3.sql
├── calcular_evolucao_rag.py
├── evolucao_spearman_rag.csv
├── motor_rag.py
├── pipeline_rag.py
├── prompts_de_sistema.md
└── README.md
```

---

# 📁 Descrição dos Arquivos

| Arquivo                     | Função                               |
| --------------------------- | ------------------------------------ |
| `motor_rag.py`              | Persistência vetorial e ChromaDB     |
| `pipeline_rag.py`           | Orquestração do pipeline RAG         |
| `calcular_evolucao_rag.py`  | Estatística e Correlação de Spearman |
| `backup_atividade_3.sql`    | Dump da base PostgreSQL              |
| `prompts_de_sistema.md`     | Engenharia de prompts                |
| `evolucao_spearman_rag.csv` | Base analítica dos experimentos      |

---

# 🔬 Tecnologias Utilizadas

* Python
* PostgreSQL
* pgAdmin
* LangChain
* ChromaDB
* Mistral AI
* Pandas
* SciPy
* OpenAI API
* Embeddings Vetoriais
* Retrieval-Augmented Generation (RAG)

---

# 📈 Contribuições Científicas

O projeto demonstra empiricamente que pipelines RAG podem:

* Reduzir limitações temporais de LLMs
* Melhorar acurácia clínica
* Diminuir desatualização semântica
* Aumentar aderência a guidelines médicas recentes
* Possibilitar avaliação automatizada via LLM-as-a-Judge

---

# 📜 Licença

Projeto desenvolvido exclusivamente para fins acadêmicos na disciplina:

**Tópicos Especiais em Engenharia de Software e SI I**
**Universidade Federal de Sergipe (UFS)**

---
