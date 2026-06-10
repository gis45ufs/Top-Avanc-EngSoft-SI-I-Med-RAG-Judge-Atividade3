import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ============================================================================
# 1. CONFIGURAÇÕES DA ARQUITETURA RAG
# ============================================================================
DIRETORIO_PDFS = "./pdfs_medicos"
DIRETORIO_CHROMA = "./chroma_db_medico"

def construir_banco_vetorial():
    print("1. Lendo os PDFs médicos recentes...")
    loader = PyPDFDirectoryLoader(DIRETORIO_PDFS)
    documentos = loader.load()
    
    if not documentos:
        print("Nenhum PDF encontrado na pasta! Coloque os arquivos lá primeiro.")
        return None

    print(f"2. Quebrando {len(documentos)} páginas em chunks textuais...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"   -> Foram gerados {len(chunks)} fragmentos de conhecimento.")

    print("3. Gerando Embeddings e salvando no ChromaDB...")
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    db = Chroma.from_documents(
        chunks, 
        embeddings_model, 
        persist_directory=DIRETORIO_CHROMA
    )
    
    print("Banco Vetorial RAG criado com sucesso! Pronto para consultas.")
    return db

if __name__ == "__main__":
    if not os.path.exists(DIRETORIO_CHROMA):
        db = construir_banco_vetorial()
    else:
        print("Banco ChromaDB já existe. Pronto para inferência!")