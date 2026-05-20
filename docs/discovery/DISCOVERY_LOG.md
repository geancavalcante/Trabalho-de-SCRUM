# Discovery Log

Registro das descobertas do squad durante a fase de Discovery (Sprint 1) e refinamentos ao longo das Sprints 2–4. Convenção: ID sequencial, evidência referenciando `EVIDENCIAS.md`, confiança em escala Baixa/Média/Alta.

| ID | Descoberta | Evidência | Impacto no projeto | Confiança | Como validar melhor |
|---|---|---|---|---|---|
| D01 | Pedidos chegam por WhatsApp pessoal, e-mail funcional e visitas presenciais — sem um único canal | E1 (entrevista coordenação) | Justifica criar canal único; impacta US01–US04 e a métrica "% chamados registrados" | Alta | Mapear 1 semana de pedidos por canal antes do go-live |
| D02 | Não há registro do que foi atendido — coordenação não consegue dizer quantos chamados houve no semestre | E1 + E2 (observação) | Histórico imutável é parte do MVP (não opcional); justifica modelo `HistoricoStatus` | Alta | Comparar registros físicos do livro de protocolo com sistema |
| D03 | Categoria "Projetor/Multimídia" é a mais frequente segundo o coordenador, seguida de "Rede" | E1 | Justifica priorização visual no relatório por categoria | Média | Validar com dados reais após 30 dias de uso |
| D04 | Solicitantes não conhecem termos técnicos — não sabem diferenciar "hardware" de "software" em casos limítrofes | E1 + E3 (benchmark GLPI/osTicket) | Categoria "Outros" obrigatória; UI deve ter dica curta por categoria | Média | Teste de usabilidade com 3 alunos voluntários |
| D05 | Equipe técnica é pequena (2 técnicos + coordenador) — atribuição manual basta | E1 | Não precisamos de auto-assign nesta versão; reduz escopo | Alta | Reavaliar quando time crescer ou volume passar de 200 chamados/mês |
| D06 | Coordenação precisa cancelar chamados duplicados ou improcedentes — não basta concluir | E1 | Status "Cancelado" obrigatório (separado de "Concluído") | Alta | Confirmar regra de visibilidade pós-cancelamento |
| D07 | Anexos são comuns (foto do problema), mas nem sempre estão disponíveis | E1 | Anexo precisa ser opcional, com validação de extensão e tamanho | Alta | Auditar tipos de anexos enviados nos primeiros 30 dias |
| D08 | Ferramentas como GLPI/osTicket/Zammad cobrem o caso, mas exigem infra dedicada (PHP/MySQL ou Java) | E2 (benchmark) | Justifica construir um app Django enxuto, controlando o escopo | Alta | Reavaliar adoção de GLPI em versão futura quando escopo crescer |
| D09 | Coordenação precisa medir "tempo médio de atendimento" — métrica solicitada por direção acadêmica | E1 + E3 | Justifica campo `concluido_em` no modelo e cálculo no relatório | Alta | Cruzar com SLA proposto em iteração futura |
| D10 | Maioria dos solicitantes acessa por celular — coordenação acessa por desktop | E1 | Layout precisa ser mobile-first; tabela de relatórios pode ser desktop-only | Alta | Smoke test em viewport 360px |
| D11 | LGPD aplicada — apenas dados estritamente necessários | E3 (escopo) | Não coletar CPF nem matrícula; só username + email institucional | Alta | Revisar com NTI antes de go-live |
| D12 | Free tier do Render derruba o servidor após 15 min de inatividade — primeiro hit do dia é lento | E2 | Aceitável para MVP institucional (uso de manhã); documentar em ADR-004 | Alta | Medir cold start em janela real de uso |

**Observação:** descobertas marcadas como confiança "Média" precisam de validação real em piloto. As "Altas" foram corroboradas por mais de uma fonte.
