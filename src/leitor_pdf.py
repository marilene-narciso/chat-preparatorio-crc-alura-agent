"""Leitura de arquivos PDF usando pypdf.

Fluxo: PDF -> pypdf -> texto.
"""

from pathlib import Path

from pypdf import PdfReader

PASTA_DOCUMENTOS = Path(__file__).resolve().parent.parent / "data" / "documentos"


def encontrar_primeiro_pdf(pasta=PASTA_DOCUMENTOS):
    """Localiza o primeiro arquivo PDF dentro da pasta informada."""
    pasta = Path(pasta)
    pdfs = sorted(pasta.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError(f"Nenhum PDF encontrado em {pasta}")
    return pdfs[0]


def ler_pdf(caminho_pdf):
    """Extrai o texto de um PDF e devolve informações básicas sobre ele."""
    caminho_pdf = Path(caminho_pdf)
    leitor = PdfReader(str(caminho_pdf))

    texto_completo = ""
    for pagina in leitor.pages:
        texto_completo += pagina.extract_text() or ""

    return {
        "nome_arquivo": caminho_pdf.name,
        "quantidade_paginas": len(leitor.pages),
        "quantidade_caracteres": len(texto_completo),
        "amostra_texto": texto_completo[:300].strip(),
    }


if __name__ == "__main__":
    caminho = encontrar_primeiro_pdf()
    info = ler_pdf(caminho)

    print(f"Arquivo: {info['nome_arquivo']}")
    print(f"Quantidade de páginas: {info['quantidade_paginas']}")
    print(f"Quantidade aproximada de caracteres extraídos: {info['quantidade_caracteres']}")
    print("Amostra do texto:")
    print(info["amostra_texto"])
