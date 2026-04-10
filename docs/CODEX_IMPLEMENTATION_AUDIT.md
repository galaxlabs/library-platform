# Codex Implementation Audit

Date: 2026-04-09  
Repository: `/home/fg/library-platform`

## Snapshot

The repository already had a real v1 skeleton before implementation work started:

- backend apps, models, and migrations existed for all target domains
- DRF root routing was already mounted under `/api/v1/`
- the AI provider runtime had already been moved into `services.py`
- the ingestion app already had a practical first-pass extraction pipeline
- the Q&A app already had DB-backed retrieval and structured answer persistence

The actual missing runtime was narrower than the original brief implied. The biggest unfinished areas were shared scoping rules, frontend session wiring, product page wiring, and VPS deployment consolidation.

## What Was Missing Or Weak

### Backend

- auth worked, but user reads were too open for non-admin users and frontend-friendly `/me` consumption was still thin
- institute detail/list endpoints existed, but object scoping and manage-vs-read rules needed tightening
- scholar profile and review endpoints existed, but there was no queue surface for review-ready answers
- library upload worked, but the metadata contract was still too loose for a mandatory metadata form
- ingestion existed, but the handoff between “book uploaded” and “job queued” needed a clearer runtime step
- provider health/selection needed better institute resolution and safer request error wrapping
- analytics counters existed, but the dashboard payload was too minimal for a practical frontend overview

### Frontend

- the visual shell was good, but auth context was still a stub
- login/register were storing tokens directly without updating app state
- dashboard, library, upload, institute, and scholar flows were not connected to live APIs
- the Q&A page showed only a thin chat history instead of the structured grounded-answer object
- route protection and workspace navigation across product pages were missing

### Deployment

- systemd units used placeholder users and paths
- no dedicated `library-backend.service` / `library-celerybeat.service` pair existed
- nginx config needed a clean split for frontend, `/api/`, `/admin/`, static, media, and larger PDF uploads
- docs still described a generic server instead of the actual `/home/fg` VPS target

### Testing

- pytest scaffolding existed, but business-critical flow coverage was still missing

## Implementation Direction

The safest practical path for v1 was:

1. preserve the existing Django app boundaries and service-layer work already present
2. strengthen permissions, scoping, and API contracts instead of rewriting working models
3. wire the frontend to the existing DRF endpoints with small contract improvements
4. keep ingestion honest:
   - extract text when possible
   - mark OCR-needed PDFs clearly
   - never fabricate source-grounded content
5. keep Q&A DB-backed and traceable, not “fantasy RAG”

## Schema Notes

At audit time, migrations already existed for all backend apps, so large schema redesign was not justified. The focus should remain on runtime completion, not migration churn, unless a later test reveals a real schema blocker.
