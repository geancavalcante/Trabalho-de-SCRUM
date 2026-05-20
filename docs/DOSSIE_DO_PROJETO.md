# Dossiê do Projeto — Helpdesk Labs

**Projeto:** Helpdesk Labs — Sistema de chamados para laboratórios de TI do campus
**Disciplina:** ARA0152 — Métodos Ágeis com Scrum (UNIFACIMP, 2026.1)
**Equipe (3 alunos, papéis distribuídos):** Gean Feitosa Cavalcante (PO + Dev Backend), Kauê do Nascimento Silva (Scrum Master + QA / Tech Writer), Tony Gabriel Alencar Alves (Dev Frontend)
**Período simulado:** 4 Sprints × 1 semana

---

## 1. Resumo executivo

A Coordenação de TI do campus opera os laboratórios sem um sistema único de chamados: pedidos chegam por WhatsApp, e-mail e visitas presenciais, sem fila auditável, sem priorização objetiva e sem histórico. Isso gera retrabalho, perda de pedidos e impossibilidade de medir desempenho da equipe técnica. O **Helpdesk Labs** é um MVP web que centraliza a abertura, triagem, atribuição, acompanhamento e fechamento dos chamados, com perfis distintos para solicitante, técnico e coordenador. Stack baseada em Django + SQLite (dev) e PostgreSQL (deploy), 100% open source, com autenticação nativa, controle de acesso por perfil, anexos validados, histórico imutável e relatórios consolidados. O resultado é um MVP funcional ao final da Sprint 4, atendendo as restrições de R$ 0 em licenças e podendo evoluir para produção em VPS free tier (Render/Railway). O foco é entregar valor mensurável: reduzir o tempo médio de atendimento e tornar 100% dos pedidos rastreáveis.

## 2. Problema e objetivos

**Problema:** Pedidos de suporte de TI dos laboratórios chegam por canais informais (WhatsApp, e-mail, balcão), sem padrão de registro, sem priorização e sem histórico. Não há SLA, não há indicadores e há perda de chamados.

**Objetivos:**
- Centralizar 100% dos chamados num único sistema com fila auditável.
- Permitir distribuição clara de tarefas para a equipe técnica.
- Gerar visibilidade gerencial sobre volume, prioridade, categoria e tempo de atendimento.

**Métricas de sucesso (mínimas):**
| Métrica | Baseline atual (estimado) | Meta após 1º mês de uso |
|---|---|---|
| % de chamados registrados no sistema (vs. canais informais) | ~30% | ≥ 90% |
| Tempo médio de atendimento (abertura → conclusão) | Não medido | Medido + estabelecer SLA |
| Chamados perdidos / não respondidos / mês | Não medido | < 5% do volume |

## 3. Stakeholders e perfis de usuário

| Stakeholder | Perfil de uso | Necessidade-chave |
|---|---|---|
| **Solicitante** (aluno, professor, monitor) | Abre chamados, acompanha o próprio chamado | Registro simples, sem treinamento, com retorno claro |
| **Técnico** (equipe TI) | Atende chamados atribuídos, comenta, atualiza status | Fila clara só com o que é dele, sem ruído |
| **Coordenador** (gerente de TI) | Visão geral, atribui técnicos, encerra/cancela, vê relatórios | Visibilidade total + indicadores para tomada de decisão |
| Direção acadêmica | Não usa o sistema, mas consome relatório | Saber se a operação está sob controle |

## 4. Jornada AS-IS e TO-BE

### AS-IS (estado atual)

| Passo | Ator | Dor |
|---|---|---|
| 1. Aluno acha defeito no projetor | Solicitante | Sem onde registrar |
| 2. Envia WhatsApp para o técnico que conhece | Solicitante | Pode mandar para o errado, pode não responder |
| 3. Técnico vê (ou não) o pedido | Técnico | Pedido se mistura a mensagens pessoais |
| 4. Técnico resolve, ou pede para coordenador resolver | Técnico/Coord | Sem rastro |
| 5. Coordenador não sabe quantos pedidos existem | Coordenador | Sem indicadores |

### TO-BE (estado desejado)

| Passo | Ator | Ganho |
|---|---|---|
| 1. Solicitante abre chamado no Helpdesk Labs com categoria, prioridade, lab e descrição | Solicitante | Padrão único |
| 2. Coordenador vê na fila e atribui ao técnico certo | Coordenador | Distribuição justa |
| 3. Técnico vê só os seus chamados, comenta, anexa, altera status | Técnico | Foco |
| 4. Solicitante acompanha o status, recebe contexto via comentários | Solicitante | Transparência |
| 5. Coordenador consulta relatórios por categoria/laboratório/tempo médio | Coordenador | Decisão baseada em dado |

## 5. Requisitos funcionais — User Stories

Formato: **Como [perfil], eu quero [ação] para [valor].**

| ID | User Story | Critério de aceite resumido |
|---|---|---|
| US01 | Como solicitante, quero fazer login para acessar apenas meus próprios chamados | Login válido redireciona para dashboard; inválido retorna erro |
| US02 | Como solicitante, quero abrir um chamado informando título, descrição, categoria, prioridade e laboratório | Chamado é criado com status "Novo" e aparece para mim |
| US03 | Como solicitante, quero anexar um arquivo opcional (imagem, log, PDF) ao chamado | Anexo é validado (extensão + 5MB) e gravado em /media |
| US04 | Como solicitante, quero acompanhar o status do meu chamado e ler comentários dos técnicos | Detalhe mostra status, histórico e comentários |
| US05 | Como solicitante, quero comentar no meu chamado para esclarecer dúvidas | Comentário gravado com autor e timestamp |
| US06 | Como técnico, quero ver apenas chamados atribuídos a mim para focar no que é meu | Lista filtra `tecnico=request.user` |
| US07 | Como técnico, quero comentar no chamado para registrar o que estou fazendo | Comentário visível para todos os envolvidos |
| US08 | Como técnico, quero mudar o status do chamado conforme o atendimento avança | Mudança gera entrada em HistoricoStatus |
| US09 | Como coordenador, quero ver todos os chamados em uma fila única | Lista exibe todos os chamados com filtros |
| US10 | Como coordenador, quero atribuir um técnico a um chamado | Campo `tecnico` é preenchido; status passa para "Em andamento" se estava "Novo" |
| US11 | Como coordenador, quero cancelar um chamado quando não for procedente | Status muda para "Cancelado" com registro de quem cancelou |
| US12 | Como coordenador, quero ver um relatório com chamados por categoria, laboratório, status e tempo médio | Página de relatórios consolida os agregados |
| US13 | Como sistema, devo registrar log de criação, atribuição, mudança de status e login para auditoria | Eventos relevantes gravados em `logs/app.log` |
| US14 | Como qualquer usuário autenticado, quero sair do sistema com segurança | Logout invalida a sessão e redireciona |

## 6. Requisitos não-funcionais (RNF)

| Categoria | RNF | Detalhe / verificação |
|---|---|---|
| **Segurança** | Autenticação obrigatória em todas as views (exceto login) | `@login_required` em todas; mixin de perfil; senha mínima 8 chars |
| | Proteção CSRF, XSS, clickjacking, MIME-sniffing | Middlewares Django ativos; `X_FRAME_OPTIONS=DENY` |
| | Validação de upload de anexos | Extensão whitelist + 5MB |
| | Não versionamento de segredos | `.gitignore` cobre `git_config.json`, `.env`, `db.sqlite3` |
| **Desempenho** | Resposta de listas < 500ms para até 1.000 chamados | `select_related` em FK; índices padrão Django |
| **Disponibilidade** | MVP roda em uma instância única (free tier aceita) | Sem requisito de HA no MVP; documentado em ADR-004 |
| **Manutenibilidade** | Código segue padrão Django padrão; testes cobrem fluxos críticos | 3 testes unitários cobrindo os 3 fluxos principais |
| **Usabilidade** | Web responsivo (mobile-first), idioma PT-BR | Bootstrap 5; templates testados em viewport ≥ 360px |
| | Mensagens de erro claras em PT-BR | Form errors + mensagens flash |
| **Auditabilidade** | Histórico imutável de status + comentários | Modelos `HistoricoStatus` e `Comentario` insert-only |
| **Compliance LGPD** | Dados mínimos (username, email institucional); senhas com hash | Hash padrão Django (PBKDF2); sem PII além de email |

## 7. Priorização do backlog — RICE

Fórmula: `RICE = (Reach × Impact × Confidence) / Effort`. Valores numa escala interna 1–5 (effort em "pontos de complexidade").

| US | Reach | Impact | Confidence | Effort | RICE | Sprint |
|---|---|---|---|---|---|---|
| US01 Login | 5 | 5 | 5 | 1 | 125 | 1 |
| US02 Abrir chamado | 5 | 5 | 5 | 2 | 62.5 | 2 |
| US04 Acompanhar chamado | 5 | 4 | 5 | 2 | 50 | 2 |
| US06 Lista do técnico | 4 | 5 | 5 | 1 | 100 | 2 |
| US08 Mudar status | 4 | 5 | 5 | 1 | 100 | 3 |
| US09 Lista do coordenador | 3 | 5 | 5 | 1 | 75 | 2 |
| US10 Atribuir técnico | 3 | 5 | 5 | 2 | 37.5 | 3 |
| US05/US07 Comentários | 5 | 3 | 5 | 2 | 37.5 | 3 |
| US03 Anexo | 4 | 3 | 4 | 2 | 24 | 3 |
| US12 Relatórios | 3 | 4 | 4 | 3 | 16 | 4 |
| US11 Cancelar | 3 | 3 | 5 | 1 | 45 | 3 |
| US13 Logs | 5 | 2 | 5 | 1 | 50 | 4 |
| US14 Logout | 5 | 2 | 5 | 1 | 50 | 1 |

**Justificativa:** RICE foi escolhido porque (a) o time tem boa visibilidade do alcance e impacto (sistema interno, escopo conhecido) e (b) effort é facilmente estimado em pontos pelo squad. A ordenação confirma a sequência das Sprints definida no escopo (auth → fila → atribuição/comentários → relatórios).

## 8. Matriz de decisão tecnológica

Versão sumária. Detalhes e pesos completos em [`/docs/decisoes/MATRIZ_DECISAO_TECNOLOGICA.md`](decisoes/MATRIZ_DECISAO_TECNOLOGICA.md).

| Decisão | Vencedor | Principal motivo |
|---|---|---|
| Stack/framework | **Django** | Auth, ORM, admin e templates prontos; domínio do time |
| Banco (dev/prod) | **SQLite (dev) → PostgreSQL (prod)** | Zero setup local; PostgreSQL gratuito em Render/Railway |
| Auth/Autorização | **Auth nativa Django + perfis customizados** | Zero custo, seguro, integrado, suficiente para o escopo |
| Deploy/Observabilidade | **Render free tier + logging em arquivo** | R$ 0; deploy via git; logs locais bastam para o MVP |

## 9. ADRs

- [ADR-001 — Stack/Framework](decisoes/adr/ADR-001-stack.md)
- [ADR-002 — Banco de Dados](decisoes/adr/ADR-002-banco-de-dados.md)
- [ADR-003 — Autenticação e Autorização](decisoes/adr/ADR-003-autenticacao-autorizacao.md)
- [ADR-004 — Deploy e Observabilidade](decisoes/adr/ADR-004-deploy-observabilidade.md)

## 10. Arquitetura — C4

- [Nível 1 — Contexto](arquitetura/C4-CONTEXTO.md): quem usa o sistema e quais sistemas externos.
- [Nível 2 — Containers](arquitetura/C4-CONTAINERS.md): aplicação web Django, banco SQLite/PostgreSQL, armazenamento de anexos local em `media/`.

## 11. Checklist mínimo de segurança — OWASP ASVS

Selecionado o subset L1 aplicável ao MVP, comentado em [`/docs/seguranca/ASVS_CHECKLIST_MINIMO.md`](seguranca/ASVS_CHECKLIST_MINIMO.md). Cobre: autenticação, gestão de sessão, controle de acesso, validação de entrada, upload seguro, proteção contra exposição de dados, logging.
