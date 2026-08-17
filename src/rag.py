"""Pipeline RAG: pergunta -> busca nos documentos -> tutor -> resposta fundamentada.

Fluxo: pergunta -> busca no índice vetorial -> trechos relevantes -> tutor monta o prompt -> Gemini -> resposta.
"""

from src.gemini_client import perguntar
from src.indexador import criar_ou_carregar_indice
from src.tutor import montar_prompt

QUANTIDADE_TRECHOS = 4

MENSAGEM_SEM_CONTEUDO = "Não há documentos processados na base de conhecimento ainda."


def responder_pergunta(pergunta, modo="padrao", k=QUANTIDADE_TRECHOS):
    """Busca os trechos mais relacionados à pergunta e gera uma resposta com o tutor."""
    try:
        indice = criar_ou_carregar_indice()
    except FileNotFoundError:
        return {"resposta": MENSAGEM_SEM_CONTEUDO, "fontes": []}

    trechos = indice.similarity_search(pergunta, k=k)
    if not trechos:
        return {"resposta": MENSAGEM_SEM_CONTEUDO, "fontes": []}

    prompt = montar_prompt(pergunta, trechos, modo=modo)

    resposta = perguntar(prompt)
    fontes = sorted({trecho.metadata["fonte"] for trecho in trechos})
    return {"resposta": resposta, "fontes": fontes}


if __name__ == "__main__":
    pergunta = "O que é depreciação?"
    resultado = responder_pergunta(pergunta)

    print(f"Pergunta: {pergunta}")
    print(f"Resposta: {resultado['resposta']}")
    print(f"Fontes: {', '.join(resultado['fontes']) if resultado['fontes'] else '(nenhuma)'}")
