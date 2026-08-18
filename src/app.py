"""Interface Streamlit do Chat Preparatório para Aprovação do CRC.

Fluxo: pergunta digitada -> src.rag.responder_pergunta() -> resposta exibida.
"""

import sys
from pathlib import Path

import streamlit as st

# Quando o Streamlit executa este arquivo diretamente, a pasta raiz do
# projeto não fica no caminho de busca do Python. Adicionamos ela aqui
# para que os imports "from src...." funcionem.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.leitor_documentos import listar_documentos
from src.rag import MENSAGEM_SEM_CONTEUDO, responder_pergunta
from src.tutor import MENSAGEM_INSUFICIENTE

st.set_page_config(page_title="Chat Preparatório para Aprovação do CRC", page_icon="📚")

st.title("Chat Preparatório para Aprovação do CRC")
st.caption("Assistente de estudos baseado em uma base de conhecimento.")

st.info(
    "As respostas deste assistente são geradas a partir dos documentos de estudo "
    "cadastrados na base de conhecimento (PDF ou CSV), não de conhecimento genérico.",
    icon="📄",
)

if not listar_documentos():
    st.warning(
        "Nenhum documento foi encontrado em data/documentos. Adicione arquivos PDF "
        "ou CSV para que o assistente possa responder.",
        icon="⚠️",
    )

if "historico" not in st.session_state:
    st.session_state.historico = []


def _perguntar_com_tratamento_de_erro(pergunta):
    """Chama o pipeline RAG e devolve (resposta, fontes, tipo).

    tipo é 'normal', 'aviso' (sem documentos / sem informação suficiente na
    base) ou 'erro' (falha ao consultar o assistente).
    """
    try:
        resultado = responder_pergunta(pergunta)
    except RuntimeError as erro:
        return str(erro), [], "erro"
    except Exception:
        mensagem = (
            "Não foi possível obter uma resposta agora. Isso pode acontecer por "
            "instabilidade temporária do serviço de IA. Tente novamente em alguns "
            "instantes."
        )
        return mensagem, [], "erro"

    resposta = resultado["resposta"]
    if resposta in (MENSAGEM_SEM_CONTEUDO, MENSAGEM_INSUFICIENTE):
        return resposta, [], "aviso"
    return resposta, resultado["fontes"], "normal"


def _exibir_resposta(resposta, fontes, tipo):
    if tipo == "erro":
        st.error(resposta)
    elif tipo == "aviso":
        st.warning(resposta)
    else:
        st.write(resposta)
        if fontes:
            st.caption("Fontes consultadas: " + ", ".join(fontes))


with st.form("form_pergunta", clear_on_submit=True):
    pergunta = st.text_input(
        "Sua pergunta:", placeholder="Ex.: O que é depreciação de ativos?"
    )
    enviar = st.form_submit_button("Enviar")

if enviar and pergunta.strip():
    with st.spinner("Buscando na base de conhecimento..."):
        resposta, fontes, tipo = _perguntar_com_tratamento_de_erro(pergunta)
    st.session_state.historico.append((pergunta, resposta, fontes, tipo))

# Histórico da conversa (mais antiga primeiro), sempre abaixo do formulário.
for pergunta_anterior, resposta_anterior, fontes_anteriores, tipo_anterior in st.session_state.historico:
    with st.chat_message("user"):
        st.write(pergunta_anterior)
    with st.chat_message("assistant"):
        _exibir_resposta(resposta_anterior, fontes_anteriores, tipo_anterior)
