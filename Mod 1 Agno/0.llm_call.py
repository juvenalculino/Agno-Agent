#from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.agent import Agent

from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model=Groq(id="openai/gpt-oss-120b")
)

agent.print_response("Olá, tudo bem?")