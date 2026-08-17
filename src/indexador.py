"""Divide os documentos em trechos e mantém o índice vetorial de busca.

Fluxo: documentos -> trechos -> embeddings -> índice vetorial (FAISS).
"""

import time
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.embeddings_gemini import EmbeddingsGemini
from src.leitor_documentos import listar_documentos, ler_documento

PASTA_INDICE = Path(__file__).resolve().parent.parent / "data" / "indice_vetorial"

TAMANHO_TRECHO = 1500
SOBREPOSICAO_TRECHO = 200

# A API do Gemini às vezes recusa chamadas de indexação com muito volume de
# texto de uma vez. Construir o índice em pedaços pequenos, salvando o
# progresso a cada pedaço, é mais lento mas bem mais confiável.
TAMANHO_PEDACO_INDEXACAO = 25
PAUSA_ENTRE_PEDACOS_SEGUNDOS = 3


def dividir_em_trechos(texto, nome_arquivo):
    """Divide o texto de um documento em trechos menores (chunks)."""
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=TAMANHO_TRECHO,
        chunk_overlap=SOBREPOSICAO_TRECHO,
    )
    return [
        Document(page_content=trecho, metadata={"fonte": nome_arquivo})
        for trecho in divisor.split_text(texto)
    ]


def montar_documentos_para_indice(pasta=None):
    """Lê todos os documentos disponíveis e devolve a lista completa de trechos."""
    caminhos = listar_documentos(pasta) if pasta else listar_documentos()

    trechos = []
    for caminho in caminhos:
        info = ler_documento(caminho)
        trechos.extend(dividir_em_trechos(info["texto"], info["nome_arquivo"]))
    return trechos


def criar_ou_carregar_indice(forcar_reconstrucao=False):
    """Carrega o índice vetorial salvo em disco, ou cria um novo se necessário."""
    embeddings = EmbeddingsGemini()

    indice_existe = (PASTA_INDICE / "index.faiss").exists()
    if indice_existe and not forcar_reconstrucao:
        return FAISS.load_local(
            str(PASTA_INDICE), embeddings, allow_dangerous_deserialization=True
        )

    trechos = montar_documentos_para_indice()
    if not trechos:
        raise FileNotFoundError(
            "Nenhum documento encontrado em data/documentos para indexar."
        )

    PASTA_INDICE.mkdir(parents=True, exist_ok=True)

    indice = None
    for inicio in range(0, len(trechos), TAMANHO_PEDACO_INDEXACAO):
        pedaco = trechos[inicio:inicio + TAMANHO_PEDACO_INDEXACAO]
        if indice is None:
            indice = FAISS.from_documents(pedaco, embeddings)
        else:
            indice.add_documents(pedaco)

        indice.save_local(str(PASTA_INDICE))  # salva o progresso a cada pedaço

        if inicio + TAMANHO_PEDACO_INDEXACAO < len(trechos):
            time.sleep(PAUSA_ENTRE_PEDACOS_SEGUNDOS)

    return indice


if __name__ == "__main__":
    indice = criar_ou_carregar_indice()
    print(f"Índice pronto com {indice.index.ntotal} trechos.")
