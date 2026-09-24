from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.os.app import AgentOS
from fastapi import FastAPI
import uvicorn

import os
from dotenv import load_dotenv

load_dotenv()


# 2. Banco vetorial com nome de coleção alterado para "pdf_osint_e5" (evita o conflito de 1536 dimensões)
vectordb = ChromaDb(collection="pdf_agent", path="tmp/chroma_db", persistent_client=True,)

# 3. Base de conhecimento vinculada ao ChromaDB local
knowledge = Knowledge(vector_db=vectordb)

# 4. Histórico de sessão do agente via SQLite
db = SqliteDb(session_table="agent_sessions", db_file="tmp/agent_session.db")


# 5. Instanciação do Agente com modelo Groq
agent = Agent(
    id="agente_pdf",
    name="Agente OSINT",
    model=OpenAIChat(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    db=db,
    knowledge=knowledge,
    instructions=["Você deve chamar o usuário de senhor."],
    description="Agente especialista em extração e análise de inteligência de fontes abertas.",
    num_history_runs=3,
    search_knowledge=True,
    update_memory_on_run = True,
    debug_mode=True,
)

# AGENTOS ==================================================
agent_os = AgentOS(
    name="Agente OSINT PDF",
    agents=[agent],
    )


# RUN ======================================================
app = agent_os.get_app()

if __name__ == "__main__":
    knowledge.insert(
        url="https://artigo19.org/wp-content/blogs.dir/24/files/2023/09/DIGITAL_OSINT_20-09-2023_ARTIGO_19.pdf",
        reader=PDFReader(),
        skip_if_exists=True
    )
    agent_os.serve(app="exemplo_2:app", host='0.0.0.0' port=10000, reload=True)    

