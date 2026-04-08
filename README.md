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
