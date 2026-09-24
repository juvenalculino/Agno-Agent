from agno.models.groq import Groq
from agno.os import AgentOS
from agno.agent import Agent
# Vamos utilizar o tavily para pesquisas web
from agno.tools.tavily import TavilyTools
from agno.memory.manager import MemoryManager 
from agno.db.sqlite import SqliteDb

from dotenv import load_dotenv
load_dotenv()

agent_db = SqliteDb(
    db_file="tmp/agent_history.db",
    runs_table="agent_runs",
)


memory = MemoryManager(model=Groq(id="openai/gpt-oss-120b"),
                       db=agent_db,
                       )
# vamos criar um agent
agent = Agent(
    update_memory_on_run = True,
    memory_manager = memory,
    enable_agentic_memory = True,
    db=agent_db,
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[TavilyTools()],
    instructions="Você é um pesquisador, responda sempre chamando o usuário de senhor.",
    debug_mode=True,
    )

agent_os = AgentOS(db=agent_db, agents=[agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="18_memory:app", port=8000, reload=False)
