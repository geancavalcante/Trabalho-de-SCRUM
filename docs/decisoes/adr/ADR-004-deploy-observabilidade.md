# ADR-004 — Deploy e Observabilidade

- **Status:** Aceito
- **Data:** 2026-02-15
- **Decisores:** Gean Feitosa Cavalcante (PO + Dev Backend), Kauê do Nascimento Silva (SM + QA/Doc), Tony Gabriel Alencar Alves (Dev Frontend)

## Contexto

O escopo exige um MVP "no ar" sem custo em licenças/infra. Volume estimado é baixíssimo no piloto (poucas dezenas de chamados/semana). Não há requisito de SLA agressivo, e a janela de uso é tipicamente diurna (8h–22h).

## Decisão

- **Deploy:** **Render free tier** (web service + PostgreSQL grátis), com deploy automático a partir de pushes na branch `main`.
- **Observabilidade no MVP:** **logging Django para arquivo** (`logs/app.log`) com formato verboso, capturando criação de chamado, mudança de status, atribuição e eventos de segurança (`django.security`).
- **Métricas:** vista de "Relatórios" coletando agregados básicos (volume por categoria/laboratório/status, tempo médio de atendimento).

## Alternativas consideradas

- **Railway free tier:** equivalente; perdeu por margem pequena na ergonomia de deploy do Django.
- **Fly.io:** ótimo, mas exige Dockerfile e CLI; adiciona setup.
- **VPS DigitalOcean básico:** US$ 4–6/mês fere a restrição de R$ 0.
- **Heroku:** não tem mais free tier confiável.
- **Sentry para monitoramento de erros:** desejável; ficou marcado como evolução pós-MVP para não estourar prazo.

## Justificativa

- Render entrega Django + PostgreSQL prontos no free tier com deploy via git push.
- Logging em arquivo é suficiente para o MVP (volume baixo) e cumpre o requisito de auditoria (ASVS V7 — Error Handling and Logging).
- Render entrega HTTPS por padrão (Let's Encrypt) — atende ASVS V9 (transport security) sem esforço.

## Consequências positivas

- Custo zero.
- Deploy contínuo a partir do main.
- HTTPS automático.
- Logs persistidos para auditoria local.

## Consequências negativas

- Free tier do Render hiberna após 15 minutos de inatividade → **cold start** de ~30s no primeiro hit do dia. Aceitável no contexto institucional.
- Logs em arquivo único exigem rotação manual em médio prazo. Aceitável até ~30 dias.
- Sem coleta de métricas operacionais (APM/uptime) no MVP.

## Riscos e mitigação

- **Risco:** instância dorme → primeiro acesso lento. **Mitigação:** documentar no README + considerar ping cron na v2.
- **Risco:** queda do disco efêmero do Render apaga `media/` e `logs/`. **Mitigação:** documentar — no MVP isso é aceitável; em v2, migrar `media/` para S3-compatible storage e logs para Logtail/Better Stack.
- **Risco:** PostgreSQL free tier expira/limita em 90 dias. **Mitigação:** documentar plano de rotação e/ou export periódico.

## Referências

- Render free tier: https://render.com/pricing
- Django logging: https://docs.djangoproject.com/en/5.0/topics/logging/
- OWASP ASVS V7 (Logging) e V9 (Transport)
- Sentry (futuro): https://sentry.io/welcome/
