from agno.models.groq import Groq

from agno.agent import Agent
# Vamos utilizar o tavily para pesquisas web
from agno.tools.tavily import TavilyTools

from dotenv import load_dotenv
load_dotenv()

# vamos criar um agent
agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[TavilyTools()]
)

# rodando
agent.print_response("Use suas ferramentas para verificar a previsão do tempo para fátima bahia.")
