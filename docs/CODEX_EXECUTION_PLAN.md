# Codex Execution Plan

Date: 2026-04-09

## Implementation Order

1. Stabilize shared backend foundations
2. Complete backend v1 runtime by app
3. Wire frontend to the real APIs
4. Consolidate VPS deployment/runtime config
5. Add tests for critical flows
6. Update runbooks and environment templates

## Step 1: Shared backend foundations

- Add shared permission helpers for:
  - platform admin
  - institute admin
  - scholar
  - institute-scoped access
- Add shared queryset scoping helpers where practical.
- Add a consistent DRF exception shape.
- Add lightweight audit/event logging helpers usage in new flows.

## Step 2: Accounts

- Keep existing register/login behavior.
- Add:
  - `/api/v1/accounts/me/`
  - JWT refresh support verification
  - safer serializers for public account reads

## Step 3: Institutes

- Add serializers, views, and routes for:
  - institute list/detail
  - memberships
  - classes/darjahs
  - institute subjects
  - private library access basics
- Apply role-aware scoping:
  - public authenticated reads where safe
  - institute admin write controls
  - institute member visibility rules

## Step 4: Scholars

- Add runtime for:
  - scholar profile read/update
  - verification application submission
  - scholar review list/create
  - support/object/revise basics
- Keep scholar verification and moderation states visible and explicit.

## Step 5: Library

- Add runtime for:
  - book list/detail/create
  - book file list
  - chunk/reference list
  - search and filters
  - visibility scoping for public/private/institute content
- Make the metadata form mandatory in create flow.

## Step 6: Ingestion

- Add upload-session serializers, service layer, routes, and Celery tasks.
- Implement lifecycle:
  - uploaded
  - metadata_pending
  - queued
  - processing
  - review_pending
  - published
  - failed
- Implement safe extraction policy:
  - extract text when feasible
  - mark scanned PDFs as `OCR_PENDING`
  - never fabricate OCR output

## Step 7: Knowledge and skills

- Add book-linked knowledge object runtime.
- Add topic-map listing.
- Add skill pack list/detail with draft vs active review state.

## Step 8: Grounded Q&A

- Add service-layer flow:
  - classify question
  - retrieve visible chunks from DB
  - select skill pack if relevant
  - build structured response
  - log query/answer/source provenance
- Return safe insufficient-support responses when evidence is weak.

## Step 9: AI providers

- Move runtime logic out of `models.py` into service/adapters files.
- Implement adapters for:
  - Gemini
  - OpenRouter
  - Ollama
- Implement selection hierarchy:
  - user
  - institute
  - system
  - env fallback for system defaults
- Add health-check endpoint.

## Step 10: Frontend

- Add auth provider and route guards.
- Replace static dashboard content with live data.
- Add product routes for:
  - library list/detail
  - upload wizard
  - grounded Q&A
  - scholar profile/reviews
  - institute overview
- Keep the existing visual language and avoid major UI churn.

## Step 11: Deployment and docs

- Update backend production settings and env examples.
- Add/update:
  - gunicorn config
  - systemd units
  - nginx site template
  - exact VPS deployment steps for `/home/fg/library-platform`

## Step 12: Tests

- Add focused tests for:
  - auth registration/login/me
  - institute-scoped access
  - book visibility
  - ingestion job creation
  - safe Q&A insufficient-support behavior
  - provider selection hierarchy
