import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.reader.pdf_reader import PDFReader
from fastapi import FastAPI
import uvicorn

load_dotenv()


# 2. Banco vetorial com nome de coleção alterado para "pdf_osint_e5" (evita o conflito de 1536 dimensões)
vectordb = ChromaDb(
    collection="pdf_agent", 
    path="tmp/chroma_db", 
    persistent_client=True, 
)

# 3. Base de conhecimento vinculada ao ChromaDB local
knowledge = Knowledge(vector_db=vectordb)

def setup_knowledge():
    """Lê o PDF diretamente da URL e armazena os embeddings no banco vetorial local."""
    pdf_url = "https://artigo19.org/wp-content/blogs.dir/24/files/2023/09/DIGITAL_OSINT_20-09-2023_ARTIGO_19.pdf"
    print("Verificando e indexando documento na base de conhecimento...")
    
    # PDFUrlReader faz o download e extração dos trechos de forma otimizada para URLs
    knowledge.insert(
        url=pdf_url,
        reader=PDFReader(),
        skip_if_exists=True
    )
    print("Base de conhecimento pronta para consultas!")

# 4. Histórico de sessão do agente via SQLite
db = SqliteDb(
    session_table="agent_sessions", 
    db_file="tmp/agent_session.db"
)

# 5. Instanciação do Agente com modelo Groq
agent = Agent(
    name="Agente OSINT",
    model=OpenAIChat(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    db=db,
    instructions=[
        "Você é um especialista em OSINT (Open Source Intelligence) focado em análise de documentos."
    ],
    description="Agente especialista em extração e análise de inteligência de fontes abertas.",    
    num_history_runs=3,
    knowledge=knowledge,
    search_knowledge=True,
    debug_mode=True,
)

app = FastAPI(title="Agente OSINT PDF", description="API para interagir com o Agente OSINT especializado em PDFs.")

@app.post("/agente_pdf")
async def agente_pdf(pergunta: str):
    """Endpoint para interagir com o agente OSINT via POST request."""
    response = agent.run(pergunta, markdown=True)
    message = response.messages[-1]
    return {"message": message.content}


if __name__ == "__main__":
    # Garante que a pasta temporária de banco exista
    os.makedirs("tmp", exist_ok=True)

    # Realiza a indexação do PDF (se ainda não tiver sido feita)
    setup_knowledge()
    uvicorn.run("exemplo_1:app", host="0.0.0.0", port=8000)