# Architecture Audit - 2026-04-08

This document is a no-edit implementation audit for the current `library-platform` repository and its active deployment target at `library.digigalaxy.cloud`.

It is intentionally diagnostic only. No production runtime assumptions in this document should be treated as complete or production-safe until the listed blockers are addressed.

## 1. Executive Summary

The domain `library.digigalaxy.cloud` is already pointed to this VPS and currently serves a Next.js application that redirects to `/login`. HTTP redirects to HTTPS successfully.

The repository contains a meaningful scaffold for the intended product:

- Django backend with modular apps
- Next.js frontend with App Router
- Docker Compose
- Nginx config
- Systemd unit files
- Basic auth and model scaffolding

However, the platform is still at an early scaffold stage rather than a production-grade scholarly SaaS system. The current implementation does not yet satisfy the required product rules around:

- source-grounded answer control
- scholar verification priority
- guided ingestion workflow depth
- trust-state modeling
- sensitive-topic safety
- institute-grade multi-tenancy
- production security hardening
- production runtime completeness

The immediate conclusion is:

- the domain and reverse proxy path are present
- the repository is a viable starting point
- the live architecture is incomplete
- production credentials and runtime topology need hardening before feature expansion

## 2. Verified Current State

Verified on April 8, 2026:

- `library.digigalaxy.cloud` resolves to `72.60.118.195`
- `http://library.digigalaxy.cloud` returns `301 Moved Permanently` to HTTPS
- `https://library.digigalaxy.cloud` returns `307 Temporary Redirect` to `/login`
- Docker currently has only `db` and `redis` running for this project
- `backend` and `frontend` are not currently running via Docker Compose

Current live/project indicators:

- [docker-compose.yml](/home/fg/library-platform/docker-compose.yml)
- [infra/nginx/library-platform.conf](/home/fg/library-platform/infra/nginx/library-platform.conf)
- [infra/systemd/library-django.service](/home/fg/library-platform/infra/systemd/library-django.service)
- [infra/systemd/library-frontend.service](/home/fg/library-platform/infra/systemd/library-frontend.service)
- [.env](/home/fg/library-platform/.env)

## 3. Current Strengths

The current codebase already has several positive foundations:

- clear backend/frontend separation
- correct broad stack choice: Django, DRF, Next.js, PostgreSQL, Redis
- modular app layout that aligns with the target product
- custom user model already enabled
- initial institute/scholar/library/skills/QA domain placeholders exist
- Nginx separation from Frappe appears conceptually respected
- Next.js root layout is already Arabic-first with `lang="ar"` and `dir="rtl"`
- AI provider abstraction has been started instead of hard-coding one vendor everywhere

These choices reduce rewrite risk and make iterative hardening practical.

## 4. Critical Production Blockers

These are the issues that should be treated as immediate blockers before calling the platform production-ready.

### 4.1 Secrets and Credentials

Current config still contains placeholder or weak values:

- DB password is `library_password`
- secret key is placeholder
- JWT secret is placeholder
- encryption key is placeholder

Affected files:

- [.env](/home/fg/library-platform/.env)
- [docker-compose.yml](/home/fg/library-platform/docker-compose.yml)

Impact:

- unsafe for production
- enables accidental credential reuse
- makes provider-key encryption non-trustworthy

### 4.2 Database Exposure

Current Compose publishes PostgreSQL directly:

- `0.0.0.0:5432->5432`

Affected file:

- [docker-compose.yml](/home/fg/library-platform/docker-compose.yml)

Impact:

- unnecessary public attack surface
- potential conflict with other DB usage on the VPS
- not aligned with least-privilege production posture

### 4.3 Development Runtime in Compose

Current backend Compose command uses:

- `python manage.py runserver 0.0.0.0:8001`

Affected file:

- [docker-compose.yml](/home/fg/library-platform/docker-compose.yml)

Impact:

- not acceptable as a production app server
- poor performance and resilience
- not aligned with systemd files that expect Gunicorn

### 4.4 Incomplete Process Topology

Current Docker Compose does not run:

- Celery worker
- Celery beat
- dedicated production frontend build flow
- static/media serving strategy

Affected files:

- [docker-compose.yml](/home/fg/library-platform/docker-compose.yml)
- [infra/systemd/library-django.service](/home/fg/library-platform/infra/systemd/library-django.service)
- [infra/systemd/library-frontend.service](/home/fg/library-platform/infra/systemd/library-frontend.service)

Impact:

- ingestion and async pipeline cannot mature cleanly
- runtime strategy is split between partial Compose and partial systemd
- operational ownership is unclear

### 4.5 Security Settings Need Expansion

Current production settings are minimal:

- `SECURE_SSL_REDIRECT = True`
- secure cookies enabled
- little additional hardening present

Affected file:

- [backend/config/settings/production.py](/home/fg/library-platform/backend/config/settings/production.py)

Missing:

- HSTS policy
- proxy SSL header trust
- secure CSRF trusted origins
- static/media strategy
- stricter CORS/host management
- logging separation by subsystem
- security middleware tuning

## 5. Backend Architecture Gap Analysis

### 5.1 Common Foundation

Current state:

- [backend/apps/common/models.py](/home/fg/library-platform/backend/apps/common/models.py) only provides timestamps

Gap:

- no UUID/public IDs
- no soft deletion strategy
- no audit actor tracking
- no moderation metadata
- no publish/review status base mixins

### 5.2 Accounts and Roles

Current state:

- [backend/apps/accounts/models.py](/home/fg/library-platform/backend/apps/accounts/models.py) has custom user, phone, language pair, roles, institute, and class/darjah links

Strength:

- correct direction for custom auth

Gaps:

- no role assignment constraints or tenant-aware permission model
- no user profile completeness or onboarding state
- no provider ownership preferences
- no scholar/teacher/student capability mapping beyond plain role names
- no audit trail for auth-sensitive actions

### 5.3 Institutes

Current state:

- [backend/apps/institutes/models.py](/home/fg/library-platform/backend/apps/institutes/models.py) contains only `Institute`, `ClassDarjah`, and `Subject`

Gaps:

- no institute memberships table
- no multi-role institute membership support
- no branding model
- no policy versioning
- no private library access control objects
- no class subject assignments
- no teacher-student cohort relationships

### 5.4 Scholars

Current state:

- [backend/apps/scholars/models.py](/home/fg/library-platform/backend/apps/scholars/models.py) only tracks one specialization string and verification status

Gaps:

- missing scholar identity profile fields
- missing document/certificate storage
- missing trust score
- missing badge state
- missing review count and correction count
- missing recommendation and verification workflow objects
- missing support/objection/revision entities

### 5.5 Library

Current state:

- [backend/apps/library/models.py](/home/fg/library-platform/backend/apps/library/models.py) only has `Book(title, arabic_title, author, public)`

Gaps:

- no `BookFile`
- no `BookMetadata`
- no metadata state separation
- no edition/version modeling
- no page count / volume / publisher / language / madhhab / level
- no structure map or chunk model
- no topic map
- no approval review model
- no file storage state
- no public/private/institute visibility policy depth

This is one of the largest model gaps in the whole platform.

### 5.6 Ingestion

Current state:

- [backend/apps/ingestion/models.py](/home/fg/library-platform/backend/apps/ingestion/models.py) only defines a minimal `UploadTask`

Gaps:

- no upload session model
- no ingestion stage state machine
- no OCR detection metadata
- no page extraction tracking
- no normalization/chunking/indexing statuses
- no review checkpoints
- no retry/failure diagnostics
- no operator notes or approvals

### 5.7 Knowledge

The app exists structurally, but the domain has not yet been expanded into the required knowledge system:

- concepts
- rules
- definitions
- evidences
- examples
- relations graph
- structured JSON knowledge objects

This app will become central to grounded retrieval and skill-pack generation.

### 5.8 Skills

Current state:

- [backend/apps/skills/models.py](/home/fg/library-platform/backend/apps/skills/models.py) stores `name`, `subject`, `rules`, `active`

Gaps:

- no review status
- no source book linkage
- no answer template
- no retrieval rules
- no citation policy
- no no-repeat-matan policy
- no summary policy
- no comparison/conflict policy
- no scholar priority policy
- no exercise generation policy
- no verification requirement policy
- no language-style configuration
- no versioning or draft/publish workflow

### 5.9 QA Engine

Current state:

- [backend/apps/qa_engine/models.py](/home/fg/library-platform/backend/apps/qa_engine/models.py) only stores `question` and a generic JSON `response`

Gaps:

- no query classification
- no sensitivity model
- no scope model
- no provider execution records
- no retrieval record set
- no provenance graph
- no confidence scoring
- no scholar-reviewed answer separation
- no verification badges
- no quoted passage entity
- no answer revision history

This is the most important functional gap relative to the product rules.

### 5.10 Learning

Current state:

- [backend/apps/learning/models.py](/home/fg/library-platform/backend/apps/learning/models.py) only defines a minimal `Exercise`

Gaps:

- no exercise templates
- no attempts
- no weak-topic tracking
- no saved questions
- no bookmarks
- no revision lists
- no notes
- no assignments
- no student progress modeling

### 5.11 AI Providers

Current state:

- [backend/apps/ai_providers/models.py](/home/fg/library-platform/backend/apps/ai_providers/models.py) is more mature than most other apps

Strengths:

- system/institute/user scoping exists
- encryption concept exists
- adapter pattern exists

Gaps:

- adapter classes currently live inside model file and are stubs
- business logic is mixed with persistence models
- no usage metering model
- no health-check cache/state
- no routing policy abstraction
- no credential rotation support
- no model capability metadata
- no provider governance for sensitive query classes

## 6. API Surface Gap Analysis

Current route organization is reasonable:

- [backend/config/urls.py](/home/fg/library-platform/backend/config/urls.py)

But current exposure is still thin:

- auth endpoints exist
- app URLs are included
- backend root returns a simple status string

Gaps:

- no API versioning strategy beyond folder inclusion
- no OpenAPI schema or docs integration
- no domain-specific serializers documented
- no filter/search/pagination patterns for library browsing
- no upload wizard endpoints
- no answer execution endpoints with review-safe response contracts
- no moderation endpoints
- no provider test/health endpoints
- no student dashboard aggregate endpoints

## 7. Frontend Gap Analysis

### 7.1 Current UI State

Current UI is still extremely early-stage:

- [frontend/app/page.tsx](/home/fg/library-platform/frontend/app/page.tsx) redirects to `/login`
- [frontend/app/dashboard/page.tsx](/home/fg/library-platform/frontend/app/dashboard/page.tsx) is a basic placeholder
- [frontend/app/layout.tsx](/home/fg/library-platform/frontend/app/layout.tsx) sets Arabic HTML direction correctly
- [frontend/package.json](/home/fg/library-platform/frontend/package.json) includes Flowbite and Tailwind

### 7.2 Missing Product UX

Major missing frontend areas:

- public homepage and library browsing
- Arabic-first product shell
- RTL/LTR language-pair switching behavior
- answer cards with verification badges
- source cards with snippet + page behavior
- upload wizard
- scholar review dashboard
- institute dashboard
- class/darjah views
- practice zone
- mobile navigation system
- dark mode strategy
- brand-level design system beyond package installation

## 8. Deployment Topology Assessment

### 8.1 Nginx

Current Nginx file:

- [infra/nginx/library-platform.conf](/home/fg/library-platform/infra/nginx/library-platform.conf)

Strengths:

- basic domain separation exists
- frontend and backend are routed separately

Gaps:

- server block still includes raw IP and domain together
- no explicit SSL server block shown in repo for the current active HTTPS behavior
- no upload-size settings
- no static/media serving rules
- no cache tuning for assets
- no long-term websocket forward strategy

### 8.2 Systemd

Current service files:

- [infra/systemd/library-django.service](/home/fg/library-platform/infra/systemd/library-django.service)
- [infra/systemd/library-frontend.service](/home/fg/library-platform/infra/systemd/library-frontend.service)

Gaps:

- paths reference `/home/library-user/...` rather than the current repository path under `/home/fg/...`
- no environment file handling shown
- no restart policy shown
- no Celery beat unit in the reviewed set
- frontend service uses `/usr/bin/npm start` without explicit build lifecycle or working production artifact assumptions

### 8.3 Compose Strategy

Current Compose is closer to local development than production:

- no healthchecks
- no worker/beat services
- no internal-only networking for DB
- no named media/static volumes
- no secrets management
- obsolete `version` key warning appears

## 9. Product Rule Compliance Assessment

Measured against your non-negotiable rules, the current codebase is only partially compliant.

### Rule: AI must not behave like a free-imagination chatbot

Status:

- not yet enforced

Reason:

- no robust answer contract
- no retrieval/provenance enforcement objects

### Rule: Scholar-reviewed answers must be separated from raw engine output

Status:

- not yet compliant

Reason:

- current QA model stores generic JSON only

### Rule: Sensitive topics require guarded behavior

Status:

- not yet compliant

Reason:

- no sensitivity classification or stricter policy routing

### Rule: Mandatory guided upload workflow

Status:

- not yet compliant

Reason:

- ingestion pipeline not modeled deeply enough

### Rule: Skill packs must be first-class and reviewed before publish

Status:

- partially scaffolded, not compliant

Reason:

- model too small, no review lifecycle

### Rule: Standalone app, not Frappe UI

Status:

- compliant in direction

Reason:

- separate Next.js frontend and Django backend are used

### Rule: Same VPS, existing Bench untouched

Status:

- compliant in intent, not yet fully operationalized

Reason:

- separate ports are used conceptually, but production isolation needs full finalization

## 10. Recommended Enhancement Priority

Enhancements should be applied in this order.

### Priority 0 - Secure the platform foundation

- rotate all placeholder secrets
- stop exposing Postgres publicly
- normalize runtime strategy
- add Gunicorn/Celery production services
- add healthchecks and restart policies
- define media/static handling

### Priority 1 - Build the domain backbone

- expand library, ingestion, QA, scholars, institutes, and learning models
- add audit and moderation primitives
- define status enums and review lifecycle models

### Priority 2 - Build the trust pipeline

- implement retrieval/provenance entities
- implement structured answer object
- add verification badges and scholar review flow
- enforce source-grounded and sensitivity-aware policies

### Priority 3 - Build the product experience

- public library
- answer viewer
- upload wizard
- scholar review dashboard
- student dashboard
- institute shell

### Priority 4 - Build scalable operations

- metrics
- backups
- CI/CD
- smoke checks
- provider health monitoring
- structured logging and alerting

## 11. Recommended First Implementation Slice

The best first implementation slice is:

1. production hardening
2. library domain expansion
3. ingestion workflow expansion
4. QA answer object and provenance model
5. public library + upload wizard + grounded answer shell

This sequence gives the highest leverage because it creates the minimum trustworthy vertical slice of the actual product.

## 12. Files Most In Need Of Immediate Follow-Up

Highest-priority existing files:

- [docker-compose.yml](/home/fg/library-platform/docker-compose.yml)
- [.env](/home/fg/library-platform/.env)
- [backend/config/settings/base.py](/home/fg/library-platform/backend/config/settings/base.py)
- [backend/config/settings/production.py](/home/fg/library-platform/backend/config/settings/production.py)
- [infra/nginx/library-platform.conf](/home/fg/library-platform/infra/nginx/library-platform.conf)
- [infra/systemd/library-django.service](/home/fg/library-platform/infra/systemd/library-django.service)
- [infra/systemd/library-frontend.service](/home/fg/library-platform/infra/systemd/library-frontend.service)
- [backend/apps/library/models.py](/home/fg/library-platform/backend/apps/library/models.py)
- [backend/apps/ingestion/models.py](/home/fg/library-platform/backend/apps/ingestion/models.py)
- [backend/apps/qa_engine/models.py](/home/fg/library-platform/backend/apps/qa_engine/models.py)
- [backend/apps/scholars/models.py](/home/fg/library-platform/backend/apps/scholars/models.py)
- [backend/apps/skills/models.py](/home/fg/library-platform/backend/apps/skills/models.py)
- [backend/apps/learning/models.py](/home/fg/library-platform/backend/apps/learning/models.py)
- [frontend/app/page.tsx](/home/fg/library-platform/frontend/app/page.tsx)
- [frontend/app/dashboard/page.tsx](/home/fg/library-platform/frontend/app/dashboard/page.tsx)

## 13. Decision Recommendation

Proceed with implementation, but do it in two explicit steps:

1. production hardening and architecture correction
2. first vertical product milestone

Do not continue adding surface features on top of the current scaffold without first fixing the runtime/security/domain-model foundation. The current repository is strong enough to evolve, but still early enough that disciplined structure now will prevent expensive rework later.
