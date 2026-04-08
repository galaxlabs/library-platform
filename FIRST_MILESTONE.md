# First Coding Milestone: Complete Auth System (Weeks 1-3)

## Objective
Establish a production-ready authentication and user management foundation. This milestone enables all future work and establishes patterns for the entire platform.

## Deliverables

### 1. User Registration & Login API
- **Endpoint:** `POST /api/v1/auth/register/`
  - Input: email, full_name, arabic_name (optional), phone, preferred_lang_pair, password
  - Returns: user object + JWT tokens (access, refresh)
  - Validation: Email unique, password 8+ chars, email verification

- **Endpoint:** `POST /api/v1/auth/login/`
  - Input: email, password
  - Returns: user object + JWT tokens
  - Features: Rate limiting (5 attempts/minute), lockout after 5 failures

- **Endpoint:** `POST /api/v1/auth/token/refresh/`
  - Input: refresh_token
  - Returns: new access_token
  - Features: Token rotation, revocation on logout

### 2. User Profile Management
- **Endpoint:** `GET /api/v1/users/me/`
  - Returns: Current user's full profile
  - Includes: Roles, institute, class, preferences

- **Endpoint:** `PATCH /api/v1/users/me/`
  - Update: full_name, arabic_name, phone, preferred_lang_pair
  - Restrictions: Cannot change email or roles via this endpoint

- **Endpoint:** `POST /api/v1/auth/password-change/`
  - Input: old_password, new_password
  - Validation: Confirm old password, enforce password complexity

### 3. Role System Foundation
- Roles: Admin, Institute Admin, Scholar, Teacher, Student, Reviewer
- Permission checks on auth endpoints (e.g., only Admins can access certain endpoints)
- Role assignment via Django admin (manual for now)
- Role validation in JWT tokens

### 4. Frontend Login/Auth Flow
- **Pages:**
  - `/login` - Login form
  - `/register` - Registration form
  - `/change-password` - Password change (authenticated)
  - `/forgot-password` - Password reset flow (optional in MVP)

- **Features:**
  - Form validation (client + server)
  - Error messages and feedback
  - Redirect to dashboard on successful login
  - Protected routes: Redirect unauthenticated users to login
  - Token persistence in localStorage or HttpOnly cookie
  - Auto-refresh token before expiry

### 5. Test Coverage
- Unit tests: User model, serializers, validators
- Integration tests: Registration, login, token refresh
- Permission tests: Auth required endpoints
- E2E tests: Full registration → login → dashboard flow
- Security tests: Rate limiting, brute force protection, SQL injection

### 6. Documentation
- API documentation (Swagger/OpenAPI)
- Setup guide: How to run backend locally
- Setup guide: How to run frontend locally
- Deployment steps for production
- Database migration guide

---

## Implementation Checklist

### Backend (Django)

#### Setup & Configuration
- [ ] Create Django project structure (config/, apps/)
- [ ] Create virtual environment and install dependencies
- [ ] Configure PostgreSQL database settings
- [ ] Create `.env` file with secrets template
- [ ] Set up logging configuration
- [ ] Configure CORS and JWT settings

#### Core Models
- [ ] Create BaseModel (common/models.py) ✅
- [ ] Create User model with custom manager ✅
- [ ] Create Role model ✅
- [ ] Create AuditLog model ✅
- [ ] Create PermissionGrant model ✅
- [ ] Database migrations

#### Serializers
- [ ] UserSerializer ✅
- [ ] RegisterSerializer with validation ✅
- [ ] LoginSerializer with authentication ✅
- [ ] PasswordChangeSerializer
- [ ] Role serializers

#### Views & Endpoints
- [ ] RegisterView ✅
- [ ] LoginView ✅
- [ ] UserViewSet with me() action ✅
- [ ] PasswordChangeView
- [ ] TokenRefreshView (from simplejwt)

#### Authentication & Permissions
- [ ] Custom JWT authentication
- [ ] Permission classes (IsAdmin, IsScholar, etc.) ✅
- [ ] Permission checks on views
- [ ] Rate limiting middleware/decorators
- [ ] CSRF protection setup

#### Utilities
- [ ] User model custom manager (create_user, create_superuser)
- [ ] Token generation and validation
- [ ] Password hashing and validation
- [ ] Email validation utilities
- [ ] Audit logging helpers ✅

#### Middleware & Security
- [ ] SecurityHeadersMiddleware ✅
- [ ] AuditLoggingMiddleware ✅
- [ ] RateLimitMiddleware ✅
- [ ] CORS configuration ✅
- [ ] CSRF protection

#### URL Routing
- [ ] Django URL configuration ✅
- [ ] API v1 namespace setup ✅
- [ ] Auth endpoints mounted ✅
- [ ] Router for UserViewSet ✅

#### Admin Interface
- [ ] Register User, Role, AuditLog, PermissionGrant in admin
- [ ] Custom admin filters and search
- [ ] Bulk actions (change roles, reset passwords)
- [ ] Read-only fields for sensitive data

#### Testing
- [ ] Test user registration (valid, invalid, duplicate email)
- [ ] Test login (valid, invalid credentials)
- [ ] Test token refresh
- [ ] Test password change
- [ ] Test permission checks
- [ ] Test rate limiting
- [ ] Test JWT expiry and refresh
- [ ] >80% code coverage for auth app

### Frontend (Next.js)

#### Setup
- [ ] Create Next.js project with App Router
- [ ] Install dependencies (axios, tailwind, flowbite, etc.)
- [ ] Configure environment variables (.env.local)
- [ ] Set up Tailwind CSS and custom theme
- [ ] Configure TypeScript

#### Layout & Components
- [ ] Root app shell layout
- [ ] Top navigation bar
- [ ] Authentication context/provider (useAuth hook)
- [ ] Protected route wrapper component
- [ ] Loading spinner component
- [ ] Error boundary component
- [ ] Form components (input, button, error messages)
- [ ] Card component (reusable)

#### Pages & Routes
- [ ] `/login` page ✅ (created)
- [ ] `/register` page
- [ ] `/dashboard` page (placeholder for now)
- [ ] `/settings/change-password` page
- [ ] `/settings/profile` page
- [ ] Catch-all redirect for unauthenticated users

#### Authentication Logic
- [ ] Login form component
- [ ] Registration form component
- [ ] Password change form component
- [ ] Token storage (localStorage or cookies)
- [ ] Token refresh logic
- [ ] API client with token injection
- [ ] Error handling and user feedback

#### State Management (if needed)
- [ ] useAuth hook (custom or Context API)
- [ ] User state (logged in, roles, profile)
- [ ] Token management (storage, refresh)
- [ ] Error state and handling

#### Styling & UX
- [ ] Mobile-first responsive design
- [ ] Dark mode support (optional)
- [ ] RTL/LTR support (future)
- [ ] Arabic text rendering
- [ ] Loading states
- [ ] Error notifications (toast or alerts)
- [ ] Form validation feedback

#### Testing
- [ ] Component unit tests (TanStack Testing Library)
- [ ] E2E tests (Cypress/Playwright)
  - Registration flow
  - Login flow
  - Protected route access
  - Token refresh scenario
  - Error scenarios
- [ ] Mobile responsiveness tests
- [ ] Accessibility tests (button labels, form fields)

#### Documentation
- [ ] Setup instructions
- [ ] Component storybook (optional)
- [ ] API integration guide
- [ ] Testing guide

### Deployment & Infrastructure

#### Backend Deployment
- [ ] Create requirements.txt with dependencies
- [ ] Create Dockerfile for backend
- [ ] Docker Compose for local dev
- [ ] Gunicorn configuration
- [ ] Environment setup script
- [ ] Database initialization script
- [ ] Create systemd service unit for Django

#### Frontend Deployment
- [ ] Create Dockerfile for Next.js
- [ ] Next.js build configuration
- [ ] Create systemd service unit for Next.js
- [ ] Environment setup for production

#### Nginx Reverse Proxy
- [ ] Configure Nginx server block ✅
- [ ] SSL certificate setup (certbot)
- [ ] API routing configuration ✅
- [ ] Frontend routing configuration ✅
- [ ] Static file caching
- [ ] Security headers setup ✅

#### Database
- [ ] PostgreSQL installation
- [ ] Database and user creation
- [ ] Initial schema setup
- [ ] Backup script automation

#### Monitoring & Logging
- [ ] Application logging setup
- [ ] Access logs for Nginx
- [ ] Error tracking (Sentry optional)
- [ ] Health check endpoints

---

## Success Criteria

- [ ] All API endpoints working and tested
- [ ] User can register with email
- [ ] User can login and receive JWT tokens
- [ ] JWT tokens validated on protected endpoints
- [ ] Tokens refresh before expiry
- [ ] Rate limiting prevents brute force
- [ ] Frontend pages load without errors
- [ ] Login redirects to dashboard on success
- [ ] Logout clears tokens
- [ ] Protected routes redirect to login when unauthenticated
- [ ] Roles assigned and permissions enforced
- [ ] Audit logs created for auth events
- [ ] >80% test coverage
- [ ] API documented (Swagger)
- [ ] Code review approved
- [ ] Deployed to staging environment
- [ ] Manual smoke tests passed

---

## Dependencies & Tools

**Backend:**
- Django 5.0
- Django REST Framework
- djangorestframework-simplejwt
- django-cors-headers
- django-celery-beat
- psycopg2 (PostgreSQL)
- cryptography (for encryption)

**Frontend:**
- Next.js 14
- React 18
- Tailwind CSS
- Flowbite React
- Axios

**Deployment:**
- Docker & Docker Compose
- Nginx
- PostgreSQL
- Gunicorn
- Systemd

**Testing:**
- pytest (backend)
- Cypress or Playwright (E2E)
- TanStack Testing Library (frontend)

**Monitoring:**
- Sentry (error tracking, optional)
- Application logs

---

## Timeline (Weeks 1-3)

| Week | Task | Owner |
|------|------|-------|
| 1 | Backend setup, models, serializers, basic views | Backend Lead |
| 1 | Frontend setup, login/register pages | Frontend Lead |
| 2 | Auth endpoints complete, JWT working | Backend Lead |
| 2 | Frontend auth flow, token management | Frontend Lead |
| 2-3 | Testing: unit, integration, E2E | QA / All |
| 3 | Documentation, code review, staging deployment | All |
| 3 | Smoke tests, bug fixes | All |

---

## Definition of Done

✅ Complete when:
- All checklist items marked complete
- Code review approved
- Tests passing (>80% coverage)
- No critical bugs
- Documentation written
- Staged deployment successful
- Team sign-off