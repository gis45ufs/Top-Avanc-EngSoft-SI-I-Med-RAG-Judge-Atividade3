import psycopg2
import pandas as pd
import warnings
from scipy.stats import spearmanr

# Oculta o aviso amarelo chato do Pandas
warnings.filterwarnings('ignore', category=UserWarning)

DB_CONFIG = {
    'dbname': 'poc_atividade1_grupo',
    'user': 'postgres',      
    'password': 'postgres', 
    'host': 'localhost',
    'port': '5432'
}

def calcular_spearman():
    conn = psycopg2.connect(**DB_CONFIG)
    
    # Query CORRIGIDA com o nome exato da sua coluna: id_resposta_ativa1
    query = """
    SELECT 
        r_antiga.id_pergunta,
        a_antiga.nota_atribuida AS nota_sem_rag,
        a_nova.nota_atribuida AS nota_com_rag
    FROM respostas_atividade_1 r_antiga
    JOIN avaliacoes_juiz a_antiga ON r_antiga.id_resposta = a_antiga.id_resposta_ativa1
    JOIN respostas_rag r_nova ON r_antiga.id_pergunta = r_nova.id_pergunta
    JOIN avaliacoes_juiz_rag a_nova ON r_nova.id_resposta_rag = a_nova.id_resposta_rag;
    """
    
    try:
        df = pd.read_sql_query(query, conn)
        print(f"Total de pares comparados: {len(df)}")
        
        correlacao, p_value = spearmanr(df['nota_sem_rag'], df['nota_com_rag'])
        
        media_sem = df['nota_sem_rag'].mean()
        media_com = df['nota_com_rag'].mean()
        
        print(f"Média de Nota (Sem RAG - Antiga): {media_sem:.2f}")
        print(f"Média de Nota (Com RAG - Atual): {media_com:.2f}")
        print(f"Correlação de Spearman (rho): {correlacao:.4f}")
        
        # Salva o CSV final
        df.to_csv("evolucao_spearman_rag.csv", index=False)
        print("\nArquivo 'evolucao_spearman_rag.csv' salvo com sucesso!")
        print("-> Agora é só jogar esse CSV no Lovable para o Dashboard!")
        
    except Exception as e:
        print(f"Erro na extração: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    calcular_spearman()