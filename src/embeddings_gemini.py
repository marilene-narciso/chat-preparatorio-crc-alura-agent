"""Embeddings do Gemini, no formato que o LangChain espera.

Fluxo: texto -> Gemini -> vetor numérico (embedding).
"""

import time

from google import genai
from google.genai import errors, types
from langchain_core.embeddings import Embeddings

from src.config import obter_api_key

MODELO_EMBEDDING = "gemini-embedding-001"
TAMANHO_DO_LOTE = 90  # um pouco abaixo do limite da API, por segurança
PAUSA_ENTRE_LOTES_SEGUNDOS = 65  # o plano gratuito limita pedidos por minuto
TENTATIVAS_POR_LOTE = 8
ESPERA_APOS_LIMITE_ATINGIDO_SEGUNDOS = 35


class EmbeddingsGemini(Embeddings):
    """Gera embeddings usando o Gemini, para uso com vetor stores do LangChain."""

    def __init__(self):
        self._cliente = genai.Client(api_key=obter_api_key())

    def embed_documents(self, texts):
        """Gera um embedding para cada trecho de documento.

        Envia em lotes pequenos, com pausa entre eles, para respeitar o
        limite de pedidos por minuto do plano gratuito do Gemini.
        """
        vetores = []
        for indice_lote, inicio in enumerate(range(0, len(texts), TAMANHO_DO_LOTE)):
            if indice_lote > 0:
                time.sleep(PAUSA_ENTRE_LOTES_SEGUNDOS)
            lote = texts[inicio:inicio + TAMANHO_DO_LOTE]
            vetores.extend(self._embedar_lote(lote, "RETRIEVAL_DOCUMENT"))
        return vetores

    def embed_query(self, text):
        """Gera o embedding de uma pergunta do usuário."""
        return self._embedar_lote([text], "RETRIEVAL_QUERY")[0]

    def _embedar_lote(self, textos, tipo_tarefa):
        """Chama a API do Gemini, esperando e tentando de novo se a cota for atingida."""
        for tentativa in range(TENTATIVAS_POR_LOTE):
            try:
                resposta = self._cliente.models.embed_content(
                    model=MODELO_EMBEDDING,
                    contents=textos,
                    config=types.EmbedContentConfig(task_type=tipo_tarefa),
                )
                return [embedding.values for embedding in resposta.embeddings]
            except errors.ClientError as erro:
                ultima_tentativa = tentativa == TENTATIVAS_POR_LOTE - 1
                if erro.code == 429 and not ultima_tentativa:
                    time.sleep(ESPERA_APOS_LIMITE_ATINGIDO_SEGUNDOS)
                    continue
                raise
