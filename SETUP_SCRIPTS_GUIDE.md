# 🚀 Live Setup Scripts - Reference Guide

## Overview

I've created comprehensive setup scripts for your Library Platform to run on port 80 (via Nginx) with:
- **Frontend First** (default serving at `/`)
- **Backend API** (at `/api/v1`)
- **Existing Nginx** already deployed on port 80

---

## 📝 Script Files Created

### 1. **setup-live.sh** ⭐ Main Setup Script
**Purpose**: Full automated setup from scratch

**What it does**:
- ✅ Checks Python & Node.js prerequisites
- ✅ Creates Python virtual environment
- ✅ Installs 38 backend Python packages
- ✅ Installs frontend dependencies (npm)
- ✅ Creates `.env` files from templates
- ✅ Runs database migrations
- ✅ Builds frontend for production
- ✅ Creates admin user
- ✅ Generates service scripts
- ✅ Creates logs directories

**How to run**:
```bash
cd /home/fg/library-platform
bash setup-live.sh
```

**Time**: ~10-15 minutes (first run with npm install)

---

### 2. **start-live.sh** Start Services
**Purpose**: Start backend and frontend

**What it does**:
- Starts Django backend (gunicorn on port 8001)
- Starts Next.js frontend (npm start on port 3000)
- Creates log files
- Runs as background processes

**How to run**:
```bash
bash start-live.sh
```

**Output**:
```
Starting backend on port 8001...
Backend started (PID: check logs/gunicorn_error.log)
Starting frontend on port 3000...
Frontend started (PID: 12345)

Services are starting...
Frontend:  http://localhost:3000
Backend:   http://localhost:8001/api/v1
Nginx:     http://localhost (port 80)
```

---

### 3. **stop-live.sh** Stop Services
**Purpose**: Gracefully stop all services

**What it does**:
- Terminates frontend (npm start process)
- Terminates backend (gunicorn process)
- Waits 2 seconds between stops

**How to run**:
```bash
bash stop-live.sh
```

---

### 4. **restart-live.sh** Restart Services
**Purpose**: Stop and start all services

**What it does**:
- Calls `stop-live.sh`
- Waits 3 seconds
- Calls `start-live.sh`

**How to run**:
```bash
bash restart-live.sh
```

---

### 5. **status-live.sh** Check Status
**Purpose**: Verify all services are running

**What it does**:
- Checks if backend (gunicorn) is running
- Checks if frontend (npm) is running
- Checks if Nginx is running
- Shows port status

**How to run**:
```bash
bash status-live.sh
```

**Output**:
```
Checking services status...

✓ Backend (gunicorn) - Running on port 8001
✓ Frontend (Next.js) - Running on port 3000
✓ Nginx - Running (port 80/443)

Port Status:
tcp  0  0 0.0.0.0:80     0.0.0.0:*  LISTEN
tcp  0  0 0.0.0.0:3000   0.0.0.0:*  LISTEN
tcp  0  0 127.0.0.1:8001 0.0.0.0:*  LISTEN
```

---

## 🔄 Typical Workflow

### First Time Setup
```bash
cd /home/fg/library-platform

# 1. Run full setup
bash setup-live.sh

# 2. Edit environment files with your values
nano backend/.env
nano frontend/.env.production

# 3. Configure Nginx (if not already done)
sudo cp infra/nginx/library.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/library.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 4. Start services
bash start-live.sh

# 5. Check status
bash status-live.sh
```

### Daily Operations
```bash
# Start services in morning
bash start-live.sh

# Monitor status
bash status-live.sh

# View logs
tail -f backend/logs/gunicorn_error.log

# Stop services at end of day
bash stop-live.sh
```

### Deployment Updates
```bash
# Stop services
bash stop-live.sh

# Pull new code (if using git)
git pull

# Install any new dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install --legacy-peer-deps

# Rebuild frontend
npm run build

# Run new migrations
cd backend && source venv/bin/activate && python manage.py migrate

# Start services
bash start-live.sh
```

---

## 📂 File Structure After Setup

```
library-platform/
├── setup-live.sh           ← Main setup script
├── start-live.sh           ← Start services script
├── stop-live.sh            ← Stop services script
├── restart-live.sh         ← Restart services script
├── status-live.sh          ← Status check script
├── DEPLOYMENT_INFO.md      ← Created by setup script
├── backend/
│   ├── venv/               ← Virtual environment (created)
│   ├── .env                ← Environment variables (created)
│   ├── logs/               ← Log files directory (created)
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   └── ...
├── frontend/
│   ├── .next/              ← Built app (created by npm build)
│   ├── node_modules/       ← npm packages (created)
│   ├── logs/               ← Log files directory (created)
│   ├── .env.production     ← Environment variables (created)
│   ├── package.json
│   └── ...
└── infra/
    ├── nginx/
    │   └── library.conf
    └── ...
```

---

## 🔑 Service Architecture

```
Internet/Port 80 (External)
    ↓
Nginx Reverse Proxy (localhost:80)
    ├─ / → Frontend (localhost:3000)
    ├─ /_next/* → Frontend static (localhost:3000)
    ├─ /api/* → Backend API (localhost:8001)
    └─ /admin/* → Django Admin (localhost:8001)
    
Frontend (Next.js, localhost:3000)
    ↓ (API calls)
Backend (Django, localhost:8001)
    ↓
PostgreSQL Database
Redis Cache
```

---

## 👤 Default Credentials

| Service | Username | Password | URL |
|---------|----------|----------|-----|
| Admin Portal | admin | admin123 | http://localhost/admin |
| API | (Bearer Token) | - | http://localhost/api/v1 |

⚠️ **IMPORTANT**: Change these immediately in production!

---

## 🔧 Environment Files

### backend/.env (created by setup-live.sh)
```
DEBUG=False
DJANGO_SECRET_KEY=<generated>
ALLOWED_HOSTS=localhost,library.digigalaxy.cloud

DB_ENGINE=django.db.backends.postgresql
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=<change-this>
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### frontend/.env.production (created by setup-live.sh)
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_APP_NAME="مكتبة النحو"
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

---

## 📊 Port Configuration

| Service | Port | Type | Role |
|---------|------|------|------|
| Nginx | 80 | HTTP | Reverse proxy (external) |
| Nginx | 443 | HTTPS | SSL reverse proxy (external) |
| Frontend | 3000 | HTTP | Internal only |
| Backend | 8001 | HTTP | Internal only |
| PostgreSQL | 5432 | TCP | Database (internal) |
| Redis | 6379 | TCP | Cache (internal) |

---

## 🔍 Logging

All services log to `/home/fg/library-platform/*/logs/`:

```bash
# Backend logs
tail -f backend/logs/gunicorn_error.log
tail -f backend/logs/gunicorn_access.log

# Frontend logs
tail -f frontend/logs/frontend.log

# Nginx logs
sudo tail -f /var/log/nginx/library_access.log
sudo tail -f /var/log/nginx/library_error.log

# Combined view
tail -f backend/logs/gunicorn_*.log frontend/logs/*.log
```

---

## ⚡ Performance Tuning (After Setup)

### Backend (Gunicorn Workers)
Edit `start-live.sh` and adjust:
```bash
--workers 4          # Increase for more CPU cores
--worker-class sync  # Or 'gevent' for async
--timeout 120        # Increase if requests are slow
```

### Frontend (Next.js)
Built for production in setup-live.sh - optimized automatically

### Database Connection Pool
Adjust in `backend/.env`:
```
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 8001
lsof -i :8001

# Kill process (be careful!)
kill -9 <PID>
```

### Backend Won't Start
```bash
cd backend
source venv/bin/activate
python manage.py check       # Check for errors
gunicorn config.wsgi:application --bind 127.0.0.1:8001 --timeout 120
# Check output for errors
```

### Frontend Won't Start
```bash
cd frontend
npm install --legacy-peer-deps
npm run build
npm start
# Check output for errors
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U library_user -d library_db -c "SELECT 1;"

# Check .env file
cat backend/.env | grep DB_
```

### Nginx Not Routing Correctly
```bash
# Test Nginx config
sudo nginx -t

# Check config file
cat /etc/nginx/sites-available/library.conf

# View error log
sudo tail -f /var/log/nginx/error.log
```

---

## 📋 Setup Checklist

After `bash setup-live.sh`:

- [ ] Edit `backend/.env` with real credentials
- [ ] Edit `frontend/.env.production` if needed
- [ ] Configure Nginx (copy config, enable, restart)
- [ ] Test services with `bash status-live.sh`
- [ ] Access frontend at http://localhost:3000
- [ ] Access admin at http://localhost/admin
- [ ] Change default admin password
- [ ] Create test users

---

## 🎯 Quick Reference

```bash
# Setup everything
bash setup-live.sh

# Daily startup
bash start-live.sh && bash status-live.sh

# Daily shutdown
bash stop-live.sh

# Check everything is working
bash status-live.sh

# View logs
tail -f backend/logs/gunicorn_error.log

# Full restart
bash restart-live.sh
```

---

## 📚 Additional Resources

- **Full Deployment Guide**: See `LIVE_DEPLOYMENT_SETUP.md`
- **Architecture**: See `ARCHITECTURE.md`
- **API Documentation**: See `API.md`
- **Deployment Details**: See `DEPLOYMENT_INFO.md`

---

## ✅ Summary

You now have production-ready setup scripts that:
1. ✅ Automate all configuration
2. ✅ Run frontend by default (port 80)
3. ✅ Work with existing Nginx setup
4. ✅ Create service management scripts
5. ✅ Generate logs and documentation
6. ✅ Support easy restarts and updates

**Get started**: `bash setup-live.sh`
