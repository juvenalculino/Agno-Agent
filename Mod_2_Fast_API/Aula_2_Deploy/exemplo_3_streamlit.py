import json
import os

import requests
import streamlit as st

from dotenv import load_dotenv


AGENT_ID = "agente_pdf"
AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "https://agno-agent-rr34.onrender.com/")
ENDPOINT = f"{AGENT_BASE_URL}/agents/{AGENT_ID}/runs"


def extract_text_from_event(event):
    """Extrai o texto da resposta do payload SSE."""
    if isinstance(event, str):
        return event

    if not isinstance(event, dict):
        return ""

    for key in ("content", "message", "text", "delta", "answer"):
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value
        if isinstance(value, list):
            texts = []
            for item in value:
                texto_item = extract_text_from_event(item)
                if texto_item:
                    texts.append(texto_item)
            if texts:
                return "".join(texts)
        if isinstance(value, dict):
            nested = extract_text_from_event(value)
            if nested:
                return nested

    if "data" in event and isinstance(event["data"], (dict, list, str)):
        return extract_text_from_event(event["data"])

    return json.dumps(event, ensure_ascii=False)


def get_response_stream(message: str):
    """Envia a pergunta para o agente e devolve o stream SSE."""
    payloads = [
        {"json": {"message": message, "stream": True}},
        {"data": {"message": message, "stream": "true"}},
    ]

    last_error = None

    for payload in payloads:
        try:
            response = requests.post(ENDPOINT, timeout=120, stream=True, **payload)
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                text = line.decode("utf-8", errors="ignore")
                if not text.startswith("data:"):
                    continue

                raw = text.replace("data:", "", 1).strip()
                if not raw or raw == "[DONE]":
                    continue

                try:
                    event = json.loads(raw)
                    yield event
                except json.JSONDecodeError:
                    continue

            return

        except requests.RequestException as exc:
            last_error = exc
            continue

    raise RuntimeError(f"Não foi possível conectar ao agente em {ENDPOINT}. Detalhe: {last_error}")


st.set_page_config(page_title="Agente PDF", page_icon="📄")
st.title("Agente CHAT PDF")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Digite sua pergunta para o agente...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resposta = st.empty()
        resposta_texto = ""

        try:
            for event in get_response_stream(prompt):
                texto = extract_text_from_event(event)
                if texto:
                    resposta_texto += texto
                    resposta.markdown(resposta_texto)

            if not resposta_texto.strip():
                resposta_texto = "Não houve resposta do agente."
                resposta.markdown(resposta_texto)

        except Exception as exc:
            resposta_texto = f"Erro ao consultar o agente: {exc}"
            resposta.error(resposta_texto)

    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})

with st.sidebar:
    st.subheader("Ações")
    if st.button("Limpar conversa"):
        st.session_state.messages = []
        st.rerun()
