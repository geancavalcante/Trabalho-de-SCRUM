# Sprint 03 — Atribuição, comentários, histórico e anexos

**Período fictício:** 2026-02-26 a 2026-03-04
**Equipe:** Gean (PO + Backend), Kauê (SM + QA/Doc), Tony (Frontend)

## Sprint Goal

> "Fechar o ciclo de vida operacional do chamado: o coordenador atribui, o técnico atualiza status, ambos comentam, anexos funcionam e tudo fica auditado."

## Sprint Backlog

| ID | Item | Estimativa | Owner | Status |
|---|---|---|---|---|
| US05 | Solicitante comenta no próprio chamado | 2 | Tony | Done |
| US07 | Técnico comenta no chamado | 2 | Tony | Done |
| US08 | Técnico altera status do chamado atribuído | 3 | Gean | Done |
| US10 | Coordenador atribui técnico | 3 | Gean | Done |
| US11 | Coordenador cancela chamado | 1 | Gean | Done |
| US03 | Anexo opcional validado (extensão + 5MB) | 2 | Gean | Done |
| TASK13 | Modelo `Comentario` + `HistoricoStatus` na criação | 2 | Gean | Done |
| TASK14 | UI no detalhe: form de comentário + atribuição + status | 3 | Tony | Done |
| TASK15 | Helpers `pode_alterar_status`, `pode_comentar` | 2 | Gean | Done |

**Pontos planejados:** 20 · **Pontos entregues:** 20.

## Daily Scrum — resumo da semana

- **Seg 26/02:** Modelos `Comentario` e `HistoricoStatus` ampliados. Migration aplicada.
- **Ter 27/02:** Form de atribuição na tela de detalhe. Gean testa transição automática Novo → Em andamento.
- **Qua 28/02:** Comentários renderizando na ordem cronológica. Tony ajusta layout.
- **Qui 29/02:** Anexos validados com whitelist e tamanho — `clean_anexo` no form.
- **Sex 01/03:** Cancelamento de chamado: ao mudar para "Cancelado", limpa `concluido_em`.
- **Sáb 02/03:** Pequenos ajustes de cópia. `pode_comentar` revisado.
- **Dom 03/03:** Review + Retro.

**Impedimentos:** ambiguidade sobre quem pode comentar quando um chamado já foi cancelado. Decisão registrada: solicitante e técnico que estiveram envolvidos continuam vendo o chamado, mas a UI deixa de exibir o form de comentário/status (a regra ainda foi mantida simples no MVP — `pode_comentar` continua permitindo, e cabe ao coordenador encerrar a conversa).

## Sprint Review — Demo e feedback

**Demo:**
1. Coordenador atribui o chamado "Projetor não liga" ao `tecnico1` — status passa de "Novo" para "Em andamento" automaticamente.
2. Técnico comenta: "Estou indo verificar fonte."
3. Solicitante vê o comentário em tempo (após reload).
4. Técnico altera para "Concluído" — `concluido_em` é gravado.
5. Histórico mostra a trilha completa: "" → Novo → Em andamento → Concluído com autor e data.
6. Tentativa de upload `.exe` é barrada com mensagem clara em PT-BR.

**Feedback:**
- "O histórico parece muito profissional. Direção vai gostar."
- "Falta um relatório com indicadores." — **Já planejado para S04, confirmado.**
- "Coordenador precisaria poder reverter status." — Avaliação: tecnicamente já é possível (o select mostra todos os status); UX confirmada na demo.

## Sprint Retrospective

| O que foi bem | O que pode melhorar | Ações |
|---|---|---|
| Atribuição automática poupa um clique do coordenador | UI do detalhe ficou densa | Reorganizar em 2 colunas (feito) |
| Validação de anexo robusta | Mensagem de extensão poderia listar exemplos | Adicionado texto auxiliar embaixo do campo |
| Par Gean–Tony sincronizado entre backend e frontend | Documentação caminhou um pouco atrás | Bloquear 1h por dia para doc na S04 |

## Incremento entregue

- Coordenador atribui técnico; mudança automática de status quando partia de "Novo".
- Técnico/Coordenador comentam e alteram status; solicitante comenta no próprio.
- Anexos opcionais com validação clara.
- Histórico imutável com de_status / para_status / autor / timestamp.
- Decorator `perfil_required` e helpers `pode_*` consolidados em `permissions.py`.
