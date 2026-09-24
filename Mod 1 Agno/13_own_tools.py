from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from agno.agent import Agent
# Vamos utilizar o tavily para pesquisas web
from agno.tools.tavily import TavilyTools
from agno.os import AgentOS

from dotenv import load_dotenv
load_dotenv()

db = SqliteDb(db_file="tmp/agent_history.db")

def celsius_to_fh(temperatura_celsius: float):
    """
    Converte uma temperatura de Celsius para Fahrenheit.
    Args:
        temperatura_celsius (float): Temperatura em graus Celsius.
    Returns:
        float: Temperatura convertida em graus Fahrenheit.

    """
    temperatura_fahrenheit = (temperatura_celsius * 9/5) + 32
    return temperatura_fahrenheit


# vamos criar um agent
workbench = Agent(
    db=db,
    name="workbench",
    add_history_to_context=True,
    num_history_runs=5,
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[TavilyTools(), 
           celsius_to_fh,
           ],
    
)

agent_os = AgentOS(agents=[workbench],)

app = agent_os.get_app()

# rodando
#agent.print_response("Qual a temperatura atual do município de fátima em fahrenheit?")

if __name__ == "__main__":
    agent_os.serve(app="13_own_tools:app", port=8000, reload=True)