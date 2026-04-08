# Risks and Mitigation Strategy

## 1. Technical Risks

### 1.1 VPS Resource Contention with Existing Frappe Bench
**Risk Level:** HIGH

**Issue:**
- Frappe/bench may spike in CPU, memory, or disk I/O
- Library platform may starve when Frappe is under load
- Both platforms share PostgreSQL and Redis connections
- Port conflicts or service interference

**Mitigation:**
- [ ] Use separate PostgreSQL database (`library_db`) with separate credentials
- [ ] Use separate Redis instance or distinct DB/index (e.g., Frappe on DB 0, Library on DB 1)
- [ ] Deploy on separate ports (Django 8001, Next.js 3000, separate from bench/socketio)
- [ ] Use dedicated system user (`library-user`) with separate venv
- [ ] Monitor resource usage (CPU, Memory, Disk I/O) via `htop`, `iotop`, Grafana
- [ ] Set up resource quotas/cgroups if kernel supports (prevent runaway processes)
- [ ] Test under load simulated Frappe traffic before production launch
- [ ] Implement health checks and auto-restart failed services
- [ ] Document escalation: If resources constrained, plan VPS upgrade or separate server

### 1.2 AI Provider Unavailability or API Failures
**Risk Level:** HIGH

**Issue:**
- Gemini/OpenRouter may have outages or rate limits
- API keys may be compromised or revoked
- Network latency or timeouts
- Cost overruns if high-volume queries hit free tier limits

**Mitigation:**
- [ ] Implement provider fallback chain (primary → secondary → Ollama local)
- [ ] Cache common queries and responses to reduce API calls
- [ ] Implement circuit breaker pattern to fail gracefully
- [ ] Warn users if all providers unavailable
- [ ] Set rate limits per user/institute to prevent abuse
- [ ] Monitor API costs and set spending alerts
- [ ] Use Ollama as free local fallback for critical operations
- [ ] Store encrypted API keys separately; rotate quarterly
- [ ] Document provider SLA requirements and have backup plan

### 1.3 Database Corruption or Data Loss
**Risk Level:** CRITICAL

**Issue:**
- PostgreSQL database crash during ingestion or high load
- Unplanned VPS shutdown (power loss, hardware failure)
- Backup failures
- Accidental data deletion

**Mitigation:**
- [ ] Enable PostgreSQL WAL archiving for point-in-time recovery
- [ ] Set up automated daily backups (full + incremental)
- [ ] Store backup copies off-server (S3, separate storage)
- [ ] Test restore procedure monthly
- [ ] Use PostgreSQL replication (streaming replication) for hot standby
- [ ] Enable transaction logging and audit trails
- [ ] Implement soft-delete (is_deleted flag) instead of hard deletes
- [ ] Version control for schema changes (alembic migrations)
- [ ] Monitor database replication lag

### 1.4 OCR and Text Processing Failures
**Risk Level:** MEDIUM

**Issue:**
- OCR may fail on low-quality PDFs or non-standard fonts
- Arabic text normalization may corrupt diacritics
- Chunking strategy may break semantically important phrases
- Embedding generation may fail for long texts

**Mitigation:**
- [ ] Implement OCR quality detection; flag poor-quality scans for manual review
- [ ] Preserve diacritics in storage; optional removal for processing
- [ ] Use overlap-aware chunking to preserve context
- [ ] Test chunking on diverse book types (matan, sharh, hashiya)
- [ ] Fallback: Allow manual text input if OCR fails
- [ ] Validate embeddings; retry failed chunks
- [ ] Log all OCR/processing errors for admin review
- [ ] Implement batch re-processing for failed chunks

### 1.5 Vector Search Performance Degradation
**Risk Level:** MEDIUM

**Issue:**
- pgvector queries may slow down with millions of embeddings
- Large result sets may cause memory/timeout issues
- Index fragmentation over time

**Mitigation:**
- [ ] Plan scaling: Test pgvector performance with 1M, 10M embeddings
- [ ] Use HNSW indexes for faster approximate search (vs IVFFlat)
- [ ] Implement result pagination (top-k + cursor-based)
- [ ] Cache frequently accessed embeddings
- [ ] Monitor query execution time; alert if >2 sec
- [ ] Reindex monthly during low-traffic windows
- [ ] Consider migration to dedicated vector DB (Weaviate, Milvus) if scaling needed

### 1.6 Celery Task Failures or Queue Backlog
**Risk Level:** MEDIUM

**Issue:**
- Long-running ingestion tasks may timeout
- Redis connection loss may drop queued tasks
- Queue backlog during peak upload times

**Mitigation:**
- [ ] Set task TTL (time-to-live) and retry policies
- [ ] Use task result backend with persistence (db or Redis AOF)
- [ ] Monitor queue depth; alert if backlog > 100 tasks
- [ ] Implement graceful task shutdown (SIGTERM handlers)
- [ ] Scale Celery workers horizontally during peak hours
- [ ] Implement task prioritization (high-priority uploads vs analytics)
- [ ] Separate queues for different task types (ingestion, emails, analytics)

---

## 2. Security Risks

### 2.1 Sensitive Topic Mishandling
**Risk Level:** CRITICAL (Reputational + Legal)

**Issue:**
- AI may generate inappropriate/heretical answers on Islamic topics
- Answers may be taken as fatwas and cause harm
- Lack of proper source grounding on sensitive topics
- User trust eroded by wrong answers

**Mitigation:**
- [ ] Enforce source-grounding - no answers without book reference
- [ ] Flagging threshold: Any sensitive topic automatically marked "needs review"
- [ ] Verification badge mandatory before publication on sensitive topics
- [ ] Admin approval workflow for sensitive subject queries
- [ ] Scholar review queue prioritizes sensitive flags
- [ ] Clear disclaimer in UI: "AI provides summaries; consult qualified scholars"
- [ ] Skill pack sensitivity_policy blocks loose summarization
- [ ] Rate limiting on sensitive topics to prevent abuse
- [ ] Dedicated audit log for sensitive queries and reviews

### 2.2 Unauthorized Data Access
**Risk Level:** HIGH

**Issue:**
- Students accessing private institute content
- Institute admins accessing another institute's data
- Scholars accessing unpublished books
- Permission system bugs allow privilege escalation

**Mitigation:**
- [ ] Implement role-based permission checks on every API endpoint
- [ ] Scope data by institute/class at database level (row-level security)
- [ ] Use Django Query objects to filter by user context
- [ ] Implement object-level permissions for sensitive data
- [ ] Audit log every access to sensitive resources
- [ ] Monthly permission audits: Check for stale/incorrect grants
- [ ] Automated tests for permission boundaries
- [ ] Use Django's `@permission_required` decorators consistently

### 2.3 Authentication Bypass or Session Hijacking
**Risk Level:** HIGH

**Issue:**
- JWT tokens stolen from localStorage (XSS vulnerability)
- Weak password policies allow brute force
- Session timeout not enforced
- Token refresh logic vulnerability

**Mitigation:**
- [ ] Use HttpOnly + Secure cookies for tokens (vs localStorage)
- [ ] Enforce 12+ character passwords, complexity rules
- [ ] Implement rate limiting: 5 failed logins → 15-min lockout
- [ ] Set short JWT expiry (15 min) with refresh token rotation
- [ ] Revoke tokens on logout
- [ ] Implement CSRF protection on state-changing endpoints
- [ ] Add device fingerprinting for anomalous login detection
- [ ] Optional: Require 2FA for admins and scholars
- [ ] Monitor for concurrent sessions; flag suspicious patterns

### 2.4 SQL Injection or ORM Misuse
**Risk Level:** HIGH

**Issue:**
- Raw SQL queries without parameterization
- Unsafe string concatenation in filters
- Serializer validation bypassed

**Mitigation:**
- [ ] Never use raw SQL; always use ORM (Django QuerySet)
- [ ] Use parameterized queries for any raw SQL needed
- [ ] Implement automatic SQL injection scanner in CI/CD (sqlmap)
- [ ] Code review checklist: Check for RAW_SQL usage
- [ ] Input validation: Whitelist expected field types/values
- [ ] DRF serializer validation mandatory on all inputs
- [ ] Test with fuzzing tools (AFL, libFuzzer)

### 2.5 API Key Exposure
**Risk Level:** HIGH

**Issue:**
- API keys hardcoded in code
- Keys logged in error messages or debug output
- Keys in version control history
- Keys exposed in frontend env vars

**Mitigation:**
- [ ] Store all keys in `.env` file (git-ignored)
- [ ] Use environment variables injected at runtime
- [ ] Encrypt keys in database (Fernet cipher)
- [ ] Never log sensitive values; use masking
- [ ] Automated scanning of git history (detect-secrets)
- [ ] Rotate API keys quarterly
- [ ] Use IAM roles instead of API keys where possible
- [ ] Implement API key scoping (read-only, time-limited)

### 2.6 Denial of Service (DoS / Brute Force)
**Risk Level:** MEDIUM-HIGH

**Issue:**
- Attackers flood upload endpoint
- Brute force password guessing
- Expensive queries (e.g., retrieval with no limits)
- Elastic costs from scaling

**Mitigation:**
- [ ] Implement rate limiting globally (requests/IP/user)
- [ ] Throttle file uploads: Max 100MB per user per day
- [ ] Query pagination: Max 100 results per request
- [ ] CAPTCHA on registration and repeated failed logins
- [ ] IP blocklist for repeated offenders
- [ ] Cloudflare or similar DDoS protection
- [ ] Monitor bandwidth and query patterns; alert on anomalies
- [ ] Budget alerts on cloud costs

---

## 3. Operational Risks

### 3.1 Deployment Failure or Rollback Issues
**Risk Level:** HIGH

**Issue:**
- Migration errors lock database
- New code breaks existing functionality
- Impossible to rollback to previous version
- Downtime during deployment

**Mitigation:**
- [ ] Zero-downtime deployments: Blue-green or canary releases
- [ ] Database migrations tested on staging before prod
- [ ] Feature flags for gradual rollout (not feature-branch deployments)
- [ ] Automated rollback if health checks fail
- [ ] Keep last 5 production docker images for quick rollback
- [ ] Documentation: Runbook for deployment, rollback, troubleshooting
- [ ] Deployment windows: Off-peak hours (e.g., 2 AM UTC)
- [ ] Post-deployment smoke tests automated

### 3.2 Logging and Monitoring Gaps
**Risk Level:** MEDIUM

**Issue:**
- Errors go unnoticed until users report
- No visibility into slow queries or bottlenecks
- Audit logs not centralized
- Can't debug production issues

**Mitigation:**
- [ ] Centralized logging: ELK (Elasticsearch, Logstash, Kibana) or Loki
- [ ] Application Performance Monitoring (APM): New Relic, DataDog, or Jaeger
- [ ] Error tracking: Sentry for exception aggregation
- [ ] Dashboards: Real-time metrics (queries/sec, error rate, latency)
- [ ] Alerts: Critical errors → PagerDuty/Slack notifications
- [ ] Log retention: 30 days online, 1 year archived
- [ ] Query logging: Slow query log for >1 sec queries
- [ ] Database monitoring: Connection pool, transaction locks

### 3.3 Backup Restoration Failure
**Risk Level:** HIGH

**Issue:**
- Backup corrupted or incomplete
- Restore process untested
- Data inconsistency after restore
- Missing transaction logs

**Mitigation:**
- [ ] Test restore procedure monthly (full dry-run)
- [ ] Store backups in multiple locations (local + remote)
- [ ] Implement incremental backups for faster restores
- [ ] Verify backup checksum before storage
- [ ] Document restore procedure with exact commands
- [ ] Maintain 2-week backup retention for point-in-time recovery
- [ ] Alert if backup fails
- [ ] Maintain separate backup credentials (separate from prod)

### 3.4 Scaling Beyond Initial Capacity
**Risk Level:** MEDIUM

**Issue:**
- Database hits query limits
- File storage fills up
- Network bandwidth saturated
- Redis memory exhausted

**Mitigation:**
- [ ] Capacity planning: Model growth (users, books, queries)
- [ ] Implement caching: Redis for hot data, CDN for static files
- [ ] Database optimization: Indexes, query optimization
- [ ] File storage on separate disk/S3 (not database disk)
- [ ] Monitoring: Alert at 70% capacity utilization
- [ ] Plan: VPS upgrade path identified and budgeted
- [ ] Database replication for read scaling
- [ ] Horizontal scaling: Multiple Django/Celery/Next.js instances load-balanced

---

## 4. Business and Compliance Risks

### 4.1 GDPR / Data Privacy Violations
**Risk Level:** CRITICAL (Legal + Fines)

**Issue:**
- User data not encrypted at rest
- No data deletion mechanism
- Unclear privacy policy or consent flow
- User data shared with third parties (AI providers)
- No audit trail for data processing

**Mitigation:**
- [ ] Encryption at rest (PostgreSQL pgcrypto, full-disk encryption)
- [ ] Encryption in transit (HTTPS/TLS, VPN for internal comms)
- [ ] Implement "right to deletion" (cascade delete or anonymization)
- [ ] Privacy policy published and linked at signup
- [ ] Explicit consent checkboxes for data processing
- [ ] Data Processing Agreement (DPA) with AI providers
- [ ] Audit log for all data access and modifications
- [ ] GDPR compliance checklist reviewed quarterly
- [ ] Data retention policy: Delete inactive accounts after 2 years
- [ ] Regular GDPR impact assessments

### 4.2 Content Copyright or Licensing Issues
**Risk Level:** HIGH (Legal + Takedown)

**Issue:**
- Uploaded books may have copyright violations
- No tracking of licensing rights
- Unclear attribution or source
- Fair use boundaries unclear

**Mitigation:**
- [ ] Upload form: Require copyright/license declaration
- [ ] Copyright check: Compare new uploads against known libraries (CrossRef, Google Books)
- [ ] License field: Store and enforce (CC-BY, CC-BY-SA, Public Domain, etc.)
- [ ] Attribution: Display original author/publisher prominently
- [ ] DMCA takedown procedure: Accept and process requests within 48 hours
- [ ] Legal review: Have lawyer review T&Cs and copyright policy
- [ ] Disable upload for suspicious copyright matches
- [ ] Geographic restriction: Some books only available in certain regions

### 4.3 Mis-representation of AI Capabilities
**Risk Level:** MEDIUM (Reputation)

**Issue:**
- Users believe AI is 100% accurate ("oracle")
- False confidence in sensitive answers
- Lack of transparency about limitations
- Misuse as a fatwa engine

**Mitigation:**
- [ ] Clear disclaimers: "AI summaries, not final advice"
- [ ] Transparency reports: Show confidence scores, verification status
- [ ] Educational content: How the platform works, limitations of AI
- [ ] Warnings on sensitive topics: "Consult qualified scholar"
- [ ] Scholar review badges: Distinguish verified vs unverified
- [ ] No marketing claims of 100% accuracy
- [ ] User feedback loop: Report errors for continuous improvement

### 4.4 Regulatory Changes or Fatwa Laws
**Risk Level:** MEDIUM (Regional)

**Issue:**
- Some countries restrict online Islamic fatwas
- AI regulations may be introduced (EU AI Act)
- Censorship or content restrictions by region
- Liability for user-generated content

**Mitigation:**
- [ ] Legal review in target markets (Saudi, Egypt, Malaysia, UK, EU)
- [ ] Explicitly not providing fatwas; educational summaries only
- [ ] Compliance with local content guidelines
- [ ] Terms of Service: Users liable for misuse, not platform
- [ ] Geographic content restrictions where necessary
- [ ] Partner with local legal counsel in expansion regions
- [ ] Maintain regulatory monitoring process

---

## 5. Organizational & Team Risks

### 5.1 Key Person Dependency
**Risk Level:** MEDIUM

**Issue:**
- Critical features owned by one developer
- Loss of institutional knowledge if person leaves
- Bottleneck on approvals or decisions

**Mitigation:**
- [ ] Pair programming on critical modules
- [ ] Comprehensive documentation: Architecture, API, deployment
- [ ] Code review process: No single-approver merges
- [ ] Weekly knowledge-sharing sessions
- [ ] Runbooks for common operations (backup, restore, scaling)
- [ ] Cross-training on key systems

### 5.2 Feature Scope Creep
**Risk Level:** MEDIUM

**Issue:**
- New requirements added mid-sprint
- Timeline delays, budget overruns
- Quality suffers from rushing

**Mitigation:**
- [ ] Strict product roadmap: Prioritized backlog
- [ ] Change control process: Require sign-off for scope changes
- [ ] Fixed-scope sprints: No mid-sprint additions
- [ ] MVP focus: Launch with core features only
- [ ] Feedback loop: Collect user requests, prioritize quarterly
- [ ] Say "no" to nice-to-have features in v1

---

## 6. Data & Model Risks

### 6.1 AI Model Hallucination or Biases
**Risk Level:** MEDIUM-HIGH

**Issue:**
- LLM invents citations or sources
- Biased responses on certain topics
- Misrepresentation of Islamic schools/madhhab
- Cultural insensitivity

**Mitigation:**
- [ ] Grounding enforcement: No answer without source
- [ ] Bias testing: Evaluate model on diverse queries, cultures
- [ ] Human review: Scholar-approved answers only on sensitive topics
- [ ] Diversity in training data review: Ensure multiple madhhab represented
- [ ] Community moderation: Scholars flag biased responses
- [ ] Continuous monitoring: Track user feedback for biases
- [ ] Model selection: Prefer models with low bias (test before deployment)

### 6.2 Knowledge Graph Inconsistencies
**Risk Level:** MEDIUM

**Issue:**
- Conflicting information from multiple books
- Extracted concepts don't match reality
- Relation inference errors
- Outdated information not refreshed

**Mitigation:**
- [ ] Conflict detection: Flag contradictory sources
- [ ] Scholar review: Consensus-building process
- [ ] Versioning: Track changes to concepts over time
- [ ] Source ranking: Prioritize older traditional sources
- [ ] Regular audits: Review extracted knowledge for accuracy
- [ ] Feedback loop: Users report inaccuracies

---

## 7. Timeline and Budget Risks

### 7.1 Underestimated Development Effort
**Risk Level:** MEDIUM

**Issue:**
- Initial estimates were too optimistic
- Unforeseen technical challenges
- Integration issues with Frappe environment

**Mitigation:**
- [ ] 30% contingency buffer in timeline (add 2 weeks per phase)
- [ ] Weekly sprint reviews: Track velocity and adjust
- [ ] Spike investigations early for high-uncertainty tasks
- [ ] Prototype risky features (AI adapter, pgvector) before committing
- [ ] Post-mortem after each phase to calibrate estimates

### 7.2 Third-Party Dependency Failures
**Risk Level:** MEDIUM

**Issue:**
- PyArabic or other Arabic packages no longer maintained
- Breaking API changes in dependencies
- Abandoned library affects core feature

**Mitigation:**
- [ ] Vendor critical libraries (copy into repo if needed)
- [ ] Monitor dependency updates monthly
- [ ] Have backup libraries identified (e.g., Farasa for Arabic NLP)
- [ ] Abstract away third-party deps behind adapter layer
- [ ] Pin versions in requirements.txt; test upgrades before deploy

---

## Risk Matrix Summary

| Risk | Level | Phase | Mitigation Lead |
|------|-------|-------|-----------------|
| VPS Resource Contention | HIGH | Deployment | DevOps/Infra |
| AI Provider Unavailability | HIGH | Phase 4 | Backend Lead |
| Database Corruption | CRITICAL | Ongoing | DevOps |
| Sensitive Topic Mishandling | CRITICAL | Phase 1 | Product Manager |
| Unauthorized Data Access | HIGH | Phase 2 | Security Lead |
| Authentication Bypass | HIGH | Phase 1 | Backend Lead |
| SQL Injection | HIGH | Ongoing | All Developers |
| API Key Exposure | HIGH | Phase 1 | DevOps/Security |
| DoS / DDoS | MEDIUM-HIGH | Deployment | DevOps |
| Deployment Failure | HIGH | Phase 9 | DevOps |
| Monitoring Gaps | MEDIUM | Deployment | DevOps |
| Backup Failure | HIGH | Phase 9 | DevOps |
| Scaling Limitations | MEDIUM | Phase 8 | Backend/DevOps |
| GDPR Violations | CRITICAL | Phase 1 | Legal/Compliance |
| Copyright Issues | HIGH | Phase 3 | Legal |
| AI Misrepresentation | MEDIUM | Phase 4 | Product/Legal |
| Key Person Dependency | MEDIUM | Ongoing | Team Lead |
| Scope Creep | MEDIUM | Ongoing | Product Manager |
| AI Hallucination | MEDIUM-HIGH | Phase 4 | ML/QA Lead |
| Development Delays | MEDIUM | Ongoing | Project Manager |

---

## Governance & Risk Review Process

- **Monthly:** Risk review meeting, update mitigation status
- **Quarterly:** Risk reassessment, new risks identified
- **Incident Response:** Postmortem within 24 hours, RCA, preventive measures
- **Escalation:** Any CRITICAL or HIGH risk → immediate attention