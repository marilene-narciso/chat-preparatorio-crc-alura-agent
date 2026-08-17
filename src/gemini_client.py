"""Comunicação simples com o modelo Gemini.

Fluxo: pergunta -> Gemini -> resposta.
"""

import os

from google import genai

from src.config import obter_api_key  # já carrega o .env ao ser importado

MODELO_PADRAO = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")


def perguntar(pergunta, modelo=None):
    """Envia uma pergunta simples ao Gemini e devolve a resposta em texto."""
    modelo = modelo or MODELO_PADRAO
    cliente = genai.Client(api_key=obter_api_key())
    resposta = cliente.models.generate_content(model=modelo, contents=pergunta)
    return resposta.text


if __name__ == "__main__":
    pergunta = "Em uma frase, o que é o Exame de Suficiência do CRC?"
    print(f"Pergunta: {pergunta}")
    print(f"Resposta: {perguntar(pergunta)}")
