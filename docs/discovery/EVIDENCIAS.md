# Evidências de Discovery

Cada evidência é referenciada no `DISCOVERY_LOG.md` pelos IDs E1, E2 e E3.

---

## E1 — Entrevista fictícia com a Coordenação de TI

**Tipo:** Entrevista semi-estruturada
**Data simulada:** 2026-02-12
**Participantes:** Coordenadora de TI (persona "Carla Mendes", interlocutora fictícia) + Scrum Master (Kauê) + PO (Gean)
**Duração:** 45 minutos

**Roteiro aplicado:**
1. Como vocês recebem pedidos hoje?
2. Quantos chamados acontecem por semana, aproximadamente?
3. Quem decide quem atende?
4. Onde isso fica registrado?
5. O que vocês não conseguem responder hoje à direção?

**Principais achados:**
- "A gente recebe por tudo: WhatsApp, e-mail e até gente que vem aqui na sala" — corrobora D01.
- "Não consigo dizer quantos chamados tivemos no semestre passado" — D02 e D09.
- "Projetor é o que mais quebra. Depois é rede. Hardware varia" — D03.
- "Aluno não sabe o nome técnico do problema, ele descreve o sintoma" — D04, justifica categoria "Outros" e dicas.
- "Eu prefiro atribuir manualmente. São só dois técnicos" — D05.
- "Tem vezes que o aluno abriu errado e eu preciso cancelar, não fechar" — D06, justifica status "Cancelado".
- "Foto ajuda demais, mas nem todos mandam" — D07, anexo opcional.
- "Direção quer saber se a operação está fluindo" — D09, métricas no relatório.

**Limitações:** entrevista fictícia simulada para fins do trabalho acadêmico. Em projeto real, recomenda-se replicar com a coordenação real e gravar a sessão (com consentimento).

---

## E2 — Benchmark de ferramentas similares

**Tipo:** Comparativo de ferramentas open source / free tier
**Data simulada:** 2026-02-13

Avaliamos três ferramentas reconhecidas no espaço de Service Desk para validar se "comprar pronto" derrotaria "construir":

| Ferramenta | Stack | Custo | Por que não adotamos para o MVP |
|---|---|---|---|
| **GLPI** | PHP/MySQL | Open source, $0 | Cobre o caso, mas exige infra dedicada (Apache/PHP), tem curva e excede o escopo de aprendizado da disciplina. Avaliado para v2. |
| **osTicket** | PHP/MySQL | Open source, $0 | Mais simples que GLPI, mas com interface datada e foco em e-mail-to-ticket, não na fila multi-perfil que precisamos. |
| **Zammad** | Ruby on Rails, Elasticsearch, Postgres | Open source, $0 self-hosted | Excelente produto, mas stack pesada (Rails + ES) inviável no free tier proposto. |

**Conclusão:** Para o **MVP acadêmico** com prazo de 4 sprints, time pequeno e domínio Django, **construir** é mais barato (em tempo e infra) do que **adotar e adaptar**. Para um cenário de produção em larga escala, GLPI deveria ser reavaliado.

**Fontes consultadas:**
- GLPI Project, documentação oficial (glpi-project.org)
- osTicket Documentation
- Zammad Docs (zammad.org/documentation)

---

## E3 — Documento de escopo da disciplina

**Tipo:** Documento de requisitos institucionais
**Referência:** [`/core/escopo.md`](../../core/escopo.md) e `/core/escopo.pdf` (versão original)
**Autor:** Coordenação ARA0152 — UNIFACIMP, 2026.1

**Pontos do escopo que viraram requisito:**
- 3 perfis (solicitante / técnico / coordenador) → US01, US06, US09.
- Categorias e status definidos → modelo `Chamado`.
- Restrição R$ 0 em licenças → motiva ADR-001, ADR-002, ADR-004.
- 4 sprints × 1 semana → cronograma e SPRINT-0X.md.
- Segurança mínima (auth, RBAC, validação, logs) → ADR-003 + ASVS_CHECKLIST_MINIMO.
- LGPD / dados mínimos → D11.
- Métricas básicas exigidas no relatório → US12.

Este documento é a fonte mais forte do projeto: em caso de conflito com qualquer outra evidência, ele prevalece.
