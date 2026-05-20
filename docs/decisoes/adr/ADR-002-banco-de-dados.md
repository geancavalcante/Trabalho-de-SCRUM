# ADR-002 — Banco de Dados

- **Status:** Aceito
- **Data:** 2026-02-14
- **Decisores:** Gean Feitosa Cavalcante (PO + Dev Backend), Kauê do Nascimento Silva (SM + QA/Doc), Tony Gabriel Alencar Alves (Dev Frontend)

## Contexto

O sistema é relacional por natureza (usuário, perfil, chamado, comentário, histórico, laboratório) e exige integridade referencial. Os dados são modestos em volume (estimado < 5.000 chamados/ano no campus). Restrição: R$ 0 em licenças.

## Decisão

- **Dev/local:** **SQLite** (default do Django).
- **Produção:** **PostgreSQL** no free tier do provider de deploy (Render).

## Alternativas consideradas

- **PostgreSQL desde o desenvolvimento via Docker:** mais próximo de produção, mas adiciona dependência de Docker para qualquer dev rodar localmente, custa tempo de setup que não temos em sprint curta.
- **MySQL:** equivalente a Postgres em capacidade, mas Postgres é o default oficial do Django e tem suporte melhor em provedores free tier.
- **MongoDB:** desnecessário; nossos dados são fortemente relacionais. Justificaria-se apenas se houvesse documentos heterogêneos.

## Justificativa

- SQLite tem **zero setup** local: arquivo único, vem com Python. Permite que qualquer dev clone e rode em < 5 minutos.
- O Django ORM abstrai o backend; trocar SQLite por PostgreSQL em prod é apenas mudar `DATABASES['default']['ENGINE']` + variáveis de ambiente.
- PostgreSQL é oferecido gratuitamente no Render/Railway no perfil hobby/free, atendendo a restrição de R$ 0.
- Em produção, PostgreSQL traz: melhor concorrência, índices avançados (GIN para JSON, full-text), backups gerenciados.

## Consequências positivas

- Onboarding ultra-rápido para devs do squad.
- Mesma base de código serve dev e prod.
- Nenhuma dependência local extra (Docker, MySQL server, etc.).

## Consequências negativas

- SQLite tem limites de concorrência (gravações serializadas) — irrelevante em dev.
- Diferenças sutis entre SQLite e PostgreSQL podem aparecer em queries muito específicas (case-sensitivity, tipos). **Mitigação:** rodar testes em PostgreSQL no CI antes de promover.
- Migrações e fixtures precisam ser testadas em ambos para garantir paridade.

## Riscos e mitigação

- **Risco:** divergência de comportamento entre dev e prod. **Mitigação:** documentação explícita no README + roteiro de smoke test em PostgreSQL antes de deploy.
- **Risco:** perda de dados no SQLite local (arquivo único). **Mitigação:** `db.sqlite3` está no `.gitignore`; documento de seed permite recriar dados.

## Referências

- Django docs — Databases: https://docs.djangoproject.com/en/5.0/ref/databases/
- Render Postgres free tier: https://render.com/docs/databases
- Matriz comparativa: [`../MATRIZ_DECISAO_TECNOLOGICA.md`](../MATRIZ_DECISAO_TECNOLOGICA.md)
