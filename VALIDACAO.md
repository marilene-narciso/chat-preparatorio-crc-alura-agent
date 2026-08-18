# Roteiro de Validação — Chat Preparatório para Aprovação do CRC

Este roteiro testa o pipeline RAG completo (`src/rag.py`) com perguntas reais,
executadas contra o índice vetorial construído a partir dos documentos em
`data/documentos/` (os 4 PDFs fornecidos + o CSV de exemplo).

Todas as perguntas e resultados esperados abaixo são baseados em trechos que
realmente existem nos arquivos — nenhum conteúdo foi inventado. As respostas
na coluna "Resultado obtido" são cópias literais do que o sistema respondeu.

**Status desta execução:** completa (7 de 7 perguntas concluídas). Durante a
primeira rodada de testes, 4 perguntas ficaram temporariamente pendentes por
um limite de cota da API do Gemini — ver observação no final do documento.

## Perguntas respondíveis pela base

| # | Pergunta | Fonte real do fato | Resultado esperado | Resultado obtido | Status |
|---|----------|--------------------|---------------------|-------------------|--------|
| 1 | Segundo o material, o total dos débitos sempre deve ser igual ao total dos créditos? | Resumo-Contabilidade-Geral.pdf: "O total dos débitos sempre terá que ser igual ao total dos créditos. Essa regra, em uma contabilidade regular, não comporta exceções." | Confirmar que sim, sempre iguais, sem exceções (Método das Partidas Dobradas) | "**Sim.** De acordo com o material, pelo **Método das Partidas Dobradas**, a soma dos débitos é sempre igual à soma dos créditos. Isso significa que para qualquer operação registrada, um ou mais débitos aplicados em uma ou mais contas deve sempre corresponder a um ou mais créditos de valor equivalente (ou seja, 'para todo débito existe um crédito de igual valor')." — Fontes: Apostila-Preparatoria-Exame-Suficiencia.pdf, Resumo-Contabilidade-Geral.pdf | **PASSOU** |
| 2 | O que é a conta capital social, segundo o resumo de contabilidade geral? | Resumo-Contabilidade-Geral.pdf: "Conta capital social: valor que os sócios entregam para o início da atividade." | Explicar que é o valor que os sócios entregam para o início da atividade | "Segundo o *Resumo de Contabilidade Geral*, a **conta capital social** é conceituada de duas formas complementares: 1. **Conta do Patrimônio Líquido (PL):** É composta pelas ações subscritas na constituição da sociedade ou com o aumento de capital, sendo dividida em *capital social* e *capital social a realizar* (item 69). 2. **Definição inicial:** Representa o valor que os sócios entregam para o início da atividade da entidade (item 8)." — Fontes: Apostila-Preparatoria-Exame-Suficiencia.pdf, Resumo-Contabilidade-Geral.pdf | **PASSOU** |
| 3 | Quantas questões objetivas tem a prova do Exame de Suficiência do Edital nº 02/2025? | prova_cfc20252_tipo01_comentada_parte 2.pdf: "caderno contendo 50 (cinquenta) questões objetivas" | Responder 50 questões objetivas | "A prova do Exame de Suficiência referente ao Edital nº 02/2025 é composta por **50 (cinquenta) questões objetivas**, cada uma contendo 4 opções de resposta (A, B, C e D), com apenas uma alternativa correta." — Fontes: Apostila-Preparatoria-Exame-Suficiencia.pdf, prova_cfc20252_tipo01_comentada_parte 2.pdf | **PASSOU** |
| 4 | Quanto tempo os candidatos têm para realizar essa prova do Exame de Suficiência? | prova_cfc20252_tipo01_comentada_parte 2.pdf: "Você dispõe de 4 (quatro) horas para a realização da prova, já incluído o tempo para a marcação do cartão de respostas" | Responder 4 horas | "Os candidatos dispõem de **4 (quatro) horas** para a realização da prova, tempo que já inclui o preenchimento do cartão de respostas." — Fontes: Apostila-Preparatoria-Exame-Suficiencia.pdf, prova_cfc20252_tipo01_comentada_parte 2.pdf | **PASSOU** |
| 5 | A partir de que ano a IFRS 18 entra em vigor de forma obrigatória? | Aulão - Intermediaria III - Programa de Revisão FMU.pdf: "A adoção é obrigatória a partir de 2027" | Responder 2027 | "A IFRS 18 entra em vigor e passa a ter adoção obrigatória a partir de **2027**." — Fontes: Aulão - Intermediaria III - Programa de Revisão FMU.pdf | **PASSOU** |

## Perguntas fora da base (não devem ser respondidas com conteúdo inventado)

| # | Pergunta | Resultado esperado | Resultado obtido | Status |
|---|----------|---------------------|-------------------|--------|
| 6 | Qual é a capital da França? | Recusar e informar que não encontrou a informação na base de conhecimento | "Não encontrei essa informação na base de conhecimento." — Fontes: Apostila-Preparatoria-Exame-Suficiencia.pdf, Aulão - Intermediaria III - Programa de Revisão FMU.pdf | **PASSOU** |
| 7 | Como trocar o óleo de um carro? | Recusar e informar que não encontrou a informação na base de conhecimento | "Não encontrei essa informação na base de conhecimento." — Fontes: Apostila-Preparatoria-Exame-Suficiencia.pdf, Resumo-Contabilidade-Geral.pdf | **PASSOU** |

## Resumo

- **Concluídas:** 7 de 7
- **Passou:** 7 de 7
- **Falhou:** 0

## Observação sobre a cota da API

Durante a primeira rodada de testes, a chave de API usada esgotou
repetidamente a cota de geração de respostas do Gemini (erro 429
RESOURCE_EXHAUSTED), mesmo com pausas de 20 a 30 segundos entre tentativas.
Isso é uma limitação temporária da conta do Google, não um defeito no código
do projeto — nas tentativas seguintes, todas as perguntas foram respondidas
normalmente.
