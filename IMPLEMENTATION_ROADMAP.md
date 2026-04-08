# Step-by-Step Implementation Roadmap

## Phase 1: Foundation & Core Auth (Weeks 1-3)

### Milestone 1.1: Project Setup & Infrastructure
- [ ] Django project structure and venv setup
- [ ] PostgreSQL database creation and initial migration
- [ ] Redis setup for caching/queues
- [ ] Environment configuration (.env files)
- [ ] Docker setup for dev/test environments
- [ ] Git repository initialization
- [ ] CI/CD pipeline setup (GitHub Actions or similar)

### Milestone 1.2: Authentication & User Management
- [ ] Implement custom User model with roles
- [ ] User registration endpoint
- [ ] Email verification flow
- [ ] Login with JWT tokens
- [ ] Token refresh mechanism
- [ ] Password reset flow
- [ ] User profile management endpoint
- [ ] Role assignment system

### Milestone 1.3: Role-Based Access Control
- [ ] Implement permission classes (IsAdmin, IsScholar, etc.)
- [ ] Middleware for permission checks
- [ ] Audit logging for auth events
- [ ] Rate limiting on login/register endpoints

### Milestone 1.4: Frontend Auth Pages
- [ ] Next.js setup with App Router
- [ ] Login page component
- [ ] Registration page component
- [ ] Password reset page
- [ ] Protected route middleware
- [ ] Token storage and refresh logic
- [ ] Auth context/provider

---

## Phase 2: Institute & Organization (Weeks 4-6)

### Milestone 2.1: Institute Management
- [ ] Institute model (name, admin, branding)
- [ ] Institute membership system
- [ ] Institute policies (JSON storage)
- [ ] Class/Darjah model and grouping
- [ ] Subject assignment to classes
- [ ] Student enrollment in classes
- [ ] Institute dashboard backend APIs

### Milestone 2.2: Institute Frontend
- [ ] Institute admin panel
- [ ] Class management interface
- [ ] Student roster view
- [ ] Subject assignment UI
- [ ] Institute settings panel

### Milestone 2.3: Role-Based Dashboards
- [ ] Admin dashboard (platform overview)
- [ ] Institute admin dashboard (institute stats)
- [ ] Teacher dashboard (class & progress)
- [ ] Student dashboard (learning path)
- [ ] Scholar dashboard (review queue)

---

## Phase 3: Library & Book Management (Weeks 7-10)

### Milestone 3.1: Book Models & Metadata
- [ ] Book model (title, author, subject, level)
- [ ] BookFile model (handling multiple formats)
- [ ] BookMetadata model (user/AI/reviewed states)
- [ ] Edition and volume support
- [ ] Public/private book states
- [ ] Book approval workflow states

### Milestone 3.2: Guided Upload Pipeline
- [ ] Book upload endpoint with file handling
- [ ] Metadata form (identity, classification, structure hints)
- [ ] Book validation and preview
- [ ] AI pre-analysis trigger (async task)
- [ ] Upload status tracking
- [ ] User/admin confirmation flow

### Milestone 3.3: File & OCR Processing
- [ ] PDF parsing and page extraction
- [ ] OCR task via Celery (PyPDF2, pdf2image)
- [ ] Page mapping (book page → file page)
- [ ] Arabic text normalization
- [ ] Quality detection and warnings

### Milestone 3.4: Library Frontend
- [ ] Book browse/search page
- [ ] Advanced filters (subject, level, institute)
- [ ] Book detail view
- [ ] Upload wizard (multi-step form)
- [ ] Upload status tracking UI

---

## Phase 4: Knowledge Extraction & QA Engine (Weeks 11-15)

### Milestone 4.1: Knowledge Models
- [ ] BookChunk model (paragraph, definition, etc.)
- [ ] KnowledgeObject model (concept, rule)
- [ ] Topic/relation graph models
- [ ] Reference and citation models
- [ ] Embeddings storage (pgvector)

### Milestone 4.2: Extraction Pipeline
- [ ] Chunking strategy (section-aware, overlap)
- [ ] Heading detection and use
- [ ] Entity extraction (names, terms, concepts)
- [ ] Embedding generation via AI provider
- [ ] Topic graph creation
- [ ] Relation extraction

### Milestone 4.3: QA Engine Core
- [ ] Query classification endpoint
- [ ] Subject/intent detection
- [ ] Retrieval with vector search (pgvector)
- [ ] Ranking and reranking logic
- [ ] Citation compilation from retrieved chunks
- [ ] Direct answer generation (grounded)
- [ ] Confidence scoring

### Milestone 4.4: Answer Verification & Badges
- [ ] Schema for answer sources and citations
- [ ] Verification status (SourceGrounded, ScholarVerified, etc.)
- [ ] Badge generation logic
- [ ] Disputed answer handling
- [ ] Answer history and revisions

### Milestone 4.5: QA Frontend
- [ ] Query input interface
- [ ] Answer display with citations
- [ ] Source expansion UI
- [ ] Verification badge display
- [ ] Answer voting/feedback

---

## Phase 5: Skill Packs & Subject Rules (Weeks 16-18)

### Milestone 5.1: Skill Pack Models
- [ ] SkillPack model (name, subject, rules)
- [ ] Rule templates (citation, summary, conflict handling)
- [ ] Definition of answer_template, retrieval_rules, etc.
- [ ] Language style policies
- [ ] Verification requirements per skill

### Milestone 5.2: Skill Pack Generation
- [ ] Auto-draft generation from uploaded books
- [ ] Rule inference from book structure
- [ ] Preview and review interface
- [ ] Admin approval workflow

### Milestone 5.3: Answer Engine Integration
- [ ] Query-to-skill-pack matching
- [ ] Apply skill pack rules in answer compilation
- [ ] No-repeat-matan enforcement
- [ ] Summary policy application
- [ ] Conflict detection and resolution

---

## Phase 6: Scholar System & Reviews (Weeks 19-22)

### Milestone 6.1: Scholar Profiles & Verification
- [ ] Scholar model (name, specialization, credentials)
- [ ] Document upload for verification
- [ ] Admin review workflow
- [ ] Verification status and badge logic
- [ ] Trust score calculation

### Milestone 6.2: Scholar Reviews & Objections
- [ ] ScholarReview model
- [ ] Review submission on answers
- [ ] Objection and support logic
- [ ] ConsensusScore computation
- [ ] Verified explanation banks

### Milestone 6.3: Scholar Frontend
- [ ] Scholar profile page
- [ ] Verification document upload
- [ ] Review queue interface
- [ ] Submit review/objection UI
- [ ] Scholar public profile

---

## Phase 7: Learning & Practice System (Weeks 23-25)

### Milestone 7.1: Exercise & Practice Models
- [ ] Exercise model (MCQ, short answer, fill-in, etc.)
- [ ] Difficulty levels and skill mapping
- [ ] Auto-generation from book content
- [ ] Answer keys and explanations

### Milestone 7.2: Learning Tracking
- [ ] Progress model (score, attempts, time spent)
- [ ] Weak topic detection
- [ ] Personalized recommendations
- [ ] Revision lists and bookmarks
- [ ] Teacher assignment tracking

### Milestone 7.3: Learning Frontend
- [ ] Practice interface
- [ ] Exercise display and submission
- [ ] Progress dashboard
- [ ] Weak topic summary
- [ ] Revision scheduler

---

## Phase 8: Admin & Moderation (Weeks 26-27)

### Milestone 8.1: Admin Panels
- [ ] Content moderation queue
- [ ] Flag/report handling
- [ ] Book approval management
- [ ] User management (ban, role changes)
- [ ] Analytics dashboard

### Milestone 8.2: Provider & Configuration
- [ ] AI provider management UI
- [ ] API key configuration
- [ ] Model selection and priority
- [ ] Rate limit settings
- [ ] System settings panel

---

## Phase 9: Deployment & Production (Weeks 28-29)

### Milestone 9.1: Backend Deployment
- [ ] Gunicorn/Uvicorn setup
- [ ] Systemd service units
- [ ] Database migrations and backup setup
- [ ] Celery worker and beat setup
- [ ] Redis persistence
- [ ] Logging and monitoring

### Milestone 9.2: Frontend Deployment
- [ ] Next.js build optimization
- [ ] Systemd service for Next.js
- [ ] Static asset caching
- [ ] Production environment variables

### Milestone 9.3: Nginx Reverse Proxy
- [ ] Nginx server block for library.digigalaxy.cloud
- [ ] SSL/TLS termination with certbot
- [ ] API route proxying
- [ ] Static file serving
- [ ] Rate limiting configuration

### Milestone 9.4: Monitoring & Maintenance
- [ ] Application performance monitoring (APM)
- [ ] Error tracking (Sentry)
- [ ] Database backups (automated)
- [ ] Log aggregation
- [ ] Health checks and alerts

---

## Phase 10: Testing & Quality Assurance (Ongoing)

### Milestone 10.1: Backend Testing
- [ ] Unit tests for models and serializers (>80% coverage)
- [ ] Integration tests for API endpoints
- [ ] Permission and auth tests
- [ ] Celery task tests

### Milestone 10.2: Frontend Testing
- [ ] Component unit tests
- [ ] E2E tests for user flows (Cypress/Playwright)
- [ ] Mobile responsive testing
- [ ] Accessibility testing (WCAG)

### Milestone 10.3: Security Testing
- [ ] OWASP Top 10 scan
- [ ] SQL injection tests
- [ ] CSRF/XSS testing
- [ ] API rate limit testing
- [ ] Password strength validation

---

## Phase 11: Documentation & Launch (Week 30+)

### Milestone 11.1: Documentation
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Architecture documentation
- [ ] Deployment guide
- [ ] User guides (admin, teacher, student, scholar)
- [ ] Developer onboarding guide

### Milestone 11.2: Soft Launch
- [ ] Beta testing with limited users
- [ ] Feedback collection
- [ ] Bug fixes and adjustments
- [ ] Performance tuning

### Milestone 11.3: Public Launch
- [ ] Content seeding (initial books)
- [ ] Scholar onboarding
- [ ] Marketing and outreach
- [ ] Community guidelines enforcement
- [ ] Continuous improvement cycle

---

## Estimated Timeline
- **Total Duration:** 30 weeks (~7 months)
- **Parallel Work:** Frontend and backend can be developed in parallel after Week 3
- **Testing:** Integrated throughout, not just Phase 10
- **Deployment:** Can begin Phase 9 by Week 20 (staging environment)

## Key Assumptions
- Team has Django/DRF and Next.js experience
- PostgreSQL and Redis available on VPS
- Existing Frappe bench configured and stable
- AI provider credentials (Gemini, OpenRouter) available
- Domain SSL certificate via certbot

## Risk Mitigation
- Weekly sprint reviews and velocity tracking
- Daily standup for blockers
- Backup plans for AI provider failures (fallback to Ollama)
- Database backup before each major deployment
- Feature flags for gradual rollout