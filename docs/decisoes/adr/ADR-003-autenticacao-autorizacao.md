# ADR-003 — Autenticação e Autorização

- **Status:** Aceito
- **Data:** 2026-02-15
- **Decisores:** Gean Feitosa Cavalcante (PO + Dev Backend), Kauê do Nascimento Silva (SM + QA/Doc), Tony Gabriel Alencar Alves (Dev Frontend)

## Contexto

O sistema precisa de autenticação obrigatória (todas as views exceto login) e de controle de acesso baseado em três perfis (Solicitante, Técnico, Coordenador). Há também o usuário admin do Django (superuser) para administração e seed. Restrições: R$ 0, segurança mínima do ASVS L1, prazo curto.

## Decisão

Usar **autenticação nativa do Django** (`django.contrib.auth`) com um modelo `PerfilUsuario` em OneToOne com `User`, controle de acesso via decorator customizado `perfil_required(*tipos)` e filtros por perfil nas queries (helper `chamados_visiveis_para`).

## Alternativas consideradas

- **Auth0 / Clerk free tier:** robusto, mas adiciona dependência externa, integração JS pesada e curva de aprendizado.
- **Django Allauth (login social Google/Microsoft):** ótimo para campus com SSO institucional. Sai do escopo do MVP, mas pode ser adicionado em v2.
- **JWT custom + DRF:** desnecessário, não temos API pública nem cliente SPA.

## Justificativa

- A auth nativa do Django já implementa hash PBKDF2 (configurável para Argon2), proteção CSRF nas views, sessão segura via cookies, throttling de tentativas (com middleware adicional), validadores de senha (comprimento, dicionário comum, similaridade com username, complexidade).
- Padrão de mercado, documentação amplamente disponível.
- Permite controle de acesso em **dois eixos**:
  - **Vertical (por perfil):** decorator `perfil_required` impede acesso a URLs proibidas.
  - **Horizontal (por dono do registro):** queryset filtrado em `chamados_visiveis_para(user)` evita IDOR (Insecure Direct Object Reference).

## Consequências positivas

- Cumprimos ASVS L1 em autenticação sem código de criptografia próprio.
- Login/logout/views genéricas funcionam direto.
- O Admin do Django serve como painel administrativo "grátis" para o coordenador.
- Configurações de senha forte aplicadas: mínimo 8 caracteres + bloqueio de senhas comuns + verificação de similaridade.

## Consequências negativas

- Templates de login precisam ser estilizados manualmente (feito em `chamados/login.html`).
- Não temos MFA no MVP. Aceitável para o ambiente institucional inicial; planejável para v2.
- Sem login social institucional no MVP — usuários precisam de credenciais locais.

## Riscos e mitigação

- **Risco:** vazamento de credenciais por brute force. **Mitigação:** validadores de senha forte; em v2, adicionar `django-axes` para rate limit.
- **Risco:** IDOR ao acessar `/chamados/<id>/` de outro perfil. **Mitigação:** `chamados_visiveis_para(user)` no início da view de detalhe — testado por `test_tecnico_nao_ve_chamado_de_outro_tecnico`.
- **Risco:** session fixation. **Mitigação:** Django rotaciona o cookie de sessão após login (default).

## Referências

- Django Auth: https://docs.djangoproject.com/en/5.0/topics/auth/
- Django Password Validation: https://docs.djangoproject.com/en/5.0/topics/auth/passwords/
- OWASP ASVS v4.0 — Categoria V2 (Authentication) e V4 (Access Control)
- Checklist local: [`../../seguranca/ASVS_CHECKLIST_MINIMO.md`](../../seguranca/ASVS_CHECKLIST_MINIMO.md)
