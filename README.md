# Atividade 3: RAG e Resolução Temporal em Domínio Médico

**Instituição:** Universidade Federal de Sergipe (UFS) - Pós-Graduação em Ciência da Computação  
**Disciplina:** Tópicos Especiais em Engenharia de Software e SI I  
**Equipe 2:** Gilson Inácio da Silva, Carlos Eduardo de Melo Pereira dos Anjos, Ian Sandes Alves, Caio Vasconcelos Silva Andrade, Gabriella de Jesus Santos.  
**Domínio:** Médico (Datasets M1: K-QA e M2: USMLE)  

🎥 **Vídeo Demonstrativo da Equipe:** [COLOQUE_O_LINK_DO_YOUTUBE_AQUI]
📄 **Tutorial/Relatório em PDF:** [Disponível neste repositório]

## 🎯 Objetivo
Solucionar a "cegueira temporal" (knowledge cutoff) de Modelos de Linguagem de Grande Escala, utilizando o método de Geração Aumentada por Recuperação (RAG). Comparamos o baseline de Modelos Crús treinados até 2023 (Média 2.43) com o pipeline RAG municiado por literatura médica do Estado da Arte de 2024/2025.

## 🛠️ Arquitetura e Tecnologias
* **Vetorização/Embbedding:** ChromaDB e LangChain (Local)
* **LLM Gerador e Juiz:** Mistral API 
* **Banco de Dados:** PostgreSQL (Tabelas lado-a-lado preservando a versão histórica)
* **Documentação Injetada:** Relatório FDA (Novas Drogas 2025) e Diretrizes AHA (2024).

## 📊 Resultados e Estatística (LLM-as-a-Judge)
Foram cruzados **16.596 pares** (nova resposta RAG vs respostas dos 4 modelos antigos).
* **Média Base (Sem RAG):** 2.43 
* **Média RAG (Mistral):** 3.46 (Melhoria Absoluta de +42.3%)
* **Correlação de Spearman ($\\rho$):** 0.1377 (Comprova ruptura com o histórico de falhas)
* **Análise de Ruído:** Foi diagnosticada falha vetorial ou ruído semântico em 17.15% dos casos, documentados no log do Juiz.

## 🗂️ Estrutura de Arquivos da Entrega
* `motor_rag.py`: Script de persistência do vetor (Chunking e ChromaDB).
* `pipeline_rag.py`: Roteamento LLM e geração baseada em recuperação semântica.
* `calcular_evolucao_rag.py`: Estatística matemática (Spearman) cruzando bases do banco.
* `backup_atividade_3.sql`: Dump estruturado obrigatório refletindo antes e depois.
* `evolucao_spearman_rag.csv`: Base analítica pura dos 16.596 pares extraídos.

## 🚀 Como Executar
1. Clone o repositório localmente.
2. Restaure o banco relacional via PGAdmin usando o `backup_atividade_3.sql`.
3. Adicione sua própria `API_KEY` da Mistral no código `motor_rag.py`.
4. Instale as bibliotecas (`pip install langchain chromadb psycopg2 scipy pandas`).
5. Execute os scripts em ordem para gerar vetores e submeter ao juiz.
