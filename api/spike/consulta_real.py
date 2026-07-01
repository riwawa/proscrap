"""
SPIKE (S0) — script isolado, descartável, para validar a API DataJud com um
processo real do TJSP antes de fechar o schema de `movimentacoes` na app.

Não faz parte da app principal (não importar de app.*). Roda standalone.

Uso:
    DATAJUD_API_KEY="<chave>" NUMERO_PROCESSO="00008323520184013202" python spike/consulta_real.py

O que este script deve confirmar (objetivos do S0):
  1. A API Key pública funciona como documentado (Authorization: APIKey ...).
  2. A estrutura real de `movimentos[]` bate com o glossário oficial.
  3. Se existe algum campo de ID/sequência estável que sirva de desempate
     melhor que `ordem_no_payload` (ver ADR-004).
  4. Confirmar/corrigir o alias "trt16" (possível typo no tutorial oficial).
"""
import json
import os
import sys

import httpx

DATAJUD_API_KEY = os.environ.get("DATAJUD_API_KEY", "")
NUMERO_PROCESSO = os.environ.get("NUMERO_PROCESSO", "")
TRIBUNAL_ALIAS = os.environ.get("TRIBUNAL_ALIAS", "tjsp")

BASE_URL = "https://api-publica.datajud.cnj.jus.br"
ENDPOINT = f"{BASE_URL}/api_publica_{TRIBUNAL_ALIAS}/_search"


def main():
    if not DATAJUD_API_KEY:
        print("ERRO: defina a variável de ambiente DATAJUD_API_KEY.", file=sys.stderr)
        sys.exit(1)
    if not NUMERO_PROCESSO:
        print(
            "ERRO: defina NUMERO_PROCESSO (20 dígitos, sem formatação).",
            file=sys.stderr,
        )
        sys.exit(1)

    headers = {
        "Authorization": f"APIKey {DATAJUD_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {"query": {"match": {"numeroProcesso": NUMERO_PROCESSO}}}

    print(f"Consultando {ENDPOINT} para o processo {NUMERO_PROCESSO}...")
    response = httpx.post(ENDPOINT, headers=headers, json=body, timeout=15.0)

    print(f"Status: {response.status_code}")
    response.raise_for_status()

    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # Inspeção rápida dos movimentos, se existirem
    hits = data.get("hits", {}).get("hits", [])
    if not hits:
        print("\nNenhum resultado encontrado para esse número de processo.")
        return

    fonte = hits[0].get("_source", {})
    movimentos = fonte.get("movimentos", [])
    print(f"\n{len(movimentos)} movimentações encontradas. Primeiras 3:")
    for mov in movimentos[:3]:
        print(json.dumps(mov, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
