# CLAUDE.md

Este arquivo orienta o Claude Code ao trabalhar neste repositório.

## Sobre o projeto

**Nome:** Chat Preparatório para Aprovação do CRC
**Contexto:** Challenge Alura — Agente do programa ONE (Oracle Next Education) AI for Tech

**Objetivo:** criar um agente de inteligência artificial capaz de responder perguntas
sobre conteúdos preparatórios para o Exame de Suficiência do CRC, utilizando documentos
PDF ou CSV como base de conhecimento (RAG).

## Sobre a usuária

Iniciante absoluta em programação. Explicações devem ser em português, simples e sem
jargão desnecessário. Erros devem ser traduzidos em linguagem acessível, explicando o
que aconteceu e por quê.

## Requisitos obrigatórios do Challenge (não remover nem simplificar)

1. O agente precisa funcionar de ponta a ponta.
2. Deve responder com base nos documentos fornecidos (RAG), não apenas conhecimento
   genérico do modelo.
3. Deve processar arquivos PDF ou CSV como base de conhecimento.
4. Código simples, organizado e didático — prioridade sobre soluções elegantes/avançadas.
5. Projeto publicado em repositório público no GitHub.
6. Manter histórico de commits (commits pequenos e frequentes, não um único commit final).
7. O README deve conter:
   - descrição do projeto
   - arquitetura
   - tecnologias
   - instruções de execução
   - exemplos de perguntas
   - exemplos de respostas
   - evidência do deploy na OCI (prints/logs em `screenshots/`)
8. Aplicação implantada na Oracle Cloud Infrastructure (OCI Compute).
9. Priorizar funcionalidade sobre interface sofisticada — Streamlit básico é suficiente.

## Stack preferencial

- Python
- LangChain
- pypdf (leitura de PDF)
- pandas (leitura de CSV)
- Gemini (LLM e embeddings)
- RAG (Retrieval-Augmented Generation)
- Streamlit (interface)
- OCI Compute (hospedagem/deploy)

## Estrutura de pastas

- `data/` — documentos PDF/CSV usados como base de conhecimento
- `src/` — código-fonte da aplicação
- `tests/` — testes automatizados
- `screenshots/` — evidências (ex.: prints do deploy na OCI) usadas no README

## Regras de trabalho para o Claude Code

- Antes de alterar arquivos, explicar em português o que será feito.
- Trabalhar uma fase por vez — não adiantar etapas futuras sem alinhar antes.
- Não implementar funcionalidades que não foram pedidas.
- Preferir sempre a solução mais simples; evitar overengineering e abstrações
  desnecessárias.
- Nunca colocar chaves de API ou segredos diretamente no código.
- Usar arquivo `.env` para segredos (ex.: chave da API do Gemini).
- Manter `.env` listado no `.gitignore`.
- Após cada etapa relevante, executar testes e validar que o código funciona.
- Explicar qualquer erro em linguagem simples, sem jargão técnico não explicado.
- Antes de cada commit, apresentar um resumo das alterações para aprovação.
- Nunca fazer deploy (OCI ou qualquer outro ambiente) sem autorização explícita.
- Preservar sempre os requisitos obrigatórios do Challenge Alura listados acima.
