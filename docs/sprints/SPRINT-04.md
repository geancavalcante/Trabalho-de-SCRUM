# Sprint 04 — Relatórios, segurança mínima, documentação final e apresentação

**Período fictício:** 2026-03-05 a 2026-03-11
**Equipe:** Gean (PO + Backend), Kauê (SM + QA/Doc), Tony (Frontend)

## Sprint Goal

> "Fechar o MVP entregando relatórios consolidados, garantindo o checklist mínimo de segurança, deixando a documentação completa e preparando a apresentação final."

## Sprint Backlog

| ID | Item | Estimativa | Owner | Status |
|---|---|---|---|---|
| US12 | Relatório: chamados por categoria, laboratório, status, tempo médio | 4 | Gean | Done |
| US13 | Logs de eventos relevantes (login, criar, atribuir, status) | 2 | Gean | Done |
| TASK16 | Aplicar checklist ASVS L1 e documentar | 3 | Kauê | Done |
| TASK17 | Testes automatizados (3 testes-chave) | 3 | Kauê + Gean | Done |
| TASK18 | README com instruções completas | 2 | Kauê | Done |
| TASK19 | Script de exportação PDF/DOCX (pandoc) | 1 | Tony | Done |
| TASK20 | Apresentação Final (`APRESENTACAO_FINAL.md`) | 2 | Gean + Kauê | Done |
| TASK21 | Smoke test em viewport mobile (360px) | 1 | Tony | Done |

**Pontos planejados:** 18 · **Pontos entregues:** 18.

## Daily Scrum — resumo da semana

- **Seg 05/03:** Gean codifica relatórios; Tony pensa nos cards.
- **Ter 06/03:** Logs em arquivo. Kauê começa o checklist ASVS.
- **Qua 07/03:** Testes automatizados: criação, autorização, mudança de status. Todos verdes.
- **Qui 08/03:** README revisado. Tony cria script `export_docs.ps1`.
- **Sex 09/03:** Apresentação final escrita. Ensaio interno.
- **Sáb 10/03:** Smoke test em mobile + ajustes finos no `base.html`.
- **Dom 11/03:** Review + Retro.

**Impedimentos:** pandoc não estava instalado no laptop de demo — substituído por script + instruções claras no README. Aceitável (escopo permite).

## Sprint Review — Demo e feedback

**Demo final:**
1. Dashboard do coordenador com KPIs (totais por status).
2. Tela de Relatórios: tempo médio de atendimento (h), totais por categoria/laboratório/status.
3. Demonstração de logs em arquivo (`logs/app.log`): login, criação, atribuição, mudança de status.
4. Run dos 3 testes automatizados — todos passam.
5. Apresentação dos próximos passos (notificações por e-mail, login Microsoft, lockout, S3 para anexos).

**Feedback final:**
- "Está pronto para piloto. Quero levar para direção."
- "O relatório resolve o pedido recorrente da direção."
- Sugestão: incluir "Top 5 categorias do mês" — registrado no backlog futuro.

## Sprint Retrospective

| O que foi bem | O que pode melhorar | Ações para v2 |
|---|---|---|
| Velocidade consistente nas 4 sprints | Subestimamos export de PDF | Investir em GitHub Action com pandoc |
| Doc + código andaram juntos | Faltou monitoramento de erro | Adotar Sentry no v2 |
| MVP entregue dentro do prazo | Sem MFA | Adicionar TOTP/Allauth no v2 |

## Incremento entregue (MVP final)

- Sistema funcional end-to-end: login, abrir, listar, atribuir, comentar, mudar status, relatórios.
- 3 testes automatizados verdes.
- Documentação Scrum completa (Dossiê, ADRs, C4, ASVS, Discovery, 4 Sprints, Apresentação).
- README com instruções claras para qualquer dev rodar em < 5 min.
- Logs de auditoria operacionais.
- Script de exportação de docs para PDF/DOCX via pandoc.
