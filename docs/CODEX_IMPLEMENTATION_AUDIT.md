# Codex Implementation Audit

Date: 2026-04-09
Repository: `/home/fg/library-platform`

## Current State Summary

The repository already contains the intended product shape:

- Django backend with modular apps for accounts, institutes, scholars, library, ingestion, knowledge, skills, Q&A, providers, analytics, and common utilities.
- Next.js frontend with a solid visual shell, auth pages, dashboard shell, and chat shell.
- Basic deployment assets under `infra/`.

The repo is not yet wired end to end. The strongest completed area is authentication. Most domain apps have models and migrations, but almost all runtime layers are still missing.

## What Is Already Good

- Custom user model exists and basic register/login endpoints already issue JWTs.
- Core domain models already exist for institutes, scholars, books, chunks, references, upload sessions, skill packs, and Q&A logs.
- Settings already include DRF, JWT, Celery, Redis, CORS, Whitenoise, and production host defaults.
- Frontend design direction is coherent, custom, and usable as a base for v1.
- Deployment intent is already separate from Frappe/bench and points at `library.digigalaxy.cloud`.

## Main Gaps Found

### Backend runtime gaps

- `institutes`, `scholars`, `library`, `ingestion`, `knowledge`, `skills`, `analytics`, and `ai_providers` have empty `urls.py`.
- Most apps are missing `serializers.py`, `views.py`, `services.py`, and `tasks.py`.
- `qa_engine` has only a small keyword-match chat flow and no structured grounded-answer pipeline.
- AI provider adapters are defined inside `models.py` and all runtime methods are still `pass`.
- Role and institute permission helpers exist but are incomplete and use brittle assumptions.
- API responses do not yet have a consistent error shape.

### Data model gaps

- `knowledge`, `analytics`, and `ai_providers` have models but no migrations in the repo.
- `knowledge.KnowledgeObject` is too thin for book-linked concept/rule/example retrieval.
- `analytics.Metric` is too minimal for meaningful event logging or dashboard counters.
- Provider selection supports DB lookup only; system default env-backed fallback is not wired.

### Ingestion gaps

- Upload session models exist, but there is no usable API, no job orchestration service, and no Celery tasks.
- No practical text extraction flow exists yet.
- There is no honest OCR fallback path for scanned PDFs.

### Frontend gaps

- Auth context is still a stub and does not fetch `/me`, refresh tokens, or guard routes.
- Dashboard is static.
- Library, upload, scholar, and institute product flows are missing.
- Chat UI exists, but it only targets the current thin Q&A endpoint.
- Root layout is not yet RTL-aware or auth-provider aware.

### Deployment/runtime gaps

- Existing systemd files use placeholder usernames and paths instead of `/home/fg`.
- Nginx config is close, but needs consolidation around the real split:
  - Next.js frontend
  - Django API/admin/static/media
  - large PDF uploads
  - no interference with the VPS's existing Frappe setup
- Deployment docs are generic and not yet exact for this VPS target.

### Testing gaps

- Test scaffolding exists, but critical business-flow coverage is still missing.

## Local Worktree Notes

The worktree is already dirty before this implementation:

- Modified:
  - `backend/apps/qa_engine/urls.py`
  - `frontend/components/AuthCard.tsx`
  - `frontend/components/DashboardStudio.tsx`
  - `frontend/components/PanelShell.tsx`
- Untracked:
  - `URDU_APP_INTRODUCTION.md`
  - `backend/apps/qa_engine/serializers.py`
  - `backend/apps/qa_engine/views.py`
  - `frontend/app/chat/`
  - `frontend/components/ChatWorkspace.tsx`

Those files should be treated carefully and not blindly reverted.

## Practical V1 Recommendation

Build v1 around the existing models and keep the implementation honest:

- Use DB-backed retrieval over `BookChunk` and `BookReference`.
- Return safe insufficient-evidence responses when grounding is weak.
- Implement upload plus metadata plus ingestion lifecycle first.
- Keep scholar review and institute permissions minimal but real.
- Expose enough frontend routes to make the main user journey runnable:
  - auth
  - dashboard
  - library browse/detail
  - upload
  - grounded Q&A
  - scholar basics
  - institute basics

## Expected Schema Work

New migrations are likely necessary for:

- `ai_providers`
- `knowledge`
- `analytics`

Additional small schema changes may be needed only if the current models cannot cleanly support the required v1 runtime.
