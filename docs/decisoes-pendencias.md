# Update — Pontos em aberto fechados (2026-06-30)

## ADR-004 (novo): Deduplicação de movimentações

**Decisão:** chave de dedup = hash(`data_hora` + `codigo_movimento` + `nome_movimento` + `ordem_no_payload`).

- `codigo_movimento` vem do campo `movimentos.codigo` (TPU), mais estável que o nome textual.
- `ordem_no_payload`: posição do item no array `movimentos` retornado naquela consulta, usado como
  desempate para movimentos idênticos no mesmo timestamp (decisões em lote).
- **Validar no S0** com dados reais antes de fechar definitivamente — hipótese de design, não fato confirmado.

## ADR-005 (novo): Autenticação API DataJud — CONFIRMADO

- Autenticação via **API Key pública única**, fornecida pelo CNJ/DPJ, no header:
  `Authorization: APIKey [Chave Pública]`
- Chave global, não por tribunal nem por usuário. Pode ser alterada pelo CNJ a qualquer momento, sem
  aviso prévio formal — a chave vigente fica sempre na wiki oficial.
- **Implicação de arquitetura:** uma única variável de ambiente (`DATAJUD_API_KEY`). Adicionar
  healthcheck/alerta para erro 401 nas tasks Celery, já que a chave pode mudar sem notificação.
- Fonte oficial: https://datajud-wiki.cnj.jus.br/api-publica/acesso/

## Resolução tribunal → endpoint — PARCIALMENTE FECHADO

- Lista completa dos 91 endpoints/aliases obtida do tutorial oficial CNJ (anexo II) — ver
  `tribunal_endpoints.py` gerado nesta sessão.
- **Gap identificado:** o tutorial da API só lista os *aliases* (ex: `tjsp`, `trt3`), não a tabela de
  códigos numéricos `J.TR` do número CNJ que mapeia para esses aliases. Essa tabela vem de outra fonte
  (Resolução CNJ nº 65/2008, estrutura da Numeração Única) e precisa ser localizada e validada
  separadamente no S0/S1.
- Possível typo no tutorial oficial: alias `trt15` aparece duplicado para 15ª e 16ª região — provável
  que TRT16 seja `api_publica_trt16`, mas **não confirmado**, validar com chamada real no S0.

## raw_payload — sem mudanças, já fechado anteriormente.

---

**Próxima ação:** ainda falta fechar a tabela J.TR → tribunal antes do S1 (não bloqueia o S0/spike,
que pode rodar direto contra o endpoint `tjsp` fixo).
