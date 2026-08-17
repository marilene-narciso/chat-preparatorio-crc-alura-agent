"""Identifica automaticamente o tipo de um documento (PDF ou CSV) e o lê.

Fluxo: documento -> identifica extensão -> leitor correspondente -> texto.
"""

from pathlib import Path

from src.leitor_csv import ler_csv
from src.leitor_pdf import PASTA_DOCUMENTOS, ler_pdf

LEITORES_POR_TIPO = {
    "pdf": ler_pdf,
    "csv": ler_csv,
}


def identificar_tipo_documento(caminho):
    """Devolve 'pdf' ou 'csv' de acordo com a extensão do arquivo."""
    extensao = Path(caminho).suffix.lower().lstrip(".")
    if extensao not in LEITORES_POR_TIPO:
        raise ValueError(f"Tipo de arquivo não suportado: .{extensao}")
    return extensao


def ler_documento(caminho):
    """Lê um documento PDF ou CSV, identificando o tipo automaticamente."""
    caminho = Path(caminho)
    tipo = identificar_tipo_documento(caminho)
    informacoes = LEITORES_POR_TIPO[tipo](caminho)
    informacoes["tipo"] = tipo
    return informacoes


def listar_documentos(pasta=PASTA_DOCUMENTOS):
    """Lista todos os PDFs e CSVs encontrados na pasta, em ordem alfabética."""
    pasta = Path(pasta)
    documentos = list(pasta.glob("*.pdf")) + list(pasta.glob("*.csv"))
    return sorted(documentos, key=lambda caminho: caminho.name)


if __name__ == "__main__":
    for caminho in listar_documentos():
        info = ler_documento(caminho)
        unidade = "páginas" if info["tipo"] == "pdf" else "linhas"
        quantidade = info.get("quantidade_paginas", info.get("quantidade_linhas"))

        print(f"Arquivo: {info['nome_arquivo']} (tipo: {info['tipo']})")
        print(f"Quantidade de {unidade}: {quantidade}")
        print(f"Quantidade aproximada de caracteres extraídos: {info['quantidade_caracteres']}")
        print("Amostra do texto:")
        print(info["amostra_texto"])
        print("-" * 40)
