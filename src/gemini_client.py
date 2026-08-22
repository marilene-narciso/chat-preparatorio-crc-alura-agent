"""Comunicação com o modelo Gemini com retry para falhas temporárias.

Fluxo: pergunta -> Gemini -> resposta.
"""

import os
import time

from google import genai
from google.genai import errors

from src.config import obter_api_key


MODELO_PADRAO = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")

MAX_TENTATIVAS = 4
TEMPOS_ESPERA = [2, 5, 10]


def perguntar(pergunta, modelo=None):
    """Envia uma pergunta ao Gemini com retry para erros temporários 503."""
    modelo = modelo or MODELO_PADRAO
    cliente = genai.Client(api_key=obter_api_key())

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            resposta = cliente.models.generate_content(
                model=modelo,
                contents=pergunta,
            )
            return resposta.text

        except errors.ServerError as erro:
            status = getattr(erro, "code", None)

            # Retry apenas para indisponibilidade temporária do serviço.
            if status != 503 or tentativa == MAX_TENTATIVAS:
                raise

            espera = TEMPOS_ESPERA[tentativa - 1]

            print(
                f"Gemini temporariamente indisponível (503). "
                f"Tentativa {tentativa}/{MAX_TENTATIVAS}. "
                f"Nova tentativa em {espera}s..."
            )

            time.sleep(espera)


if __name__ == "__main__":
    pergunta = "Em uma frase, o que é o Exame de Suficiência do CRC?"
    print(f"Pergunta: {pergunta}")
    print(f"Resposta: {perguntar(pergunta)}")
