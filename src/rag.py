"""Pipeline RAG: pergunta -> busca nos documentos -> resposta fundamentada.

Fluxo: pergunta -> busca no índice vetorial -> trechos relevantes -> prompt -> Gemini -> resposta.
"""

from src.gemini_client import perguntar
from src.indexador import criar_ou_carregar_indice

QUANTIDADE_TRECHOS = 4

MENSAGEM_SEM_CONTEUDO = "Não há documentos processados na base de conhecimento ainda."

PROMPT_TEMPLATE = """Responda à pergunta usando apenas as informações presentes nos \
trechos abaixo, retirados dos documentos de estudo.

Se a resposta não estiver claramente presente nos trechos, responda exatamente:
"Não encontrei essa informação na base de conhecimento."

Trechos:
{contexto}

Pergunta: {pergunta}
"""


def responder_pergunta(pergunta, k=QUANTIDADE_TRECHOS):
    """Busca os trechos mais relacionados à pergunta e gera uma resposta com o Gemini."""
    try:
        indice = criar_ou_carregar_indice()
    except FileNotFoundError:
        return {"resposta": MENSAGEM_SEM_CONTEUDO, "fontes": []}

    trechos = indice.similarity_search(pergunta, k=k)
    if not trechos:
        return {"resposta": MENSAGEM_SEM_CONTEUDO, "fontes": []}

    contexto = "\n\n".join(
        f"(Fonte: {trecho.metadata['fonte']})\n{trecho.page_content}" for trecho in trechos
    )
    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)

    resposta = perguntar(prompt)
    fontes = sorted({trecho.metadata["fonte"] for trecho in trechos})
    return {"resposta": resposta, "fontes": fontes}


if __name__ == "__main__":
    pergunta = "O que é depreciação?"
    resultado = responder_pergunta(pergunta)

    print(f"Pergunta: {pergunta}")
    print(f"Resposta: {resultado['resposta']}")
    print(f"Fontes: {', '.join(resultado['fontes']) if resultado['fontes'] else '(nenhuma)'}")
