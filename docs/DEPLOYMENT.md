# Deployment Guide

This app must stay separate from the VPS’s existing Frappe / bench runtime. Do not place it inside bench, do not proxy it through bench, and do not reuse Frappe services.

## Target

- host: `72.60.118.195`
- domain: `library.digigalaxy.cloud`
- repo path: `/home/fg/library-platform`
- backend: Django + Gunicorn + Celery + Redis + PostgreSQL
- frontend: Next.js production server
- reverse proxy: Nginx

## 1. System Packages

```bash
sudo apt update
sudo apt install -y \
  python3.11 python3.11-venv python3.11-dev \
  postgresql postgresql-contrib \
  redis-server \
  nginx \
  build-essential \
  git curl
```

Install Node.js 20 LTS if it is not already present.

## 2. PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'change-me';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
\q
```

## 3. Backend Setup

```bash
cd /home/fg/library-platform/backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
cp .env.example .env
```

Set at minimum in `/home/fg/library-platform/backend/.env`:

```env
DEBUG=False
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
ALLOWED_HOSTS=localhost,127.0.0.1,72.60.118.195,library.digigalaxy.cloud
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://library.digigalaxy.cloud
CSRF_TRUSTED_ORIGINS=https://library.digigalaxy.cloud
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=replace-me
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
STATIC_ROOT=/home/fg/library-platform/backend/staticfiles
MEDIA_ROOT=/home/fg/library-platform/backend/media
```

Then run:

```bash
source /home/fg/library-platform/backend/venv/bin/activate
cd /home/fg/library-platform/backend
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 4. Frontend Setup

```bash
cd /home/fg/library-platform/frontend
cp .env.example .env
npm install
npm run build
```

Set in `/home/fg/library-platform/frontend/.env`:

```env
NEXT_PUBLIC_API_URL=https://library.digigalaxy.cloud/api/v1
NEXT_PUBLIC_APP_NAME=Maktaba Ilmiah
```

## 5. systemd Services

Copy the provided units:

```bash
sudo cp /home/fg/library-platform/infra/systemd/library-backend.service /etc/systemd/system/
sudo cp /home/fg/library-platform/infra/systemd/library-celery.service /etc/systemd/system/
sudo cp /home/fg/library-platform/infra/systemd/library-celerybeat.service /etc/systemd/system/
sudo cp /home/fg/library-platform/infra/systemd/library-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable library-backend library-celery library-celerybeat library-frontend
sudo systemctl restart library-backend library-celery library-celerybeat library-frontend
```

Useful checks:

```bash
sudo systemctl status library-backend
sudo systemctl status library-celery
sudo systemctl status library-celerybeat
sudo systemctl status library-frontend
```

## 6. Nginx

Install the site config without disturbing the existing bench config. Use a dedicated server block for `library.digigalaxy.cloud` only.

```bash
sudo cp /home/fg/library-platform/infra/nginx/library-platform.conf /etc/nginx/sites-available/library-platform.conf
sudo ln -sf /etc/nginx/sites-available/library-platform.conf /etc/nginx/sites-enabled/library-platform.conf
sudo nginx -t
sudo systemctl reload nginx
```

The provided template:

- proxies `/` to Next.js on `127.0.0.1:3000`
- proxies `/api/` and `/admin/` to Django on `127.0.0.1:8001`
- serves `/static/` and `/media/` from `/home/fg/library-platform/backend`
- allows larger PDF uploads

## 7. SSL

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d library.digigalaxy.cloud
```

## 8. Local Run Commands

Backend:

```bash
cd /home/fg/library-platform/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001
```

Celery worker:

```bash
cd /home/fg/library-platform/backend
source venv/bin/activate
celery -A config worker -l info
```

Frontend:

```bash
cd /home/fg/library-platform/frontend
npm run dev
```

## 9. Logs

```bash
sudo journalctl -u library-backend -f
sudo journalctl -u library-celery -f
sudo journalctl -u library-celerybeat -f
sudo journalctl -u library-frontend -f
```

## 10. Deployment Notes

- keep this app outside bench
- do not edit Frappe’s Nginx server blocks to host this app indirectly
- if Nginx already serves other domains, only add the dedicated `library.digigalaxy.cloud` block
- rebuild the frontend after UI changes:

```bash
cd /home/fg/library-platform/frontend
npm run build
sudo systemctl restart library-frontend
```

- after backend code or dependency changes:

```bash
cd /home/fg/library-platform/backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart library-backend library-celery library-celerybeat
```
