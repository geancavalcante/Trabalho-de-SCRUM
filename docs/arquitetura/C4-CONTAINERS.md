# C4 — Nível 2: Containers

Abrimos a caixa preta do "Helpdesk Labs" do nível anterior. Cada container é uma unidade de runtime independente.

## Diagrama (Mermaid)

```mermaid
flowchart LR
    Browser["<b>Navegador do usuário</b><br/>(Chrome/Firefox/Edge,<br/>desktop e mobile)"]

    subgraph Render["<b>Render Free Tier</b>"]
        Web["<b>Aplicação Web</b><br/>Django 5 + Gunicorn<br/>Templates + Forms + ORM"]
        DB[("<b>Banco de Dados</b><br/>PostgreSQL (prod)<br/>SQLite (dev)")]
        Media[("<b>Armazenamento de anexos</b><br/>Volume local /media<br/>(efêmero no free tier)")]
        Logs[("<b>Logs</b><br/>arquivo /logs/app.log")]
    end

    Browser -- "HTTPS<br/>(Let's Encrypt)" --> Web
    Web -- "SQL via ORM" --> DB
    Web -- "FileField" --> Media
    Web -- "Python logging" --> Logs
```

## Containers

| Container | Tecnologia | Responsabilidade | Comunicação |
|---|---|---|---|
| **Aplicação Web** | Python 3.11+, Django 5, Gunicorn (prod) / runserver (dev) | Renderiza templates, valida formulários, aplica RBAC, expõe `/admin/` | HTTP/HTTPS para o navegador; SQL para o banco; sistema de arquivos para anexos e logs |
| **Banco de Dados** | PostgreSQL 15 (prod) / SQLite 3 (dev) | Persiste usuários, perfis, chamados, comentários, histórico, laboratórios | Driver `psycopg` (prod) ou `sqlite3` builtin (dev) |
| **Armazenamento de anexos** | Sistema de arquivos local (`MEDIA_ROOT`) | Guarda uploads de chamados | Acesso direto via `FileField.upload_to="anexos/"` |
| **Logs** | Sistema de arquivos local (`logs/app.log`) | Trilha de auditoria de eventos relevantes (login, criação, mudança de status, atribuição) | Logger `chamados` + `django.security` via handler `FileHandler` |

## Componentes principais da Aplicação Web (preview do nível 3 — Componentes)

| Componente | Caminho | Função |
|---|---|---|
| `chamados.models` | `src/chamados/models.py` | Modelos `PerfilUsuario`, `Laboratorio`, `Chamado`, `Comentario`, `HistoricoStatus` |
| `chamados.views` | `src/chamados/views.py` | Dashboard, lista, detalhe, criação, atribuição, mudança de status, relatórios |
| `chamados.forms` | `src/chamados/forms.py` | Validação de chamado, anexo, comentário, atribuição |
| `chamados.permissions` | `src/chamados/permissions.py` | `perfil_required`, `chamados_visiveis_para`, `pode_alterar_status`, `pode_comentar` |
| `chamados.signals` | `src/chamados/signals.py` | Cria `PerfilUsuario` automaticamente ao criar `User` |
| `chamados.admin` | `src/chamados/admin.py` | Painel admin nativo do Django |
| `chamados.management.commands.seed` | `src/chamados/management/commands/seed.py` | Popular dados de demonstração |

## Fluxos típicos

### Solicitante abre chamado

```mermaid
sequenceDiagram
    autonumber
    actor S as Solicitante
    participant V as views.criar_chamado
    participant F as forms.ChamadoForm
    participant M as models.Chamado
    participant H as models.HistoricoStatus

    S->>V: POST /chamados/novo/ (dados + anexo opcional)
    V->>F: instancia + valida (extensão e tamanho do anexo)
    F-->>V: cleaned_data OK
    V->>M: save(solicitante=request.user)
    V->>H: create(de_status="", para_status="NOVO")
    V-->>S: redirect /chamados/<id>/
```

### Técnico altera status

```mermaid
sequenceDiagram
    autonumber
    actor T as Técnico
    participant V as views.detalhe_chamado
    participant P as permissions.pode_alterar_status
    participant M as models.Chamado
    participant H as models.HistoricoStatus

    T->>V: POST /chamados/<id>/ (acao=mudar_status)
    V->>P: pode_alterar_status(user, chamado)?
    P-->>V: True (tecnico==user)
    V->>M: status=NOVO_STATUS, concluido_em=now() se CONCLUIDO
    V->>H: create(de_status=anterior, para_status=NOVO_STATUS, autor=user)
    V-->>T: redirect /chamados/<id>/
```

## Restrições visíveis neste nível

- Sem cache distribuído (Redis/Memcached) — desnecessário em volume MVP.
- Sem fila de jobs (Celery) — todas as operações são síncronas.
- Anexos no disco local: aceitável em piloto; migrar para object storage em v2 (consequência aceita em ADR-004).
