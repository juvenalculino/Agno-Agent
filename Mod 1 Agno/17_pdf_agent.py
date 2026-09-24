import os
from agno.agent import Agent
from agno.os import AgentOS
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from dotenv import load_dotenv

load_dotenv()

DB_DIR = "tmp"
CHROMA_DIR = os.path.join(DB_DIR, "chroma_db")
SQLITE_PATH = os.path.join(DB_DIR, "agent_history.db")
DOCUMENTS_DIR = "documentos"

# 1. Configura o Embedder local gratuito
local_embedder = SentenceTransformerEmbedder(id="sentence-transformers/all-MiniLM-L6-v2")

# 2. Configura o banco vetorial Chroma
vectordb = ChromaDb(
    collection="recipes",
    path=CHROMA_DIR,
    embedder=local_embedder
    )

# 3. Inicializa a base de conhecimento
knowledge = Knowledge(vector_db=vectordb)

# 4. Configura o armazenamento do histórico do agente
agent_storage = SqliteDb(
    runs_table="agent_history",
    db_file=SQLITE_PATH,
    )

# 5. Inicializa o Agente mantendo o modelo original intocado
agent = Agent(
        name="Agente de PDF",
        model=Groq(id="openai/gpt-oss-120b"),
        db=agent_storage,
        add_history_to_context=True,
        num_history_runs=5,
        knowledge=knowledge,
        search_knowledge=True,

        debug_mode=True,
        description="Você é um especialista em extrair e analisar informações de documentos e relatórios.",
        instructions=[
        "Você possui acesso aos documentos PDF indexados na pasta 'documentos'.",
        "Se o usuário perguntar quais arquivos/documentos estão disponíveis, informe que os PDFs da pasta 'documentos' foram indexados.",
        "Para responder dúvidas sobre o conteúdo do documento, use a ferramenta 'search_knowledge_base' pesquisando sempre por conceitos, tópicos e palavras-chave relevantes.",
        "PROIBIDO: Nunca use o nome do arquivo (ex: '49414.pdf') ou expressões genéricas como 'arquivos disponíveis' como termo de busca na ferramenta 'search_knowledge_base', pois o banco busca apenas o conteúdo textual interno do documento."
        ]
    )



agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

def setup_knowledge_base():
    """Retorna todos os PDFs encontrados na pasta de documentos."""
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    pdf_paths = []
    for root, _, filenames in os.walk(DOCUMENTS_DIR):
        pdf_paths.extend(
            os.path.join(root, filename)
            for filename in filenames
            if filename.lower().endswith(".pdf")
        )

    if not pdf_paths:
        raise FileNotFoundError(
            f"Nenhum arquivo PDF foi encontrado na pasta '{DOCUMENTS_DIR}'."
        )
    return sorted(pdf_paths)

print("Verificando os arquivos PDF no ChromaDB local...")
for pdf_path in setup_knowledge_base():
    document_name = os.path.relpath(pdf_path, DOCUMENTS_DIR)
    knowledge.insert(
        name=document_name,
        path=pdf_path,
        reader=PDFReader(chunk_size=500),
        skip_if_exists=True,
    )
print("Documentos PDF disponíveis no ChromaDB local!")

if __name__ == "__main__":
    os.makedirs(DB_DIR, exist_ok=True)

    # Inicia o servidor Agno OS
    # Definição de reload=False para evitar que reinicializações limpem/corrompam a sessão do ChromaDB
    agent_os.serve(app="17_pdf_agent:app", port=8000, reload=False)