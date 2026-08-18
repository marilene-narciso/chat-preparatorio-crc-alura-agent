"""Personalidade e instruções do tutor do Chat Preparatório para Aprovação do CRC.

Este módulo só monta o texto do prompt (pergunta + trechos -> prompt). Ele não
carrega documentos nem chama a API do Gemini — essas responsabilidades ficam
em outros módulos (leitor_pdf.py, leitor_csv.py, indexador.py, gemini_client.py).
"""

MENSAGEM_INSUFICIENTE = "Não encontrei essa informação na base de conhecimento."

INSTRUCOES_BASE = f"""Você é o tutor educacional do "Chat Preparatório para Aprovação do CRC", \
que ajuda estudantes a se prepararem para o Exame de Suficiência do Conselho Federal de \
Contabilidade (CRC).

Regras que você deve seguir sempre:
- Responda usando prioritariamente as informações presentes nos trechos de documentos \
fornecidos abaixo.
- Explique os conceitos de forma simples e didática, como um bom professor faria.
- Nunca invente informações que não estejam nos trechos fornecidos.
- Se os trechos não contiverem informação suficiente para responder, diga isso claramente: \
"{MENSAGEM_INSUFICIENTE}" Não tente adivinhar.
- Use sempre uma linguagem educacional, clara e objetiva."""

INSTRUCOES_POR_MODO = {
    "padrao": "Responda à pergunta do aluno de forma direta.",
    "resumo": "Explique de forma resumida, em poucas frases, apenas os pontos essenciais.",
    "detalhado": "Explique de forma detalhada, cobrindo os principais aspectos do conceito, "
    "com exemplos quando fizer sentido.",
    "perguntas_estudo": "Em vez de responder diretamente, gere de 3 a 5 perguntas de estudo "
    "(com o gabarito de cada uma) baseadas SOMENTE no conteúdo dos trechos fornecidos. "
    "Não use nenhum conhecimento que não esteja nos trechos.",
    "alternativa": "O aluno quer saber por que uma alternativa/resposta é a correta. Explique "
    "o motivo com base nos trechos fornecidos. Se os trechos não confirmarem isso claramente, "
    "diga que não há informação suficiente para confirmar.",
}

PROMPT_BASE = """{instrucoes_base}

Instrução para esta resposta: {instrucao_modo}

Trechos dos documentos de estudo:
{contexto}

Pergunta do aluno: {pergunta}
"""


def montar_prompt(pergunta, trechos, modo="padrao"):
    """Monta o prompt do tutor a partir da pergunta e dos trechos já recuperados."""
    if modo not in INSTRUCOES_POR_MODO:
        modos_disponiveis = ", ".join(sorted(INSTRUCOES_POR_MODO))
        raise ValueError(f"Modo '{modo}' não suportado. Modos disponíveis: {modos_disponiveis}")

    contexto = "\n\n".join(
        f"(Fonte: {trecho.metadata['fonte']})\n{trecho.page_content}" for trecho in trechos
    )

    return PROMPT_BASE.format(
        instrucoes_base=INSTRUCOES_BASE,
        instrucao_modo=INSTRUCOES_POR_MODO[modo],
        contexto=contexto,
        pergunta=pergunta,
    )
