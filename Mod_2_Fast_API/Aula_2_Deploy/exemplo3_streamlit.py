# 1 - Imports =================================
import requests
import json
import os
from pprint import pprint


AGENT_ID = 'agente_pdf'  # ID do agente que você deseja consultar
ENDPOINT = f"http://localhost:8000/agents/{AGENT_ID}/runs"  # Endpoint do Agno Server


# 2 - Conexão com o Agno (Server) =============
def get_response_stream(message: str):
    response = requests.post(
        url=ENDPOINT,
        data={"message": message, "stream": "true"},
        stream=True  # Habilita o streaming da resposta
    )

# 3 - Streaming (Processamento) ===============


# 4 - Printa a Resposta =======================


# 5 - Run (loop) ==============================
if __name__ == "__main__":
    message = input("Digite a mensagem: ")
    response = get_response_stream(message)
    print(response)