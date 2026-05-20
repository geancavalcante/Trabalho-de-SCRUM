# Helpdesk Labs

> Sistema web de chamados de suporte/manutenção dos laboratórios de TI do campus.
> MVP acadêmico — Trabalho de PBL/Scrum, ARA0152 (UNIFACIMP, 2026.1).

## Problema resolvido

A Coordenação de TI recebia pedidos por WhatsApp, e-mail e visitas presenciais, sem padrão, priorização ou histórico. O Helpdesk Labs centraliza tudo num **canal único auditável**, com perfis distintos (Solicitante, Técnico, Coordenador), fila com status e prioridades, comentários, anexos, histórico imutável e relatório gerencial.

Resumo completo do projeto: [`docs/DOSSIE_DO_PROJETO.md`](docs/DOSSIE_DO_PROJETO.md).

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Django 5 (Python 3.11+) |
| Banco (dev) | SQLite |
| Banco (prod) | PostgreSQL (Render free tier) |
| Frontend | Templates Django + Bootstrap 5 (via CDN) |
| Auth | `django.contrib.auth` nativa + perfis customizados |
| Anexos | `MEDIA_ROOT` local (`media/`) |
| Logs | Arquivo (`logs/app.log`) |
| Testes | `django.test` |

Justificativa: [`docs/decisoes/MATRIZ_DECISAO_TECNOLOGICA.md`](docs/decisoes/MATRIZ_DECISAO_TECNOLOGICA.md) e ADRs em [`docs/decisoes/adr/`](docs/decisoes/adr/).

## Requisitos

- Python 3.11 ou superior (testado em 3.13)
- `pip` atualizado
- (Opcional, para exportar docs) `pandoc` + `xelatex`

## Instalação (passo a passo, dev local)

```powershell
# 1. Clonar o repositório
git clone https://github.com/geancavalcante/Trabalho-de-SCRUM.git
cd Trabalho-de-SCRUM

# 2. (Opcional, recomendado) criar virtualenv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r src/requirements.txt

# 4. Aplicar migrações e popular dados de demonstração
python src/manage.py migrate
python src/manage.py seed

# 5. Subir o servidor
python src/manage.py runserver
# acesse http://127.0.0.1:8000/
```

Em Linux/macOS, use `python3` e ative o venv via `source .venv/bin/activate`.

## Como criar usuário administrador

O `seed` já cria 3 usuários (ver abaixo). Para criar um superusuário adicional:

```powershell
python src/manage.py createsuperuser
```

Acesse o admin em `http://127.0.0.1:8000/admin/`.

## Como rodar testes

```powershell
python src/manage.py test chamados
```

Saída esperada: `Ran 3 tests in <s> OK`.

## Como acessar o sistema — Credenciais de demonstração

| Usuário | Perfil | Senha (apenas DEV) |
|---|---|---|
| `solicitante1` | Solicitante | `Demo@2026` |
| `tecnico1` | Técnico | `Demo@2026` |
| `coordenador1` | Coordenador | `Demo@2026` |

> **Atenção:** essa senha é só para ambiente local de demonstração. **Nunca** use em produção.

## Perfis e permissões

| Perfil | O que pode fazer |
|---|---|
| **Solicitante** | Abrir chamado, ver e comentar os próprios chamados |
| **Técnico** | Ver e comentar chamados atribuídos a si; alterar status |
| **Coordenador** | Ver todos os chamados, atribuir técnico, alterar status, cancelar, ver relatórios |

Implementação em [`src/chamados/permissions.py`](src/chamados/permissions.py).

## Fluxos principais (demo de 5 minutos)

1. Login como `solicitante1` → abrir chamado (categoria/prioridade/lab).
2. Logout → login como `coordenador1` → atribuir técnico ao chamado.
3. Logout → login como `tecnico1` → comentar e mudar status para "Em andamento" e depois "Concluído".
4. Logout → login como `coordenador1` → conferir `/relatorios/`.

## Backlog e Sprints

O backlog priorizado está no [Dossiê](docs/DOSSIE_DO_PROJETO.md#7-priorização-do-backlog--rice). Cada Sprint tem documento próprio:

- [Sprint 01 — Discovery + setup + auth](docs/sprints/SPRINT-01.md)
- [Sprint 02 — Abertura e fila](docs/sprints/SPRINT-02.md)
- [Sprint 03 — Atribuição, comentários, anexos](docs/sprints/SPRINT-03.md)
- [Sprint 04 — Relatórios, segurança, doc final](docs/sprints/SPRINT-04.md)

## Deploy básico (Render free tier)

1. Criar conta gratuita em [render.com](https://render.com/).
2. Novo **Web Service** apontando para o repo.
3. Build command: `pip install -r src/requirements.txt`.
4. Start command: `cd src && gunicorn config.wsgi`.
5. Adicionar variáveis de ambiente:
   - `DJANGO_SECRET_KEY` (gerar com `python -c "import secrets;print(secrets.token_urlsafe(50))"`)
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=<seu-app>.onrender.com`
6. Criar **PostgreSQL database** no Render e ligar via `DATABASE_URL` (ajuste `settings.py` se quiser usar `dj-database-url`).
7. Render emite HTTPS por padrão (Let's Encrypt).

> Free tier hiberna após 15 min — primeiro hit do dia leva ~30s. Detalhes em [ADR-004](docs/decisoes/adr/ADR-004-deploy-observabilidade.md).

## Como exportar documentação (PDF / DOCX)

Os documentos `.md` em `/docs/` podem ser convertidos para PDF ou DOCX com **pandoc**. Os scripts já estão preparados:

### Windows (PowerShell)

```powershell
# instalar pandoc: https://pandoc.org/installing.html
# para PDF, instalar MiKTeX: https://miktex.org/download
pwsh scripts/export_docs.ps1            # tenta PDF, cai para DOCX se faltar LaTeX
pwsh scripts/export_docs.ps1 -Force pdf
pwsh scripts/export_docs.ps1 -Force docx
```

### Linux/macOS

```bash
sudo apt install pandoc texlive-xetex   # ou equivalente
chmod +x scripts/export_docs.sh
./scripts/export_docs.sh
```

Os artefatos gerados (`docs/DOSSIE_DO_PROJETO.pdf`, `docs/APRESENTACAO_FINAL.pdf` ou `.docx`) não são versionados (`.gitignore`).

## Estrutura de pastas

```
/
├── README.md
├── .gitignore
├── core/                          # arquivos do trabalho (escopo, git_config)
├── docs/                          # documentação Scrum completa
│   ├── DOSSIE_DO_PROJETO.md
│   ├── APRESENTACAO_FINAL.md
│   ├── discovery/                 # DISCOVERY_LOG.md, EVIDENCIAS.md
│   ├── decisoes/                  # MATRIZ + 4 ADRs
│   ├── arquitetura/               # C4-CONTEXTO.md, C4-CONTAINERS.md
│   ├── seguranca/                 # ASVS_CHECKLIST_MINIMO.md
│   └── sprints/                   # SPRINT-01..04.md
├── scripts/
│   ├── export_docs.ps1
│   └── export_docs.sh
└── src/
    ├── manage.py
    ├── requirements.txt
    ├── config/                    # settings.py, urls.py, wsgi.py
    └── chamados/                  # app principal: models, views, forms, etc.
```

## Segurança — resumo

- Autenticação obrigatória em todas as views (exceto login).
- Controle de acesso por perfil (decorator) + por dono do registro (queryset filtrado).
- CSRF, XSS-escape, X-Frame-Options DENY, HTTPS forçado em produção.
- Senha mínima de 8 caracteres, validação contra dicionário comum.
- Validação de upload (whitelist de extensões + limite 5MB).
- Logs de eventos relevantes em `logs/app.log`.
- `git_config.json`, `db.sqlite3`, `media/`, `logs/` ignorados pelo Git.

Detalhes em [`docs/seguranca/ASVS_CHECKLIST_MINIMO.md`](docs/seguranca/ASVS_CHECKLIST_MINIMO.md).

## Licença

Trabalho acadêmico — uso educacional. Stack 100% open source.
