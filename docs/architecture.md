# Architecture — Kapruka Gift Agent

## Purpose

A gift concierge for Kapruka.com that remembers recipient preferences (especially nut-free), retrieves live catalog items with RAG, checks Sri Lankan district delivery, and runs a Draft → Critique → Revise safety loop before answering.

## Constraints

- Custom Python orchestration only (no LangGraph, CrewAI, AutoGen).
- Secrets live in `.env` only.
- Domain is Sri Lankan e-commerce / Kapruka.

## Runtime topology

```
Browser (Next.js App Router)
        │  HTTP JSON / SSE (Phase 7–8)
        ▼
FastAPI  (backend/api)
        │
        ▼
KaprukaGiftAgent  (backend/src/core/agent.py)
        ├── IntentRouter
        ├── CatalogSpecialist  → LongTermMemory (Qdrant RAG on catalog.json)
        ├── LogisticsSpecialist → DistrictMatcher
        ├── SemanticMemory     → data/recipient_profiles/*.json
        ├── ShortTermMemory    → session buffer
        └── Reflection: Drafter → Critic → Reviser
```

## Data

| Path | Role |
| --- | --- |
| `data/catalog.json` | Normalized product catalog from the Playwright crawler |
| `data/recipient_profiles/` | Semantic memory documents |
| Qdrant collections | Vector index of catalog (+ optional conversation memory) |

## Phase 1 (complete)

- Repository layout
- `Settings` via pydantic-settings
- Structured logging
- Token budgets
- Shared helpers (JSON, retry, districts)

Later phases fill crawler, memory, specialists, reflection, API, UI, and metrics.

The pre-development proposal PDF listed in the original tree is not generated here; keep any signed PDF alongside this document when available.
