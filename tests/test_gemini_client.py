import os

import pytest

from src.gemini_client import perguntar


@pytest.mark.skipif(
    not os.environ.get("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY não configurada. Configure o .env para rodar este teste.",
)
def test_perguntar_responde_pergunta_simples():
    resposta = perguntar("Responda apenas com a palavra: ok")

    assert isinstance(resposta, str)
    assert resposta.strip() != ""
