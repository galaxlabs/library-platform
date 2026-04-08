# مكتبة النحو - Scholarly AI Learning Platform

A production-grade, Arabic-first scholarly AI learning platform for Islamic and Arabic books. Built with Django, Next.js, and modern cloud-native technologies.

## 🎯 Features

- **Source-Grounded AI Answers**: All responses backed by uploaded books and verified sources
- **Scholar Verification System**: Multi-level expert approval workflow
- **Skill Packs**: Subject-specific answer templates (Nahw, Sarf, Fiqh, etc.)
- **Guided Book Ingestion**: Upload → Metadata → AI Analysis → Review → Publish
- **Multi-Institute Support**: Single platform, isolated content per institute
- **Adaptive Learning**: Personalized exercises and progress tracking
- **Multiple AI Providers**: Gemini, OpenRouter, Ollama (local) with fallback support
- **Arabic-First Design**: RTL/LTR support, Arabic+Urdu, Arabic+English
- **Role-Based Access**: Admin, Institute Admin, Scholar, Teacher, Student, Reviewer

## 🛠 Tech Stack

### Backend
- Django 5.0 + Django REST Framework
- PostgreSQL with pgvector for semantic search
- Celery + Redis for async tasks (OCR, embeddings, etc.)
- JWT authentication (SimpleJWT)

### Frontend
- Next.js 14 (App Router)
- React 18
- Tailwind CSS + Flowbite components
- Mobile-first, responsive design

### AI & Language
- Google Gemini adapter
- OpenRouter adapter
- Ollama support (local/private deployments)
- PyArabic, libqutrub for Arabic processing
- Cryptography for key encryption

### Deployment
- Docker & Docker Compose
- Nginx reverse proxy
- Systemd services
- PostgreSQL + Redis on VPS

## 📋 Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
# Open http://localhost:3000
```

### Docker Compose (All Services)

```bash
docker-compose up -d
# Backend: http://localhost:8001
# Frontend: http://localhost:3000
# API Docs: http://localhost:8001/api/v1/docs/
```

## ✅ Migration Fixes and What Was Resolved

During setup we fixed several backend issues so migration could complete successfully:

- Matched database settings between `backend/.env`, `backend/config/settings/development.py`, and `docker-compose.yml`
- Ensured the database name is `library_db` and the user/password are `library_user` / `library_password`
- Started PostgreSQL and Redis services with Docker Compose
- Created missing app migrations for `accounts` and `institutes`
- Resolved a circular migration dependency between `accounts.User` and `institutes.Institute` by splitting the model migrations into two phases:
  - `institutes.0001_initial` created `Institute`, `ClassDarjah`, and `Subject`
  - `accounts.0001_initial` created the custom `User` and `Role` models without the foreign key fields
  - `accounts.0002_auto...` added `institute` and `class_darjah` fields to `User`
  - `institutes.0002_auto...` added the `admin` foreign key to `Institute`
- After these changes, `python manage.py migrate --noinput` completed successfully

## 🔐 Admin Portal Login

The Django admin portal is available at:

- `http://localhost:8001/admin/`
- `http://127.0.0.1:8001/admin/`

Important notes:

- You must create a superuser first:
  ```bash
  cd backend
  source venv/bin/activate
  python manage.py createsuperuser
  ```
- This project uses a custom user model with `USERNAME_FIELD = 'email'`, so login uses email and password
- If you see login failure, check that the superuser exists and use the correct email/password pair
- If you still cannot log in, try clearing cookies, using a private browser window, or recreating the superuser

## 🌐 UI Address and 404 Explanation

The backend root URL is not a homepage, so this is expected:

- `http://127.0.0.1:8001/` → 404 because only `admin/`, `api/v1/`, `media/`, and `static/` are configured

The actual frontend UI is served separately by Next.js at:

- `http://localhost:3000/`

If you want production-style access via domain and port 80, point your domain to the server IP and configure Nginx to proxy traffic to the frontend/backend ports. For example:

- Server IP: `your.server.ip.address` → point DNS A record to this IP
- UI: `http://library.digigalaxy.cloud/` → proxy to `http://localhost:3000`
- Admin: `http://library.digigalaxy.cloud/admin/` → proxy to `http://localhost:8001/admin/`
- API: `http://library.digigalaxy.cloud/api/v1/` → proxy to `http://localhost:8001/api/v1/`

If you want the backend on port 80 directly, use Nginx reverse proxy instead of exposing Django directly. Keep the app running on `localhost:8001` and let Nginx forward public requests from port 80.

### Example Nginx proxy config

```nginx
server {
    listen 80;
    server_name library.digigalaxy.cloud;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8001/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/v1/ {
        proxy_pass http://127.0.0.1:8001/api/v1/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📖 Documentation

- [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md) - 30-week development plan
- [FIRST_MILESTONE.md](./FIRST_MILESTONE.md) - Phase 1 auth system details
- [RISKS_AND_MITIGATION.md](./RISKS_AND_MITIGATION.md) - Risk management strategy
- [EXACT_FILES_TO_CREATE.md](./EXACT_FILES_TO_CREATE.md) - Complete file checklist
- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - System architecture
- [docs/API.md](./docs/API.md) - API documentation
- [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) - Deployment guide

## 🏗 Project Structure

```
library-platform/
├── backend/               # Django project
│   ├── config/           # Django settings, URLs
│   ├── apps/             # Modular Django apps
│   │   ├── accounts/     # Auth, users, roles
│   │   ├── institutes/   # Multi-institute support
│   │   ├── library/      # Books, files, metadata
│   │   ├── ingestion/    # Upload, OCR pipeline
│   │   ├── knowledge/    # Concepts, topics, graph
│   │   ├── skills/       # Skill packs
│   │   ├── qa_engine/    # Query, retrieval, answers
│   │   ├── learning/     # Exercises, progress
│   │   ├── scholars/     # Scholar profiles, reviews
│   │   ├── ai_providers/ # AI adapters
│   │   ├── analytics/    # Metrics, dashboards
│   │   └── common/       # Shared utilities
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Next.js project
│   ├── app/             # App Router pages
│   ├── components/      # Reusable components
│   ├── lib/             # Utilities, API client
│   ├── public/          # Static assets
│   ├── package.json
│   └── Dockerfile
├── infra/               # Infrastructure
│   ├── nginx/           # Nginx config
│   └── systemd/         # Service units
├── docs/                # Documentation
├── scripts/             # Utility scripts
├── docker-compose.yml   # Local dev environment
└── README.md
```

## 🚀 Deployment

### Production on Same VPS with Frappe

The platform is designed to coexist with existing Frappe/bench:

```
Same VPS:
├── Frappe Bench (existing)
│   ├── Port 8000 (gunicorn)
│   ├── Port 9000 (socketio)
│   └── Domain: digihoopoe.com
│
├── Library Platform (new)
│   ├── Django: Port 8001
│   ├── Next.js: Port 3000
│   ├── Celery: Background workers
│   ├── PostgreSQL: Separate DB
│   ├── Redis: Separate DB/index
│   └── Domain: library.digigalaxy.cloud
│
└── Nginx
    ├── Reverse proxy for both platforms
    ├── SSL termination
    └── Static file serving
```

### Deployment Steps

1. **Infrastructure Setup**
   ```bash
   ./infra/scripts/setup.sh
   ```

2. **Database & Environment**
   ```bash
   createdb library_db
   createuser library_user
   cd backend && python manage.py migrate
   ```

3. **Start Services**
   ```bash
   systemctl start library-django
   systemctl start library-celery
   systemctl start library-frontend
   ```

4. **Verify Nginx**
   ```bash
   nginx -t
   systemctl restart nginx
   ```

See [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed steps.

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=apps

# Frontend tests
cd frontend
npm run test
npm run test:e2e  # E2E with Cypress
```

## 📊 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8001/api/v1/docs/
- **ReDoc**: http://localhost:8001/api/v1/redoc/

## 🔐 Security

- Encrypted API keys (Fernet cipher)
- JWT authentication with refresh rotation
- Role-based permissions on all endpoints
- Audit logging for all actions
- HTTPS/TLS enforced in production
- SQL injection protection (ORM only)
- CSRF protection
- Rate limiting on auth endpoints
- Input validation on all forms

## 📱 Features by Phase

### Phase 1 (Weeks 1-3): Auth & Foundation ✅
- User registration/login
- Role system
- Permission checks
- Audit logging

### Phase 2-11 (Weeks 4+): Full Platform
See [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md) for all phases.

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/feature-name`
2. Follow code style (black, flake8)
3. Write tests (>80% coverage)
4. Submit PR with description

## 📄 License

TBD

## 👥 Team

- **Product**: Senior architect, product designer
- **Backend**: Django/DRF specialist
- **Frontend**: Next.js/React specialist
- **DevOps**: Infrastructure and deployment
- **QA**: Testing and security

## 🚦 Status

- **v0.1**: Architecture & Design ✅
- **v0.2**: Auth System (In Progress, Weeks 1-3)
- **v1.0**: MVP Launch (Weeks 30+)

## 📞 Support

For issues, questions, or contributions, please open a GitHub issue or contact the team.

---

**Built with ❤️ for Islamic scholarship and modern education.**
