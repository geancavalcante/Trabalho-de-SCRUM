# Sprint 02 — Abertura e fila de chamados

**Período fictício:** 2026-02-19 a 2026-02-25
**Equipe:** Gean (PO + Backend), Kauê (SM + QA/Doc), Tony (Frontend)

## Sprint Goal

> "Permitir que um solicitante abra um chamado e que técnico/coordenador vejam a fila correta conforme o perfil."

## Sprint Backlog

| ID | Item | Estimativa | Owner | Status |
|---|---|---|---|---|
| US02 | Abertura de chamado (título, descrição, categoria, prioridade, lab) | 4 | Gean | Done |
| US04 | Detalhe e acompanhamento do próprio chamado | 3 | Gean + Tony | Done |
| US06 | Lista filtrada por perfil (técnico vê só seus) | 3 | Gean | Done |
| US09 | Lista do coordenador com filtros | 2 | Gean | Done |
| TASK09 | Modelos `Chamado`, `Laboratorio`, `HistoricoStatus` | 3 | Gean | Done |
| TASK10 | Templates: lista, formulário, detalhe (sem comentário ainda) | 4 | Tony | Done |
| TASK11 | Decorator `perfil_required` + `chamados_visiveis_para` | 2 | Gean | Done |
| TASK12 | Seed inicial (3 usuários, 3 labs, 3 chamados) | 2 | Kauê | Done |

**Pontos planejados:** 23 · **Pontos entregues:** 23.

## Daily Scrum — resumo da semana

- **Seg 19/02:** Modelagem definida. Gean migra `models.py`.
- **Ter 20/02:** Form de criação pronto. Tony monta `chamado_form.html`.
- **Qua 21/02:** Lista do solicitante operacional. Gean mexendo no decorator de perfil.
- **Qui 22/02:** Lista do coordenador e do técnico funcionando. Filtros por status, prioridade e categoria.
- **Sex 23/02:** Detalhe do chamado renderizando histórico (sem comentar ainda).
- **Sáb 24/02:** Seed pronto, 3 chamados de exemplo aparecem.
- **Dom 25/02:** Review + Retro.

**Impedimentos:** dúvida sobre se atribuição entra agora ou na Sprint 03. Decidido empurrar para 03 para fechar bem o fluxo de "abrir + visualizar" nesta.

## Sprint Review — Demo e feedback

**Demo:**
1. Login como `solicitante1`.
2. Abre chamado "Projetor não liga" com prioridade Alta e laboratório B2.
3. Aparece na lista do próprio solicitante (com badge "Novo").
4. Login como `coordenador1` → vê todos os 3 chamados na fila.
5. Login como `tecnico1` → vê só os atribuídos (ainda fixo via seed, atribuição UI vem na S03).
6. Filtros funcionando.

**Feedback:**
- "A tela de criar chamado ficou simples, gostei."
- "Achei a categoria 'Outros' importante."
- Pedido: deixar mais óbvio que o anexo é opcional. **Acolhido** — copy ajustado.

## Sprint Retrospective

| O que foi bem | O que pode melhorar | Ações |
|---|---|---|
| Velocidade boa, escopo entregue 100% | Pequenos bugs em filtro combinado (3 filtros) | Cobrir filtros com teste manual na S03 |
| Templates clean, acessíveis | Falta de feedback visual ao criar chamado | Adicionar mensagens flash (feito ainda na sprint) |
| Decorator de perfil ficou reutilizável | Gean sobrecarregado com backend | Tony passa a fazer parte das views simples |

## Incremento entregue

- Abertura de chamado funcional, com anexo opcional validado (extensão + tamanho).
- Listagem por perfil com filtros (status, prioridade, categoria).
- Tela de detalhe mostrando dados + histórico (comentários virão na S03).
- Seed completo para demo.
