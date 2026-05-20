# Matriz de Decisão Tecnológica

Avaliação de alternativas para as 4 decisões-chave do projeto. Cada critério tem peso; a nota é 1–5 (5 = melhor). Score final = Σ (nota × peso). Maior score vence.

## Critérios e pesos

| Critério | Peso | Justificativa do peso |
|---|---|---|
| Prazo (4 sprints curtas) | 5 | Restrição rígida do escopo |
| Domínio do time | 4 | Equipe fictícia composta majoritariamente por iniciantes em Python/Django, sem domínio profundo de outras stacks |
| Custo / licença | 5 | Restrição rígida: R$ 0 em licenças |
| Segurança | 4 | Requisito não-funcional explícito |
| Manutenibilidade | 3 | Importante mas não bloqueante para o MVP |
| Infra / compatibilidade free tier | 4 | Restrição de R$ 0 também afeta deploy |

---

## Decisão 1 — Stack / Framework

| Alternativa | Prazo (5) | Domínio (4) | Custo (5) | Segurança (4) | Manut. (3) | Infra (4) | Score |
|---|---|---|---|---|---|---|---|
| **Django** | 5 | 5 | 5 | 5 | 5 | 5 | **125** |
| FastAPI + frontend separado | 3 | 3 | 5 | 4 | 4 | 4 | 95 |
| Flask + extensões | 4 | 3 | 5 | 3 | 3 | 5 | 92 |
| Node.js (Express/Next) | 3 | 2 | 5 | 3 | 4 | 4 | 86 |
| Spring Boot | 2 | 2 | 5 | 5 | 4 | 3 | 84 |

**Vencedor: Django.** Bateu em todos os critérios pela combinação "tudo pronto" (ORM, auth, admin, templates) + domínio do time. Detalhe em [`adr/ADR-001-stack.md`](adr/ADR-001-stack.md).

---

## Decisão 2 — Banco de Dados

| Alternativa | Prazo | Domínio | Custo | Segurança | Manut. | Infra | Score |
|---|---|---|---|---|---|---|---|
| **SQLite (dev) + PostgreSQL (prod)** | 5 | 5 | 5 | 4 | 4 | 5 | **117** |
| PostgreSQL desde o dev (via Docker) | 3 | 3 | 5 | 5 | 5 | 4 | 99 |
| MySQL | 3 | 3 | 5 | 4 | 4 | 4 | 92 |
| MongoDB | 2 | 2 | 5 | 3 | 3 | 4 | 79 |

**Vencedor: SQLite (dev) + PostgreSQL (prod).** Setup zero em dev, ORM Django abstrai a troca, free tier de Render/Railway oferece PostgreSQL grátis. Detalhe em [`adr/ADR-002-banco-de-dados.md`](adr/ADR-002-banco-de-dados.md).

---

## Decisão 3 — Autenticação / Autorização

| Alternativa | Prazo | Domínio | Custo | Segurança | Manut. | Infra | Score |
|---|---|---|---|---|---|---|---|
| **`django.contrib.auth` + modelo `PerfilUsuario`** | 5 | 5 | 5 | 5 | 4 | 5 | **122** |
| Auth0 / Clerk free tier | 2 | 2 | 4 | 5 | 4 | 3 | 85 |
| Django Allauth (OAuth Google) | 3 | 3 | 5 | 5 | 4 | 4 | 96 |
| JWT custom + DRF | 2 | 2 | 5 | 4 | 3 | 4 | 81 |

**Vencedor: Auth nativa Django + perfis customizados.** Zero dependência, hash padrão PBKDF2 já cobre segurança L1, suficiente para o MVP. Detalhe em [`adr/ADR-003-autenticacao-autorizacao.md`](adr/ADR-003-autenticacao-autorizacao.md).

---

## Decisão 4 — Deploy / Observabilidade

| Alternativa | Prazo | Domínio | Custo | Segurança | Manut. | Infra | Score |
|---|---|---|---|---|---|---|---|
| **Render free tier + logging Django em arquivo** | 5 | 4 | 5 | 4 | 4 | 5 | **115** |
| Railway free tier | 4 | 4 | 4 | 4 | 4 | 5 | 105 |
| Fly.io | 3 | 3 | 4 | 4 | 4 | 4 | 92 |
| VPS DigitalOcean básico | 3 | 3 | 2 | 4 | 4 | 4 | 80 |
| Heroku | 4 | 3 | 1 | 4 | 4 | 5 | 84 |

**Vencedor: Render free tier.** Gratuito, deploy por push do git, suporta Django + PostgreSQL nativo. Cold start é aceitável para uso institucional. Detalhe em [`adr/ADR-004-deploy-observabilidade.md`](adr/ADR-004-deploy-observabilidade.md).

---

## Sumário

| Decisão | Vencedor | Score | Runner-up |
|---|---|---|---|
| Stack | Django | 125 | FastAPI (95) |
| Banco | SQLite dev → PostgreSQL prod | 117 | PostgreSQL desde dev (99) |
| Auth | Django auth nativa + perfis | 122 | Allauth (96) |
| Deploy | Render free tier | 115 | Railway (105) |

Todas as decisões respeitam as restrições do escopo: R$ 0 em licenças, 4 sprints e segurança mínima do ASVS L1.
