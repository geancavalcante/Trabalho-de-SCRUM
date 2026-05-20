# Sprint 01 — Discovery, arquitetura, setup e autenticação base

**Período fictício:** 2026-02-12 a 2026-02-18
**Equipe:** Gean (PO + Backend), Kauê (SM + QA/Doc), Tony (Frontend)

## Sprint Goal

> "Concluir a fase de Discovery, formalizar as decisões técnicas e ter o esqueleto da aplicação rodando com autenticação e perfis de usuário."

## Sprint Backlog

| ID | Item | Estimativa | Owner | Status |
|---|---|---|---|---|
| US01 | Login e logout funcionais | 3 | Gean | Done |
| US14 | Logout seguro | 1 | Gean | Done |
| TASK01 | Entrevista fictícia com coordenação (E1) | 2 | Gean | Done |
| TASK02 | Benchmark de ferramentas (E2) | 2 | Gean + Kauê | Done |
| TASK03 | Discovery Log com >= 8 descobertas | 2 | Gean | Done |
| TASK04 | Matriz de decisão tecnológica | 3 | Kauê + Gean | Done |
| TASK05 | ADR-001..004 redigidos | 3 | Gean | Done |
| TASK06 | C4 Contexto e Containers em Mermaid | 2 | Tony | Done |
| TASK07 | Setup do projeto Django + perfis (`PerfilUsuario`) | 3 | Gean | Done |
| TASK08 | Diretrizes de estilo / base.html / Bootstrap CDN | 2 | Tony | Done |

**Pontos planejados:** 23 · **Pontos entregues:** 23.

## Daily Scrum — resumo da semana

- **Seg 12/02:** Kickoff. Definição da Sprint Goal. Gean começa setup do Django.
- **Ter 13/02:** Gean finaliza E1 e inicia E2. Kauê define critérios da matriz.
- **Qua 14/02:** ADRs 001 e 002 publicados. Tony monta `base.html`.
- **Qui 15/02:** ADRs 003 e 004 publicados. Gean termina sistema de perfis + signal.
- **Sex 16/02:** Login funcionando. Kauê começa rascunho do plano de testes.
- **Sáb 17/02:** Cleanup, escrita de Discovery Log.
- **Dom 18/02:** Review + Retro.

**Impedimentos:** nenhum bloqueante. Ajuste menor: Django 5 exige Python ≥ 3.10 — todos confirmaram ambiente local OK.

## Sprint Review — Demo e feedback

**Demo realizada para a Coordenação fictícia:**
- Tela de login (responsiva), com mensagem clara em PT-BR.
- Login dos três perfis (solicitante, técnico, coordenador) leva ao dashboard apropriado.
- Painel admin do Django mostrando os modelos básicos.

**Feedback recebido:**
- "Gostei que já tem 3 perfis separados, parecia caro fazer isso." — persona Carla Mendes (coordenação fictícia)
- "Texto de erro do login está em português, ótimo."
- Pedido: incluir uma frase explicando o sistema no login. **Acolhido** — texto adicionado no template.

## Sprint Retrospective

| O que foi bem | O que pode melhorar | Ações |
|---|---|---|
| Decisões técnicas fechadas cedo, sem retrabalho | Subestimamos tempo dos ADRs | Definir template padrão para ADRs (feito) |
| Documentação caminhou junto com código | Falta de ferramenta de protótipo visual | Para Sprint 02, alinhar wireframes simples antes |
| Discovery rendeu mais que o esperado | Backend (Gean) acumulou tarefas em paralelo a docs | Daily mais focada por papel |

## Incremento entregue

- Projeto Django rodando localmente (`runserver`).
- Login/logout funcionais.
- Modelos `PerfilUsuario` + auto-criação via signal.
- Documentação: 4 ADRs, Matriz, Discovery Log, Evidências, C4-Contexto, C4-Containers.
- Estrutura visual base com tipografia Inter, paleta neutra + acento esmeralda.
