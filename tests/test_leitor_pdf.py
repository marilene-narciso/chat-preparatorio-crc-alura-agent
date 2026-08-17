from src.leitor_pdf import encontrar_primeiro_pdf, ler_pdf


def test_ler_pdf_extrai_texto():
    caminho = encontrar_primeiro_pdf()
    resultado = ler_pdf(caminho)

    assert resultado["nome_arquivo"] == caminho.name
    assert resultado["quantidade_paginas"] > 0
    assert resultado["quantidade_caracteres"] > 0
    assert resultado["amostra_texto"] != ""
