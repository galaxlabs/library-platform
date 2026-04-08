#!/bin/bash
# Quick Start Guide for Library Platform Live Setup

# ==============================================================================
# 📋 QUICK START - ONE COMMAND
# ==============================================================================

# cd /home/fg/library-platform
# bash setup-live.sh

# ==============================================================================
# 📋 MANUAL STEPS (if script fails)
# ==============================================================================

# 1. BACKEND SETUP
# ================
cd /home/fg/library-platform/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create environment file
cp .env.example .env
# EDIT: nano .env  (add your DB password, secret key, etc.)

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create admin user
python manage.py createsuperuser --noinput --username admin --email admin@library.local

# ==============================================================================
# 2. FRONTEND SETUP
# =================
cd /home/fg/library-platform/frontend

# Install dependencies
npm install --legacy-peer-deps

# Create environment file
cp .env.example .env.production

# Build for production
npm run build

# ==============================================================================
# 3. NGINX SETUP
# ==============
sudo cp /home/fg/library-platform/infra/nginx/library.conf /etc/nginx/sites-available/

# Verify nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# ==============================================================================
# 4. START SERVICES
# =================

# Option A: Using provided scripts (RECOMMENDED)
cd /home/fg/library-platform
bash start-live.sh
bash status-live.sh

# Option B: Manual startup
# Terminal 1 - Backend:
cd /home/fg/library-platform/backend
source venv/bin/activate
gunicorn config.wsgi:application --bind 127.0.0.1:8001 --workers 4

# Terminal 2 - Frontend:
cd /home/fg/library-platform/frontend
npm start

# ==============================================================================
# 5. VERIFY DEPLOYMENT
# ====================
curl http://localhost:3000           # Frontend
curl http://localhost:8001/api/v1    # Backend
curl http://localhost                # Nginx (via port 80)

# ==============================================================================
# 6. USEFUL COMMANDS
# ==================

# Check service status
bash /home/fg/library-platform/status-live.sh

# Stop all services
bash /home/fg/library-platform/stop-live.sh

# Restart all services
bash /home/fg/library-platform/restart-live.sh

# View backend logs
tail -f /home/fg/library-platform/backend/logs/gunicorn_error.log

# View frontend logs
tail -f /home/fg/library-platform/frontend/logs/frontend.log

# View nginx logs
sudo tail -f /var/log/nginx/library_access.log

# ==============================================================================
# 7. PATHS & LOCATIONS
# ====================

Project Location:     /home/fg/library-platform
Backend:              /home/fg/library-platform/backend
Frontend:             /home/fg/library-platform/frontend
Infrastructure:       /home/fg/library-platform/infra
Nginx Config:         /home/fg/library-platform/infra/nginx/library.conf
Service Scripts:      /home/fg/library-platform/start-live.sh
                      /home/fg/library-platform/stop-live.sh
                      /home/fg/library-platform/restart-live.sh
                      /home/fg/library-platform/status-live.sh

# ==============================================================================
# 8. PORTS & URLS
# ===============

Frontend (Next.js):   http://localhost:3000
Backend (Django):     http://localhost:8001
Admin Panel:          http://localhost/admin (via Nginx)
API:                  http://localhost/api/v1 (via Nginx)
Nginx (Port 80):      http://localhost

# ==============================================================================
# 9. CREDENTIALS
# ==============
Admin Username: admin
Admin Password: admin123

⚠️  CHANGE THESE IMMEDIATELY IN PRODUCTION!

# ==============================================================================
# 10. ENVIRONMENT VARIABLES
# =========================

Backend (.env):
  - DB_NAME, DB_USER, DB_PASSWORD
  - REDIS_URL
  - DJANGO_SECRET_KEY
  - DEBUG=False (for production)
  - ALLOWED_HOSTS=your.domain.com

Frontend (.env.production):
  - NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1

# ==============================================================================
# 11. TROUBLESHOOTING
# ===================

# Backend issues?
cd /home/fg/library-platform/backend
source venv/bin/activate
python manage.py check

# Frontend issues?
cd /home/fg/library-platform/frontend
npm install --legacy-peer-deps
npm run build

# Port in use?
lsof -i :8001
lsof -i :3000

# Database connection?
psql -U library_user -d library_db -c "SELECT 1;"

# ==============================================================================
