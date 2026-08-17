import pytest
from langchain_core.documents import Document

from src.tutor import montar_prompt


def _trechos_exemplo():
    return [
        Document(
            page_content="Depreciação é o reconhecimento da perda de valor de um ativo ao longo do tempo.",
            metadata={"fonte": "resumo.pdf"},
        )
    ]


def test_prompt_inclui_pergunta_contexto_e_fonte():
    prompt = montar_prompt("O que é depreciação?", _trechos_exemplo())

    assert "O que é depreciação?" in prompt
    assert "perda de valor de um ativo" in prompt
    assert "resumo.pdf" in prompt


def test_prompt_sempre_inclui_regra_de_nao_inventar():
    prompt = montar_prompt("O que é depreciação?", _trechos_exemplo())

    assert "não invente" in prompt.lower() or "nunca invente" in prompt.lower()
    assert "não encontrei essa informação" in prompt.lower()


def test_modo_resumo_pede_explicacao_curta():
    prompt = montar_prompt("O que é depreciação?", _trechos_exemplo(), modo="resumo")

    assert "resumid" in prompt.lower()


def test_modo_detalhado_pede_explicacao_completa():
    prompt = montar_prompt("O que é depreciação?", _trechos_exemplo(), modo="detalhado")

    assert "detalhad" in prompt.lower()


def test_modo_perguntas_estudo_pede_geracao_de_perguntas():
    prompt = montar_prompt(
        "Gere perguntas sobre depreciação", _trechos_exemplo(), modo="perguntas_estudo"
    )

    assert "perguntas de estudo" in prompt.lower()
    assert "gabarito" in prompt.lower()


def test_modo_alternativa_pede_justificativa():
    prompt = montar_prompt(
        "Por que a alternativa B está correta?", _trechos_exemplo(), modo="alternativa"
    )

    assert "alternativa" in prompt.lower()


def test_modo_invalido_gera_erro():
    with pytest.raises(ValueError):
        montar_prompt("O que é depreciação?", _trechos_exemplo(), modo="modo_inexistente")
