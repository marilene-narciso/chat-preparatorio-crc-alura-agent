from src.leitor_csv import ler_csv
from src.leitor_documentos import listar_documentos


def _primeiro_csv():
    for caminho in listar_documentos():
        if caminho.suffix.lower() == ".csv":
            return caminho
    raise FileNotFoundError("Nenhum CSV encontrado em data/documentos")


def test_ler_csv_extrai_texto():
    caminho = _primeiro_csv()
    resultado = ler_csv(caminho)

    assert resultado["nome_arquivo"] == caminho.name
    assert resultado["quantidade_linhas"] > 0
    assert resultado["quantidade_caracteres"] > 0
    assert resultado["amostra_texto"] != ""
