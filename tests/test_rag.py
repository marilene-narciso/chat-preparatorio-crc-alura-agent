import os

import pytest

from src.rag import responder_pergunta

pytestmark = pytest.mark.skipif(
    not os.environ.get("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY não configurada. Configure o .env para rodar este teste.",
)


def test_responde_com_base_em_conteudo_presente_na_base():
    resultado = responder_pergunta("O que é depreciação?")

    assert resultado["resposta"].strip() != ""
    assert resultado["fontes"] != []


def test_nao_inventa_resposta_para_assunto_fora_da_base():
    resultado = responder_pergunta(
        "Qual é a receita tradicional de um bolo de cenoura com cobertura de chocolate?"
    )

    assert "não encontrei" in resultado["resposta"].lower()
