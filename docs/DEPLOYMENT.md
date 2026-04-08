# Deployment Guide

## Prerequisites

- Ubuntu 20.04+ server
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Nginx 1.18+

## System Setup

### 1. Create System User

```bash
sudo useradd -m -s /bin/bash library-user
sudo usermod -aG sudo library-user
```

### 2. Install Dependencies

```bash
sudo apt update
sudo apt install -y \
  python3.11 \
  python3.11-dev \
  python3.11-venv \
  postgresql \
  postgresql-contrib \
  redis-server \
  nginx \
  git \
  curl \
  wget
```

### 3. Database Setup

```bash
sudo -u postgres psql << EOF
CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'strong-password';
ALTER ROLE library_user SET client_encoding TO 'utf8';
ALTER ROLE library_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE library_user SET default_transaction_deferrable TO on;
ALTER ROLE library_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
\q
EOF
```

### 4. Redis Setup

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
redis-cli ping  # Should return PONG
```

## Backend Deployment

### 1. Clone Repository

```bash
su - library-user
git clone https://github.com/your-org/library-platform.git
cd library-platform
```

### 2. Setup Python Environment

```bash
cd backend
python3.11 -m venv /home/library-user/venv
source /home/library-user/venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
cp .env.example .env
# Edit .env with production settings
nano .env
```

Key settings:
```
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=library.digigalaxy.cloud
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Database Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 5. Gunicorn Setup

```bash
sudo cp /home/library-user/library-platform/infra/systemd/library-django.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable library-django
sudo systemctl start library-django
sudo systemctl status library-django
```

### 6. Celery Setup

```bash
sudo cp /home/library-user/library-platform/infra/systemd/library-celery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable library-celery
sudo systemctl start library-celery
```

## Frontend Deployment

### 1. Setup Node Environment

```bash
su - library-user
cd library-platform/frontend
```

### 2. Build Frontend

```bash
npm install
npm run build
```

### 3. Systemd Service

```bash
sudo cp /home/library-user/library-platform/infra/systemd/library-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable library-frontend
sudo systemctl start library-frontend
```

## Nginx Configuration

### 1. Copy Nginx Config

```bash
sudo cp /home/library-user/library-platform/infra/nginx/library.conf /etc/nginx/sites-available/library.conf
sudo ln -s /etc/nginx/sites-available/library.conf /etc/nginx/sites-enabled/
```

### 2. SSL Certificates with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d library.digigalaxy.cloud
```

### 3. Verify and Restart Nginx

```bash
sudo nginx -t
sudo systemctl restart nginx
```

## Monitoring & Logs

### View Logs

```bash
sudo journalctl -u library-django -f
sudo journalctl -u library-celery -f
sudo journalctl -u library-frontend -f
```

### Nginx Logs

```bash
sudo tail -f /var/log/nginx/library_access.log
sudo tail -f /var/log/nginx/library_error.log
```

## Backup

### Database Backup

```bash
sudo -u postgres pg_dump library_db > library_db_backup_$(date +%Y%m%d).sql
```

### Automated Daily Backups

```bash
crontab -e
# Add: 0 2 * * * sudo -u postgres pg_dump library_db > /backups/library_db_$(date +\%Y\%m\%d).sql
```

## Troubleshooting

### Check Service Status

```bash
sudo systemctl status library-django
sudo systemctl status library-celery
sudo systemctl status library-frontend
sudo systemctl status nginx
```

### Restart Services

```bash
sudo systemctl restart library-django
sudo systemctl restart library-celery
sudo systemctl restart library-frontend
```

### Check Connectivity

```bash
curl http://localhost:8001/api/v1/health/  # Backend
curl http://localhost:3000  # Frontend
```

## Security Hardening

1. Configure firewall (UFW):
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. Disable root SSH login
3. Use SSH keys only (no passwords)
4. Keep system updated: `sudo apt update && sudo apt upgrade -y`
5. Regular security audits

## Performance Tuning

- Increase Gunicorn workers: `--workers=4`
- Configure PostgreSQL for production load
- Enable Redis persistence
- Implement CDN for static assets  
- Use database connection pooling
