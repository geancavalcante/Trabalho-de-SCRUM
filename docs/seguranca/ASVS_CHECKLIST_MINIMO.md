# Checklist Mínimo de Segurança — OWASP ASVS v4 (Nível L1 aplicável ao MVP)

Selecionamos um subset prático do ASVS L1, cobrindo o que o MVP **deve** garantir. Cada controle inclui status, como está implementado e em que arquivo verificar.

| Categoria | Controle ASVS | Status | Implementação no Helpdesk Labs | Verificar em |
|---|---|---|---|---|
| **V2 — Autenticação** | V2.1.1 — Senhas com no mínimo 8 caracteres | OK | `MinimumLengthValidator min_length=8` | `src/config/settings.py` |
| | V2.1.7 — Validar senhas comuns | OK | `CommonPasswordValidator` (dicionário do Django) | `src/config/settings.py` |
| | V2.1.9 — Similaridade com username | OK | `UserAttributeSimilarityValidator` | `src/config/settings.py` |
| | V2.2.1 — Lockout de força bruta | A FAZER (v2) | Documentado: usar `django-axes` em v2 | ADR-003 |
| | V2.7.1 — Recuperação de senha sem MFA | A FAZER (v2) | Não há reset por e-mail no MVP | ADR-003 |
| **V3 — Sessão** | V3.2.1 — Sessão invalida no logout | OK | `LogoutView` rota `/logout/`, cookies HttpOnly | `src/config/settings.py` e `urls.py` |
| | V3.4.1 — Cookies com flag `HttpOnly` | OK | `SESSION_COOKIE_HTTPONLY=True`, `CSRF_COOKIE_HTTPONLY=True` | `src/config/settings.py` |
| | V3.4.3 — Cookies com `SameSite=Lax` | OK | `SESSION_COOKIE_SAMESITE='Lax'` | `src/config/settings.py` |
| | V3.7.1 — Sessão segura em HTTPS (prod) | OK | `SESSION_COOKIE_SECURE=True` quando `DEBUG=False` | `src/config/settings.py` |
| **V4 — Controle de Acesso** | V4.1.1 — Negar por padrão | OK | Todas as views usam `@login_required` ou `@perfil_required` | `src/chamados/views.py` |
| | V4.1.3 — Princípio do menor privilégio | OK | Decorator `perfil_required(*tipos)` restringe por papel | `src/chamados/permissions.py` |
| | V4.2.1 — IDOR (acesso indevido por ID) | OK | `chamados_visiveis_para(user)` aplicado no detalhe e na lista | `src/chamados/permissions.py` + view `detalhe_chamado` |
| **V5 — Validação de Entrada** | V5.1.3 — Sanitização contra XSS | OK | Django escapa por default em templates | Templates Django |
| | V5.1.5 — SQL Injection | OK | ORM parametrizado (não há SQL cru no projeto) | `src/chamados/views.py` |
| | V5.1.6 — CSRF | OK | Middleware `CsrfViewMiddleware` + `{% csrf_token %}` em todos os forms POST | Todos os templates |
| **V8 — Upload Seguro** | V12.4.1 — Validar extensão de upload | OK | `clean_anexo` valida whitelist de extensões | `src/chamados/forms.py` |
| | V12.4.2 — Limitar tamanho de upload | OK | Limite de 5MB via `MAX_ANEXO_BYTES` | `src/chamados/forms.py` |
| | V12.5.1 — Não executar uploads como código | OK | Arquivos servidos via `FileField` em `/media/`, sem execução | `src/config/urls.py` |
| **V7 — Logging** | V7.1.1 — Eventos de segurança registrados | OK | `LOGGING` captura `chamados` + `django.security` | `src/config/settings.py` |
| | V7.1.3 — Não registrar dados sensíveis | OK | Logs registram username e ID, não senhas ou tokens | `src/chamados/views.py` |
| **V9 — Transporte** | V9.1.1 — HTTPS | OK em prod | `SECURE_SSL_REDIRECT=True` quando `DEBUG=False`; HTTPS automático do Render | `src/config/settings.py` |
| | V9.1.3 — HSTS | OK em prod | `SECURE_HSTS_SECONDS=31536000` | `src/config/settings.py` |
| **V14 — Configuração** | V14.1.1 — `DEBUG=False` em prod | OK | Lê `DJANGO_DEBUG` da env (default `True` em dev) | `src/config/settings.py` |
| | V14.3.2 — Não expor segredos | OK | `SECRET_KEY` via env; `git_config.json` no `.gitignore` | `.gitignore` + `src/config/settings.py` |
| | V14.4.3 — Cabeçalho `X-Frame-Options` | OK | `X_FRAME_OPTIONS='DENY'` | `src/config/settings.py` |
| | V14.4.4 — `X-Content-Type-Options: nosniff` | OK | `SECURE_CONTENT_TYPE_NOSNIFF=True` | `src/config/settings.py` |

## Itens deliberadamente fora do escopo do MVP

- MFA / TOTP — planejado para v2.
- Login social institucional (Allauth + Microsoft/Google) — v2.
- Rate limit por IP / lockout de brute force — v2 (via `django-axes`).
- WAF — fica a cargo do provedor de hospedagem.
- Pentest formal — recomendado antes do go-live em produção real.

## Auditoria rápida (como verificar)

Em terminal, dentro do projeto:

```bash
python src/manage.py check --deploy  # diagnóstico de segurança para produção
python src/manage.py test chamados   # roda os 3 testes que cobrem RBAC e fluxo
grep -r "csrf_token" src/chamados/templates  # confere CSRF em todos os forms
```
