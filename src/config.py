"""Configuração e segredos do projeto, lidos do arquivo .env."""

import os

from dotenv import load_dotenv

load_dotenv()


def obter_api_key():
    """Devolve a chave da API do Gemini, ou explica como configurá-la."""
    chave = os.environ.get("GOOGLE_API_KEY")
    if not chave:
        raise RuntimeError(
            "Chave da API do Gemini não encontrada. "
            "Copie o arquivo .env.example para .env e preencha "
            "GOOGLE_API_KEY com sua chave "
            "(veja https://aistudio.google.com/apikey)."
        )
    return chave
