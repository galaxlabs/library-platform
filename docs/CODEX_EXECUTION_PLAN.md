# Codex Execution Plan

Date: 2026-04-09

## Order Of Work

1. stabilize shared backend behavior and API contracts
2. finish the remaining backend runtime seams
3. wire the frontend to live backend flows
4. consolidate deployment/runtime assets for the `/home/fg` VPS target
5. add critical tests and run local validation

## Concrete Work Items

### 1. Shared backend stabilization

- tighten shared permission helpers around institute access and institute management
- make account serialization safer for non-admin users
- keep `/api/v1/accounts/me/` as the frontend identity source
- improve provider resolution to use the user’s active institute context more reliably
- expand analytics payloads so the dashboard can be live instead of static

### 2. Domain runtime completion

- preserve current institute, library, ingestion, knowledge, skill, scholar, Q&A, and provider APIs where already present
- add missing runtime seams rather than redesigning:
  - scholar review queue basics
  - mandatory library metadata input
  - explicit upload-to-queued ingestion handoff
  - event logging on critical create actions
- keep ingestion honest for OCR-unready PDFs

### 3. Frontend wiring

- complete auth context:
  - login
  - register
  - logout
  - `/accounts/me/` bootstrap
  - token refresh retry
- add route protection for product pages
- replace static dashboard content with live analytics and user data
- add minimum functional pages for:
  - library list
  - library detail
  - upload wizard
  - grounded Q&A
  - scholar profile
  - institute overview
- keep the current visual language and RTL-first layout direction

### 4. Deployment/runtime consolidation

- add gunicorn config for backend production runs
- update frontend production config for a clean API base strategy
- create or update:
  - `infra/systemd/library-backend.service`
  - `infra/systemd/library-celery.service`
  - `infra/systemd/library-celerybeat.service`
  - `infra/systemd/library-frontend.service`
- update nginx template to proxy:
  - `/` to Next.js
  - `/api/` and `/admin/` to Django
  - static/media directly where appropriate
- document exact VPS steps for `/home/fg/library-platform`

### 5. Tests and verification

- add focused backend tests for:
  - registration/login/me
  - institute-scoped membership visibility
  - book creation and visibility
  - ingestion job creation
  - safe insufficient-support Q&A
  - provider selection hierarchy
- run the checks that are feasible in the current environment and record any remaining blockers
