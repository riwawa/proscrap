# Painel de Monitoramento Processual (Proscrap)

Um painel que permite cadastrar números de processo (padrão CNJ) e acompanhar automaticamente novas movimentações, consultando periodicamente.

https://github.com/user-attachments/assets/b3ff6470-6325-492f-8695-15b5223ce4af

## Estrutura

```
api/            # Backend FastAPI + Celery + PostgreSQL
  app/
    core/       # config, database, mapeamento de tribunais
    models/     # SQLAlchemy (Processo, Movimentacao, ConsultaLog)
    schemas/    # Pydantic
    services/   # DataJudClient, dedup
    api/routes/ # Rotas REST
    tasks/      # Celery (placeholders até S3)
  spike/        # Script isolado do S0 — NÃO faz parte da app
  alembic/      # Migrations (a popular no S1)

web/            # Frontend Next.js (placeholder mínimo até S4/S5)
  lib/api.ts    # Cliente HTTP para o backend
```
## Rodando o spike (S0)

```bash
cd api
pip install httpx
DATAJUD_API_KEY="<chave-da-wiki-cnj>" \
NUMERO_PROCESSO="00008323520184013202" \
TRIBUNAL_ALIAS="tjsp" \
python spike/consulta_real.py
```

A chave vigente está sempre em: https://datajud-wiki.cnj.jus.br/api-publica/acesso/

## Subindo dependências locais (Postgres + Redis)

```bash
docker compose up -d
cp api/.env.example api/.env
# editar api/.env com a DATAJUD_API_KEY
```

## Backend (após o S1, quando o CRUD estiver pronto)

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend (após o S4)

```bash
cd web
npm install
cp .env.local.example .env.local
npm run dev
```
