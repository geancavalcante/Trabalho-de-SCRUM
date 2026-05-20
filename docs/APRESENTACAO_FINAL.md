# Apresentação Final — Helpdesk Labs

Sprint Review final da iteração #4, ARA0152 (UNIFACIMP, 2026.1).
Equipe: Gean Feitosa Cavalcante, Kauê do Nascimento Silva, Tony Gabriel Alencar Alves.

---

## 1. O problema

A Coordenação de TI do campus recebe pedidos de manutenção dos laboratórios por **WhatsApp, e-mail e visitas presenciais**. Sem padrão único, sem priorização, sem histórico, sem indicadores. Pedidos se perdem, técnicos não sabem o que está priorizado, e a direção não tem visibilidade.

## 2. A proposta — Helpdesk Labs

Sistema web responsivo, em Django, gratuito, com três perfis (Solicitante, Técnico, Coordenador) que cobre **abrir → triar → atender → fechar → medir**.

## 3. Demo (roteiro)

> Tempo previsto: 6 minutos.

1. **Login** com `solicitante1` (senha de demo `Demo@2026`).
2. **Abrir chamado** "Projetor não liga" — categoria Projetor/Multimídia, prioridade Alta, anexar foto.
3. Logout → login como `coordenador1`.
4. **Atribuir** o chamado ao `tecnico1` — status muda automaticamente para "Em andamento".
5. Logout → login como `tecnico1`.
6. **Comentar**: "Indo verificar fonte". **Mudar status** para "Concluído".
7. Logout → login como `coordenador1`.
8. **Tela de Relatórios**: totais por categoria, laboratório, status e tempo médio de atendimento.
9. Mostrar `logs/app.log` no terminal: trilha de auditoria.

## 4. O que entrou no MVP

- Login e RBAC com 3 perfis.
- Abertura de chamado com categoria, prioridade, laboratório, descrição e anexo opcional.
- Lista filtrada por perfil + filtros (status, prioridade, categoria).
- Detalhe com comentários + histórico imutável.
- Atribuição manual de técnico (com transição automática Novo → Em andamento).
- Relatório consolidado (volume + tempo médio).
- Logs de auditoria em arquivo.
- 3 testes automatizados cobrindo os fluxos críticos.

## 5. O que ficou fora (consciente)

- Notificações por e-mail (planejado v2).
- Login institucional via Microsoft/Google (Allauth v2).
- MFA / TOTP (v2).
- Auto-assign de técnico (não necessário com 2 técnicos).
- Dashboard agregado de SLA (v2 após coleta de dados reais).
- APM/Sentry (v2).

## 6. Decisões técnicas principais (com trade-offs)

| Decisão | Trade-off aceito |
|---|---|
| **Django + templates** (vs SPA) | Menos interatividade JS, em troca de velocidade de entrega |
| **SQLite dev → PostgreSQL prod** | Pequenas divergências entre engines, em troca de zero setup local |
| **Auth nativa Django** (vs Auth0/Allauth) | Sem login social, em troca de zero dependência externa |
| **Render free tier** | Cold start ~30s, em troca de R$ 0 |
| **Logging em arquivo** (vs Sentry/APM) | Sem alerta proativo, em troca de simplicidade no MVP |

Detalhes em [`/docs/decisoes/MATRIZ_DECISAO_TECNOLOGICA.md`](decisoes/MATRIZ_DECISAO_TECNOLOGICA.md) e nos 4 ADRs.

## 7. Métricas e indicadores

O sistema já coleta automaticamente:
- Volume por categoria, laboratório e status.
- Tempo médio de atendimento (em horas) para chamados concluídos.
- Trilha de eventos (criação, atribuição, mudança de status, login) em `logs/app.log`.

Métrica-chave do MVP: **% de chamados registrados no sistema** (vs. canais informais). Meta após 1 mês de uso: ≥ 90%.

## 8. Próximos passos (roadmap proposto)

1. **Piloto controlado** com a coordenação de TI por 30 dias, coletando feedback e medindo as métricas baseline.
2. **Notificações por e-mail** (mudança de status, atribuição) e SSO institucional.
3. **MFA** + lockout de força bruta (`django-axes`).
4. **Migração de anexos** para object storage compatível com S3 (evita perda em redeploy).
5. **Sentry / APM** para detecção proativa de erros.
6. **Dashboard de SLA** baseado em dados reais coletados no piloto.

## 9. Encerramento

O Helpdesk Labs entrega o mínimo necessário para **substituir os canais informais por um sistema único e auditável**, dentro das restrições do trabalho: R$ 0, 4 sprints, equipe de 5 alunos. Está pronto para piloto. As escolhas técnicas estão documentadas e podem ser refeitas com critério quando o contexto mudar.
