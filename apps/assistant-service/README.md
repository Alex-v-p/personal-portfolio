# assistant-service

FastAPI service for the portfolio assistant.

## Current behavior

- reads indexed portfolio content from `knowledge_documents` and `knowledge_chunks`
- stores conversations in the shared PostgreSQL database
- supports a default `mock` provider mode for local development
- can be pointed at Ollama or an OpenAI-compatible / vLLM-style endpoint later
- Docker Compose now starts the Ollama container by default, but the assistant still uses `mock` unless you set `ASSISTANT_PROVIDER_BACKEND=ollama`

## Useful environment variables

- `ASSISTANT_PROVIDER_BACKEND=mock|ollama|openai-compatible`
- `ASSISTANT_PROVIDER_MODEL=qwen2.5:3b`
- `ASSISTANT_PROVIDER_BASE_URL=http://ollama:11434`
- `ASSISTANT_PROVIDER_API_KEY=`

## CMS workflow

The portfolio CMS rebuilds the assistant knowledge index through the portfolio API. After content changes, use the **Assistant** tab in the CMS to rebuild the searchable index.


Notes:
- Docker Compose reads the root `.env` file for the assistant container. Changing only `apps/assistant-service/.env` will not change the container's backend when running through Compose.
- With the Ollama backend enabled, successful generation requests show up as `POST /api/chat` in the Ollama logs. Embedding requests show up as `POST /api/embed`.
