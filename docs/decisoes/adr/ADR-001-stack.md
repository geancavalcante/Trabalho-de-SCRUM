# ADR-001 — Stack / Framework

- **Status:** Aceito
- **Data:** 2026-02-14
- **Decisores:** Gean Feitosa Cavalcante (PO + Dev Backend), Kauê do Nascimento Silva (SM + QA/Doc), Tony Gabriel Alencar Alves (Dev Frontend)

## Contexto

Precisamos entregar um MVP funcional de sistema de chamados em 4 sprints de 1 semana, com orçamento R$ 0 em licenças, equipe de 5 alunos com domínio razoável de Python e iniciante em outras stacks. O sistema é web responsivo, monolítico, com auth, RBAC, formulário com upload, lista filtrável, persistência relacional e relatórios.

## Decisão

Adotar **Django 5.x** como framework único (backend + templates) para o MVP.

## Alternativas consideradas

- **FastAPI + frontend separado (React/Vue):** ótimo desempenho, mas exige escrever auth, admin, formulários, templates e build do frontend separados. Cabe em 4 sprints apenas para equipe sênior.
- **Flask + extensões (Flask-Login, Flask-WTF, Flask-Admin):** equivalente a remontar à mão o que o Django entrega pronto, com mais bibliotecas para manter.
- **Node.js (Express ou Next.js):** equipe não domina o ecossistema; risco alto em sprint curta.
- **Spring Boot:** maduro e seguro, mas curva alta para Python-first.

Comparação completa em [`../MATRIZ_DECISAO_TECNOLOGICA.md`](../MATRIZ_DECISAO_TECNOLOGICA.md).

## Justificativa

- O Django entrega "out of the box": ORM, auth, admin, sistema de templates, CSRF, migrations. Cobre 100% das nossas necessidades do MVP sem dependências adicionais relevantes.
- Squad já tem fluência em Python + Django (baseline de aprendizagem da disciplina).
- Templates server-rendered são mais rápidos de evoluir num MVP do que SPAs.
- Auth e RBAC nativos atendem o ASVS L1 sem precisar de provider externo.
- Curva de manutenção baixa: convenção forte e documentação oficial extensa.

## Consequências positivas

- Velocidade de implementação: o painel admin sai grátis e ajuda na demo.
- Segurança baseline alta sem esforço extra (CSRF, XSS-escape em templates, ORM parametrizado).
- Mesmo código funciona em SQLite (dev) e PostgreSQL (prod).

## Consequências negativas

- Templates server-rendered limitam interatividade rica sem JavaScript adicional. Aceitável para MVP.
- Acoplamento alto entre camadas (típico de Django) pode incomodar em refactors grandes. Não é problema em escala MVP.
- Performance bruta inferior a stacks assíncronas (FastAPI/Node). Não é gargalo no perfil de carga interno.

## Riscos e mitigação

- **Risco:** time tropeça em peculiaridades do ORM em queries de relatório. **Mitigação:** isolar agregações em funções nomeadas e testar.
- **Risco:** deploy do Django em free tier exige `whitenoise` ou similar. **Mitigação:** ADR-004 trata.

## Referências

- Documentação oficial: https://docs.djangoproject.com/en/5.0/
- "Two Scoops of Django" (Greenfeld, Roy-Greenfeld) — guia de boas práticas
- Matriz comparativa local: [`../MATRIZ_DECISAO_TECNOLOGICA.md`](../MATRIZ_DECISAO_TECNOLOGICA.md)
