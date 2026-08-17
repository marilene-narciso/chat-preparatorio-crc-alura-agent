import pytest

from src.leitor_documentos import identificar_tipo_documento, ler_documento, listar_documentos


def _primeiro_por_tipo(tipo):
    for caminho in listar_documentos():
        if caminho.suffix.lower() == f".{tipo}":
            return caminho
    raise FileNotFoundError(f"Nenhum arquivo do tipo {tipo} encontrado em data/documentos")


def test_identifica_tipo_pdf_e_csv():
    assert identificar_tipo_documento("relatorio.pdf") == "pdf"
    assert identificar_tipo_documento("dados.csv") == "csv"


def test_tipo_nao_suportado_gera_erro():
    with pytest.raises(ValueError):
        identificar_tipo_documento("arquivo.txt")


def test_ler_documento_identifica_pdf_automaticamente():
    caminho = _primeiro_por_tipo("pdf")
    info = ler_documento(caminho)

    assert info["tipo"] == "pdf"
    assert info["quantidade_caracteres"] > 0
    assert info["amostra_texto"] != ""


def test_ler_documento_identifica_csv_automaticamente():
    caminho = _primeiro_por_tipo("csv")
    info = ler_documento(caminho)

    assert info["tipo"] == "csv"
    assert info["quantidade_caracteres"] > 0
    assert info["amostra_texto"] != ""
