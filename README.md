# Kapruka Gift Agent

Production-oriented Gift Concierge for [Kapruka.com](https://www.kapruka.com): preference-aware recommendations, catalog RAG, Sri Lankan district delivery checks, and a Draft → Critique → Revise safety loop.

This repository is being built in phases. **Phase 1 (project setup) is complete.** Later phases are stubbed so the folder contract is stable.

## Current status

| Phase | Scope | Status |
| --- | --- | --- |
| 1 | Folder structure, config, logging, tokens, helpers | Done |
| 2 | Playwright crawler → `data/catalog.json` | Not started |
| 3 | Short-term, Qdrant RAG, recipient profiles | Not started |
| 4 | Intent router + catalog/logistics specialists | Not started |
| 5 | Reflection loop (draft / critique / revise) | Not started |
| 6 | Custom Python orchestration loop | Not started |
| 7 | FastAPI for the Next.js client | Not started |
| 8 | Next.js concierge UI | Scaffold only |
| 9 | Evaluation metrics | Scaffold only |

Hard constraint: no LangGraph, CrewAI, AutoGen, or other multi-agent frameworks. Orchestration is a custom Python control loop.

## Prerequisites

- Python 3.11+
- Node.js 18.17+ (frontend, Phase 8)
- Docker (optional, for local Qdrant in Phase 3)

## Setup (Phase 1)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Fill `OPENAI_API_KEY` and other values in `.env`. Secrets must never be hardcoded.

Run utility tests:

```bash
pytest backend/tests/test_utils.py
```

## Layout

See `docs/architecture.md`. Backend code lives under `backend/src`. The FastAPI app lives under `backend/api`. The Next.js app lives under `frontend/`.

## License

Private / portfolio project. Not affiliated with Kapruka.com except as a domain-focused demo.
