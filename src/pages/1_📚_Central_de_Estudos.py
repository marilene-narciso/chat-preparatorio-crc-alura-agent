"""Página de vídeos de apoio, organizados por categoria.

Fluxo: data/videos.json -> agrupado por categoria -> exibido em abas com cards.
"""

import json
from pathlib import Path

import streamlit as st

PASTA_RAIZ = Path(__file__).resolve().parent.parent.parent
CAMINHO_VIDEOS = PASTA_RAIZ / "data" / "videos.json"

CATEGORIAS = ["Revisão de Matéria", "Revisão de Provas", "Reconhecimento de Voz"]

st.set_page_config(page_title="Central de Estudos", page_icon="📚")

st.title("Central de Estudos")
st.caption("Vídeos de apoio organizados por categoria, para complementar seus estudos.")


def carregar_videos():
    """Lê a lista de vídeos cadastrados em data/videos.json."""
    if not CAMINHO_VIDEOS.exists():
        return []
    with open(CAMINHO_VIDEOS, encoding="utf-8") as arquivo:
        return json.load(arquivo)


videos = carregar_videos()
abas = st.tabs(CATEGORIAS)

for aba, categoria in zip(abas, CATEGORIAS):
    with aba:
        videos_da_categoria = [v for v in videos if v.get("categoria") == categoria]

        if not videos_da_categoria:
            st.info("Nenhum vídeo cadastrado nesta categoria ainda.")
            continue

        for video in videos_da_categoria:
            with st.container(border=True):
                st.subheader(video["titulo"])
                if video.get("assunto"):
                    st.caption(video["assunto"])
                if video.get("descricao"):
                    st.write(video["descricao"])
                st.video(video["url"])
