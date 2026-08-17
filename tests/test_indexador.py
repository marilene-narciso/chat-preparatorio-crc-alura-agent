from src.indexador import dividir_em_trechos


def test_dividir_em_trechos_texto_curto_gera_um_trecho():
    trechos = dividir_em_trechos("Texto curto de exemplo.", "arquivo.pdf")

    assert len(trechos) == 1
    assert trechos[0].page_content == "Texto curto de exemplo."
    assert trechos[0].metadata["fonte"] == "arquivo.pdf"


def test_dividir_em_trechos_texto_longo_gera_varios_trechos():
    texto_longo = "Contabilidade geral. " * 500

    trechos = dividir_em_trechos(texto_longo, "apostila.pdf")

    assert len(trechos) > 1
    assert all(trecho.metadata["fonte"] == "apostila.pdf" for trecho in trechos)
    assert all(len(trecho.page_content) <= 1500 for trecho in trechos)
