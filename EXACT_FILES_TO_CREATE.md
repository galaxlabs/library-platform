# Exact Files to Create First (Priority Order)

This document lists all files required to start development for the First Coding Milestone, in the order they should be created.

---

## Priority 0: Project Initialization (Do First)

### 1. Root `.env.example`
**Path:** `/home/fg/library-platform/.env.example`
**Purpose:** Template for environment variables
**Contents:**
```
# Django
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,library.digigalaxy.cloud

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=your-db-password-here
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Providers
ENCRYPTION_KEY=your-fernet-key-here

# JWT
JWT_SECRET=your-jwt-secret-here
JWT_EXP_DELTA_SECONDS=900  # 15 minutes

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587

# API Keys (encrypted in database, not here)
GEMINI_API_KEY=
OPENROUTER_API_KEY=
```

### 2. Root `README.md`
**Path:** `/home/fg/library-platform/README.md`
**Purpose:** Project overview and quick start
**Sections:**
- Project Description
- Features
- Tech Stack
- Quick Start (backend, frontend, both)
- Project Structure
- Architecture Overview (link to docs)
- Development Workflow
- Deployment
- Contributing
- License

### 3. Root `.gitignore`
**Path:** `/home/fg/library-platform/.gitignore`
**Contents:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Django
*.db
*.sqlite3
/staticfiles/
/media/
.env
.env.local

# Node
node_modules/
npm-debug.log
yarn-error.log
.next/
out/

# IDE
.vscode/
.idea/
*.swp
*.swo
*.sublime-*

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/

# Logs
logs/
*.log
```

---

## Priority 1: Backend Core (Weeks 1-2)

### 4. `backend/requirements.txt`
**Path:** `/home/fg/library-platform/backend/requirements.txt`
**Key Packages:**
- Django==5.0
- djangorestframework==3.14
- djangorestframework-simplejwt==5.3
- django-cors-headers==4.3
- django-celery-beat==2.5
- django-celery-results==2.5
- psycopg2-binary==2.9
- celery==5.3
- redis==5.0
- cryptography==41.0
- python-decouple==3.8
- pillow==10.1
- requests==2.31
- pytest==7.4
- pytest-django==4.7
- factory-boy==3.3

### 5. `backend/pyproject.toml`
**Path:** `/home/fg/library-platform/backend/pyproject.toml`
**Purpose:** Project metadata, build config, tool configurations
**Sections:**
- Project name, version, description
- Dependencies and dev dependencies
- Tool configs (pytest, black, flake8, mypy)

### 6. `backend/manage.py` ✅ (Already created in step 1)

### 7. `backend/config/__init__.py`
**Path:** `/home/fg/library-platform/backend/config/__init__.py`
**Contents:**
```python
# Celery integration
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('library_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### 8. `backend/config/settings/__init__.py`
**Path:** `/home/fg/library-platform/backend/config/settings/__init__.py`
**Contents:** Empty or minimal (imports base.py)

### 9. `backend/config/settings/base.py` ✅ (Already created in step 2)

### 10. `backend/config/settings/development.py`
**Path:** `/home/fg/library-platform/backend/config/settings/development.py`
**Purpose:** Development-specific overrides
**Contents:**
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*.ngrok.io']

INSTALLED_APPS += [
    'django_extensions',
    'drf_yasg',  # Swagger
]

DATABASES['default']['NAME'] = 'library_db_dev'

CELERY_TASK_ALWAYS_EAGER = True  # Run tasks synchronously in dev

LOGGING['loggers'] = {
    'django': {'level': 'DEBUG'},
    'apps': {'level': 'DEBUG'},
}
```

### 11. `backend/config/settings/production.py`
**Path:** `/home/fg/library-platform/backend/config/settings/production.py`
**Purpose:** Production-specific overrides
**Contents:**
```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['library.digigalaxy.cloud']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

DATABASES['default']['ATOMIC_REQUESTS'] = True
```

### 12. `backend/config/wsgi.py`
**Path:** `/home/fg/library-platform/backend/config/wsgi.py`
**Purpose:** WSGI entry point for production
**Contents:**
```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_wsgi_application()
```

### 13. `backend/config/asgi.py`
**Path:** `/home/fg/library-platform/backend/config/asgi.py`
**Purpose:** ASGI entry point for async support (future websockets)
**Contents:**
```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_asgi_application()
```

### 14. `backend/config/urls.py` ✅ (Already created in step 11)

### 15. `backend/apps/__init__.py`
**Path:** `/home/fg/library-platform/backend/apps/__init__.py`
**Contents:** Empty or minimal

### 16. `backend/apps/common/__init__.py`
**Path:** `/home/fg/library-platform/backend/apps/common/__init__.py`

### 17. `backend/apps/common/models.py` ✅ (Already created in step 9)

### 18. `backend/apps/common/permissions.py` ✅ (Already created in step 12)

### 19. `backend/apps/common/middleware.py` ✅ (Already created in step 12)

### 20. `backend/apps/common/audit.py` ✅ (Already created in step 12)

### 21. `backend/apps/common/apps.py`
**Path:** `/home/fg/library-platform/backend/apps/common/apps.py`
**Contents:**
```python
from django.apps import AppConfig

class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.common'
```

### 22. `backend/apps/common/admin.py`
**Path:** `/home/fg/library-platform/backend/apps/common/admin.py`
**Contents:**
```python
from django.contrib import admin
from .audit import AuditLog, PermissionGrant

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'resource_type', 'created_at', 'success']
    list_filter = ['action', 'success', 'created_at']
    search_fields = ['user__username', 'resource_type']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

@admin.register(PermissionGrant)
class PermissionGrantAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission', 'granted_by', 'is_active']
    list_filter = ['permission', 'granted_at']
    search_fields = ['user__username', 'permission']
```

### 23. `backend/apps/accounts/__init__.py`

### 24. `backend/apps/accounts/apps.py`
**Path:** `/home/fg/library-platform/backend/apps/accounts/apps.py`
**Contents:**
```python
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
```

### 25. `backend/apps/accounts/models.py` ✅ (Already created in step 3)

### 26. `backend/apps/accounts/serializers.py` ✅ (Already created in step 8)

### 27. `backend/apps/accounts/views.py` ✅ (Already created in step 4)

### 28. `backend/apps/accounts/admin.py`
**Path:** `/home/fg/library-platform/backend/apps/accounts/admin.py`
**Contents:**
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('arabic_name', 'phone', 'preferred_lang_pair', 'institute', 'class_darjah')}),
        ('Roles', {'fields': ('roles',)}),
    )
    list_display = ['email', 'full_name', 'institute', 'is_staff', 'is_active']
    search_fields = ['email', 'full_name', 'arabic_name']
    filter_horizontal = ['roles', 'groups', 'user_permissions']
```

### 29. `backend/apps/accounts/urls.py`
**Path:** `/home/fg/library-platform/backend/apps/accounts/urls.py`
**Contents:**
```python
from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
```

### 30. `backend/apps/accounts/managers.py`
**Path:** `/home/fg/library-platform/backend/apps/accounts/managers.py`
**Contents:**
```python
from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return super().create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return super().create_superuser(email, password, **extra_fields)
```

### 31. `backend/apps/institutes/__init__.py`

### 32. `backend/apps/institutes/apps.py`
**Path:** `/home/fg/library-platform/backend/apps/institutes/apps.py`
**Contents:**
```python
from django.apps import AppConfig

class InstitutesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.institutes'
    verbose_name = 'Institutes'
```

### 33. `backend/apps/institutes/models.py`
**Path:** `/home/fg/library-platform/backend/apps/institutes/models.py`
**Purpose:** Institute, Class, Subject models (minimal for now)
**Contents:**
```python
from django.db import models
from apps.common.models import BaseModel

class Institute(BaseModel):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    policies = models.JSONField(default=dict)

class ClassDarjah(BaseModel):
    name = models.CharField(max_length=255)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    level = models.IntegerField()

class Subject(BaseModel):
    name = models.CharField(max_length=255)
```

### 34. `backend/apps/institutes/urls.py`
**Path:** `/home/fg/library-platform/backend/apps/institutes/urls.py`
**Contents:**
```python
from django.urls import path

urlpatterns = []
```

### 35. `backend/apps/scholars/models.py`, `urls.py`, `apps.py`
**Path:** `/home/fg/library-platform/backend/apps/scholars/`
**Purpose:** Placeholder apps for now
**Contents:** Minimal placeholder classes, empty URLs

**Similarly create for:**
- `backend/apps/library/`
- `backend/apps/ingestion/`
- `backend/apps/knowledge/`
- `backend/apps/skills/`
- `backend/apps/qa_engine/`
- `backend/apps/learning/`
- `backend/apps/ai_providers/`
- `backend/apps/analytics/`

### 36. `backend/apps/ai_providers/models.py` ✅ (Already created in step 10)

### 37. Initial Django Migrations Script
**Path:** `/home/fg/library-platform/scripts/init_db.sh`
**Purpose:** Setup script for database initialization
**Contents:**
```bash
#!/bin/bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < fixtures/initial_roles.py
```

---

## Priority 2: Frontend Core (Weeks 1-2)

### 38. `frontend/package.json` ✅ (Already created in step 5)

### 39. `frontend/tsconfig.json`
**Path:** `/home/fg/library-platform/frontend/tsconfig.json`
**Contents:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "isolatedModules": true,
    "incremental": true,
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

### 40. `frontend/next.config.js`
**Path:** `/home/fg/library-platform/frontend/next.config.js`
**Contents:**
```javascript
module.exports = {
  reactStrictMode: true,
  swcMinify: true,
  i18n: {
    locales: ['ar', 'en'],
    defaultLocale: 'ar',
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1',
  },
};
```

### 41. `frontend/tailwind.config.js`
**Path:** `/home/fg/library-platform/frontend/tailwind.config.js`
**Contents:**
```javascript
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    'node_modules/flowbite-react/lib/esm/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [require('flowbite/plugin')],
};
```

### 42. `frontend/postcss.config.js`
**Path:** `/home/fg/library-platform/frontend/postcss.config.js`
**Contents:**
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### 43. `frontend/.env.example`
**Path:** `/home/fg/library-platform/frontend/.env.example`
**Contents:**
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_APP_NAME="مكتبة النحو"
```

### 44. `frontend/app/layout.tsx`
**Path:** `/home/fg/library-platform/frontend/app/layout.tsx`
**Purpose:** Root layout with globals
**Contents:**
```typescript
import type { Metadata } from 'next';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: 'مكتبة النحو',
  description: 'منصة تعليمية ذكية',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
```

### 45. `frontend/app/(auth)/layout.tsx`
**Path:** `/home/fg/library-platform/frontend/app/(auth)/layout.tsx`
**Purpose:** Auth pages layout
**Contents:**
```typescript
export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
```

### 46. `frontend/app/(auth)/login/page.tsx` ✅ (Already created in step 6)

### 47. `frontend/app/(auth)/register/page.tsx`
**Path:** `/home/fg/library-platform/frontend/app/(auth)/register/page.tsx`
**Purpose:** Registration page (similar to login)

### 48. `frontend/app/dashboard/page.tsx`
**Path:** `/home/fg/library-platform/frontend/app/dashboard/page.tsx`
**Purpose:** Protected dashboard (placeholder)
**Contents:**
```typescript
'use client';
export default function DashboardPage() {
  return <h1>Dashboard</h1>;
}
```

### 49. `frontend/app/globals.css`
**Path:** `/home/fg/library-platform/frontend/app/globals.css`
**Purpose:** Global styles

### 50. `frontend/lib/api.ts`
**Path:** `/home/fg/library-platform/frontend/lib/api.ts`
**Purpose:** API client with token handling

### 51. `frontend/contexts/AuthContext.tsx`
**Path:** `/home/fg/library-platform/frontend/contexts/AuthContext.tsx`
**Purpose:** Auth state management

### 52. `frontend/hooks/useAuth.ts`
**Path:** `/home/fg/library-platform/frontend/hooks/useAuth.ts`
**Purpose:** useAuth custom hook

### 53. `frontend/components/ProtectedRoute.tsx`
**Path:** `/home/fg/library-platform/frontend/components/ProtectedRoute.tsx`
**Purpose:** Route protection wrapper

---

## Priority 3: Infrastructure (Week 3)

### 54. `backend/Dockerfile`
**Path:** `/home/fg/library-platform/backend/Dockerfile`

### 55. `frontend/Dockerfile`
**Path:** `/home/fg/library-platform/frontend/Dockerfile`

### 56. `docker-compose.yml`
**Path:** `/home/fg/library-platform/docker-compose.yml`
**Purpose:** Local dev environment

### 57. `infra/nginx/library.conf` ✅ (Already created in step 7)

### 58. `infra/systemd/library-django.service`
**Path:** `/home/fg/library-platform/infra/systemd/library-django.service`

### 59. `infra/systemd/library-celery.service`
**Path:** `/home/fg/library-platform/infra/systemd/library-celery.service`

### 60. `infra/systemd/library-frontend.service`
**Path:** `/home/fg/library-platform/infra/systemd/library-frontend.service`

---

## Priority 4: Documentation & Tests (Week 3)

### 61. `backend/tests/__init__.py`
**Path:** `/home/fg/library-platform/backend/tests/__init__.py`

### 62. `backend/tests/test_accounts.py`
**Path:** `/home/fg/library-platform/backend/tests/test_accounts.py`
**Purpose:** Auth tests

### 63. `FIRST_MILESTONE.md` ✅ (Already created in step 15)

### 64. `IMPLEMENTATION_ROADMAP.md` ✅ (Already created in step 13)

### 65. `RISKS_AND_MITIGATION.md` ✅ (Already created in step 14)

### 66. `docs/API.md`
**Path:** `/home/fg/library-platform/docs/API.md`
**Purpose:** API documentation

### 67. `docs/DEPLOYMENT.md`
**Path:** `/home/fg/library-platform/docs/DEPLOYMENT.md`
**Purpose:** Deployment guide

### 68. `docs/ARCHITECTURE.md`
**Path:** `/home/fg/library-platform/docs/ARCHITECTURE.md`
**Purpose:** Architecture overview

---

## Total Files to Create: 68

### Summary by Category:
- Core Configuration: 15 files
- Backend Code (Accounts & Common): 20 files
- Backend Placeholder Apps: 30 files
- Frontend Code: 15 files
- Infrastructure: 8 files
- Documentation & Tests: 8 files

### Next Steps After Creating These Files:
1. Run `pip install -r requirements.txt` in backend
2. Run `npm install` in frontend
3. Create `.env` from `.env.example`
4. Run Django migrations
5. Create superuser
6. Run dev servers
7. Test registration and login endpoints
8. Run full test suite