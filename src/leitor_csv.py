"""Leitura de arquivos CSV usando pandas.

Fluxo: CSV -> pandas -> texto.
"""

from pathlib import Path

import pandas as pd


def ler_csv(caminho_csv):
    """Lê um CSV e devolve informações básicas sobre o conteúdo."""
    caminho_csv = Path(caminho_csv)
    tabela = pd.read_csv(caminho_csv)

    texto_completo = tabela.to_string(index=False)

    return {
        "nome_arquivo": caminho_csv.name,
        "quantidade_linhas": len(tabela),
        "quantidade_caracteres": len(texto_completo),
        "amostra_texto": texto_completo[:300].strip(),
    }
