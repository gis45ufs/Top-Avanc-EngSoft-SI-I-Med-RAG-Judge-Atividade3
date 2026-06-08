import psycopg2
import json
import time  # <-- Adicionado para controlar o tempo e evitar quedas
from openai import OpenAI
from psycopg2.extras import DictCursor
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ============================================================================
# 1. CONFIGURAÇÕES (BANCO, API E RAG)
# ============================================================================
MISTRAL_API_KEY = "TEqiet2Fs00bvKfLCirE5KxQiPjrpWoJ" # A sua chave da Mistral

client = OpenAI(base_url="https://api.mistral.ai/v1", api_key=MISTRAL_API_KEY)
MODELO_API = 'mistral-small-latest'

DB_CONFIG = {
    'dbname': 'poc_atividade1_grupo',
    'user': 'postgres',      
    'password': 'postgres', 
    'host': 'localhost',
    'port': '5432'
}

print("\n[Inicialização] Conectando ao Banco Vetorial ChromaDB...")
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db_rag = Chroma(persist_directory="./chroma_db_medico", embedding_function=embeddings_model)
print("[Inicialização] ChromaDB Pronto e carregado!")

# ============================================================================
# 2. FUNÇÕES DE IA COM BLINDAGEM CONTRA QUEDAS DA API (RETRY)
# ============================================================================
def gerar_resposta_com_rag(pergunta, contexto):
    prompt = f"""Você é um médico especialista. Use APENAS o contexto atualizado abaixo para responder à pergunta.
    CONTEXTO DO PDF (2024/2025): {contexto}
    PERGUNTA: {pergunta}
    """
    for tentativa in range(3): # Tenta 3 vezes antes de desistir
        try:
            response = client.chat.completions.create(
                model=MODELO_API,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"      [Aviso] API engasgou (Gerador). Tentando novamente em 5s... (Tentativa {tentativa+1}/3)")
            time.sleep(5)
    raise Exception("A API da Mistral caiu definitivamente.")

def juiz_avalia_rag(pergunta, resposta_ouro, resposta_rag, contexto):
    system_prompt = """Você é um Juiz Médico avaliando o impacto do RAG (Recuperação de Informação).
    Compare a 'Resposta RAG' com a 'Resposta Ouro'.
    
    CRITÉRIOS (1 a 5):
    5 = Perfeita / 1 = Incorreta.
    
    No seu 'chain_of_thought', você DEVE analisar explicitamente se o Contexto Fornecido ajudou a IA a evitar uma alucinação ou se trouxe ruído.
    Retorne APENAS um JSON válido: {"nota": <nota>, "chain_of_thought": "<justificativa>"}
    """
    user_prompt = f"CONTEXTO RECUPERADO:\n{contexto}\n\nPERGUNTA:\n{pergunta}\n\nRESPOSTA OURO:\n{resposta_ouro}\n\nRESPOSTA RAG:\n{resposta_rag}"
    
    for tentativa in range(3):
        try:
            response = client.chat.completions.create(
                model=MODELO_API,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            resultado = json.loads(response.choices[0].message.content)
            return resultado['nota'], resultado['chain_of_thought']
        except Exception as e:
            print(f"      [Aviso] API engasgou (Juiz). Tentando novamente em 5s... (Tentativa {tentativa+1}/3)")
            time.sleep(5)
    raise Exception("A API da Mistral caiu definitivamente.")

# ============================================================================
# 3. MOTOR PRINCIPAL - CARGA TOTAL
# ============================================================================
def rodar_pipeline():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor(cursor_factory=DictCursor)

    try:
        # Puxa TODAS as perguntas do banco
        cur.execute("SELECT id_pergunta, enunciado, resposta_ouro FROM perguntas ORDER BY id_pergunta ASC;")
        todas_perguntas = cur.fetchall()
        total = len(todas_perguntas)

        # Descobre quais perguntas já foram feitas para não duplicar
        cur.execute("SELECT id_pergunta FROM respostas_rag;")
        perguntas_concluidas = set([row['id_pergunta'] for row in cur.fetchall()])

        for idx, p in enumerate(todas_perguntas, 1):
            id_pergunta = p['id_pergunta']
            
            # Lógica de pulo (Pula as 15 que você já fez)
            if id_pergunta in perguntas_concluidas:
                print(f"\n[{idx}/{total}] Pergunta ID {id_pergunta} já processada. Pulando...")
                continue

            print(f"\n[{idx}/{total}] Processando Pergunta ID {id_pergunta}...")
            
            # Passo A: Buscar no ChromaDB
            docs = db_rag.similarity_search(p['enunciado'], k=2)
            contexto_recuperado = "\n".join([doc.page_content for doc in docs])
            
            # Passo B: Gerar Nova Resposta com a IA
            print(" -> Gerando nova resposta baseada no PDF...")
            nova_resposta = gerar_resposta_com_rag(p['enunciado'], contexto_recuperado)
            
            # Salvar no Banco
            cur.execute("""
                INSERT INTO respostas_rag (id_pergunta, id_modelo, texto_resposta_com_rag, contexto_recuperado) 
                VALUES (%s, 999, %s, %s) RETURNING id_resposta_rag;
            """, (id_pergunta, nova_resposta, contexto_recuperado))
            id_resp_rag = cur.fetchone()[0]
            
            # Passo C: Juiz Avalia o Impacto
            print(" -> Juiz avaliando impacto fático...")
            nota, cot = juiz_avalia_rag(p['enunciado'], p['resposta_ouro'], nova_resposta, contexto_recuperado)
            
            cur.execute("""
                INSERT INTO avaliacoes_juiz_rag (id_resposta_rag, id_modelo_juiz, nota_atribuida, cot_impacto_rag)
                VALUES (%s, 999, %s, %s);
            """, (id_resp_rag, nota, cot))
            
            conn.commit()
            print(f" -> SUCESSO! Nota do Juiz: {nota}")
            
            # Pausa de 2 segundos para não tomar bloqueio da Mistral
            time.sleep(2)
            
    except Exception as e:
        print(f"\n[ERRO FATAL] Algo falhou na base de dados ou na API: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("\nPipeline finalizado. Fechando conexão.")

if __name__ == "__main__":
    rodar_pipeline()