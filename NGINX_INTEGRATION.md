# 🔗 Nginx Integration Guide for Library Platform

## Current Setup (As Per Your System)

Your system has:
- ✅ Nginx running on port 80
- ✅ Other apps already deployed
- ✅ Library Platform needs to be added to this setup

---

## How Nginx Routes Work

When user visits `http://library.digigalaxy.cloud`:

```
HTTP Request (Port 80)
    ↓
Nginx listens on port 80
    ↓
Nginx checks URL path:
  ├─ "/" → Routes to Frontend (localhost:3000)
  ├─ "/api/v1/*" → Routes to Backend (localhost:8001)
  ├─ "/admin/*" → Routes to Backend Admin (localhost:8001)
  └─ "/media/*" → Serves from disk
    ↓
Response sent back to user
```

---

## Current Nginx Config Structure

Your nginx config file is at:
```
/home/fg/library-platform/infra/nginx/library.conf
```

### Configuration Overview

```nginx
# Upstream services (where to forward requests)
upstream library_frontend {
    server localhost:3000;        # Next.js frontend
}

upstream library_backend {
    server localhost:8001;        # Django backend
}

# HTTP to HTTPS redirect (if using SSL)
server {
    listen 80;
    return 301 https://...
}

# SSL/HTTPS server (443)
server {
    listen 443 ssl http2;
    
    # Routes
    location ~ ^/api/       → Backend API
    location ~ ^/admin/     → Backend Admin
    location /media/        → Disk storage
    location /_next/static/ → Frontend static
    location /              → Frontend (default)
}
```

---

## Installation Steps

### Step 1: Copy Config to Nginx

```bash
# Copy the library config to nginx sites-available
sudo cp /home/fg/library-platform/infra/nginx/library.conf \
    /etc/nginx/sites-available/library.conf

# Verify permissions
ls -la /etc/nginx/sites-available/library.conf
```

### Step 2: Enable the Site

```bash
# Create symlink in sites-enabled
sudo ln -s /etc/nginx/sites-available/library.conf \
    /etc/nginx/sites-enabled/library.conf

# Verify
ls -la /etc/nginx/sites-enabled/library.conf
```

### Step 3: Test Configuration

```bash
# ALWAYS test before reloading!
sudo nginx -t

# Expected output:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration will be successful
```

### Step 4: Reload Nginx

```bash
# Graceful reload (doesn't drop connections)
sudo systemctl reload nginx

# Verify it's running
sudo systemctl status nginx

# Should show: ● nginx.service - A high performance web server
#             Loaded: loaded (/lib/systemd/nginx.service...)
#             Active: active (running)
```

---

## Configuration Details

### Route Definitions

#### 1. Frontend (Default Route)
```nginx
location / {
    proxy_pass http://library_frontend;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
**Effect**: All requests to `/` go to Next.js frontend

#### 2. API Backend
```nginx
location ~ ^/api/ {
    proxy_pass http://library_backend;
    proxy_http_version 1.1;
    proxy_cache_bypass $http_upgrade;
}
```
**Effect**: All requests to `/api/v1/*` go to Django backend

#### 3. Admin Panel
```nginx
location ~ ^/admin/ {
    proxy_pass http://library_backend;
}
```
**Effect**: All requests to `/admin/*` go to Django admin

#### 4. Static Files (Frontend Assets)
```nginx
location /_next/static/ {
    proxy_pass http://library_frontend;
    expires 365d;
    add_header Cache-Control "public, immutable";
}
```
**Effect**: Next.js CSS/JS files cached for 1 year

#### 5. Media Upload Storage
```nginx
location /media/ {
    alias /home/library-user/library-platform/backend/media/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```
**Effect**: Uploaded books/PDFs served from disk

---

## Setup After Nginx Configuration

### Step 1: Setup Backend & Frontend

```bash
cd /home/fg/library-platform
bash setup-live.sh
```

This will:
- ✅ Create Python venv
- ✅ Install all dependencies
- ✅ Run migrations
- ✅ Build frontend
- ✅ Create .env files

### Step 2: Update Environment Variables

```bash
# Edit backend environment
nano backend/.env

# Key values to update:
DEBUG=False
DJANGO_SECRET_KEY=your-long-random-key-here
ALLOWED_HOSTS=library.digigalaxy.cloud,localhost
SECURE_SSL_REDIRECT=True
```

### Step 3: Start Services

```bash
cd /home/fg/library-platform
bash start-live.sh
```

Services will start on:
- Frontend: `localhost:3000`
- Backend: `localhost:8001`

### Step 4: Verify Through Nginx

```bash
# Frontend (should show login page)
curl http://localhost/

# Backend API (should show API response)
curl http://localhost/api/v1/

# Admin panel (should redirect to login)
curl http://localhost/admin/
```

---

## Testing Your Setup

### Test 1: Frontend is Accessible
```bash
curl -I http://localhost/
# Should return: HTTP/1.1 200 OK
```

### Test 2: Backend API is Accessible
```bash
curl -I http://localhost/api/v1/
# Should return: HTTP/1.1 200 OK
```

### Test 3: All Services Running
```bash
bash /home/fg/library-platform/status-live.sh

# Output should show:
# ✓ Backend (gunicorn) - Running on port 8001
# ✓ Frontend (Next.js) - Running on port 3000
# ✓ Nginx - Running (port 80/443)
```

### Test 4: View Nginx Logs
```bash
# Check for errors
sudo tail -f /var/log/nginx/library_error.log

# Check access log
sudo tail -f /var/log/nginx/library_access.log
```

---

## Integration with Existing Apps

If you have other apps already deployed:

### Keep Them Running

```bash
# Check what's currently running on nginx
sudo nginx -T | grep "server_name"

# Your existing apps should remain unchanged
```

### Add Library Platform Alongside

The config uses:
- Domain: `library.digigalaxy.cloud`
- Paths: `/api`, `/admin`, `/_next`, `/media`

This means you can have other apps on different domains/ports without conflict.

### Example Multi-App Setup

```
Nginx (Port 80)
├─ library.digigalaxy.cloud/
│  ├─ / → Frontend (3000)
│  ├─ /api → Backend (8001)
│  └─ /admin → Backend (8001)
├─ crm.digigalaxy.cloud/
│  └─ / → Other app (different port)
└─ shop.digigalaxy.cloud/
   └─ / → Another app (different port)
```

---

## Troubleshooting

### Nginx Won't Start

```bash
# Check syntax
sudo nginx -t

# Get detailed error
sudo nginx -T 2>&1 | head -20

# Check if port 80 is in use
sudo lsof -i :80

# Check systemd errors
sudo journalctl -u nginx -n 50
```

### Routes Not Working

```bash
# Tail error log while accessing
sudo tail -f /var/log/nginx/library_error.log
# In another terminal: curl http://localhost/api/v1/

# Check config was loaded
sudo nginx -T | grep "location"

# Restart nginx
sudo systemctl restart nginx
```

### Services Behind Nginx Not Responding

```bash
# Check backend is running on 8001
telnet localhost 8001

# Check frontend is running on 3000
telnet localhost 3000

# Restart services
bash /home/fg/library-platform/restart-live.sh
```

### 502 Bad Gateway Error

```bash
# Check services are running
bash /home/fg/library-platform/status-live.sh

# If not running, start them
bash /home/fg/library-platform/start-live.sh

# Check backend logs
tail -f /home/fg/library-platform/backend/logs/gunicorn_error.log
```

---

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d library.digigalaxy.cloud

# Update nginx config paths
sudo nano /etc/nginx/sites-available/library.conf

# Add these lines:
ssl_certificate /etc/letsencrypt/live/library.digigalaxy.cloud/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/library.digigalaxy.cloud/privkey.pem;

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### Auto-Renewal

```bash
# Enable auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Test renewal (dry run)
sudo certbot renew --dry-run
```

---

## Performance Optimization

### Enable Caching

Already configured in `library.conf`:
```nginx
# Static cache for 1 year
expires 365d;
add_header Cache-Control "public, immutable";

# Gzip compression
gzip on;
gzip_comp_level 6;
```

### Monitor Performance

```bash
# Watch nginx in real-time
watch 'netstat -an | grep ESTABLISHED | wc -l'

# Check active connections
sudo netstat -tlnp | grep nginx

# View bandwidth usage
sudo nethogs
```

---

## Maintenance Commands

### View Current Config
```bash
sudo cat /etc/nginx/sites-available/library.conf
```

### Edit Config
```bash
sudo nano /etc/nginx/sites-available/library.conf

# After editing:
sudo nginx -t
sudo systemctl reload nginx
```

### Disable Site Temporarily
```bash
sudo rm /etc/nginx/sites-enabled/library.conf
sudo systemctl reload nginx
```

### Re-enable Site
```bash
sudo ln -s /etc/nginx/sites-available/library.conf \
    /etc/nginx/sites-enabled/library.conf
sudo systemctl reload nginx
```

### View Active Sites
```bash
ls -la /etc/nginx/sites-enabled/
```

---

## Configuration Checklist

- [ ] Nginx config file copied to `/etc/nginx/sites-available/`
- [ ] Config symlinked to `/etc/nginx/sites-enabled/`
- [ ] Config tested with `sudo nginx -t`
- [ ] Nginx reloaded: `sudo systemctl reload nginx`
- [ ] Backend service running on port 8001
- [ ] Frontend service running on port 3000
- [ ] Frontend accessible at http://localhost/
- [ ] Backend API accessible at http://localhost/api/v1/
- [ ] Admin panel accessible at http://localhost/admin/
- [ ] SSL certificate installed (if using HTTPS)
- [ ] Error logs checked: `sudo tail -f /var/log/nginx/error.log`
- [ ] Access logs verified: `sudo tail -f /var/log/nginx/library_access.log`

---

## Quick Reference

```bash
# Copy config
sudo cp /home/fg/library-platform/infra/nginx/library.conf /etc/nginx/sites-available/

# Enable site
sudo ln -s /etc/nginx/sites-available/library.conf /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Setup services
cd /home/fg/library-platform && bash setup-live.sh

# Start services
bash start-live.sh

# Check status
bash status-live.sh

# View logs
sudo tail -f /var/log/nginx/error.log
tail -f backend/logs/gunicorn_error.log
```

---

## Support

For detailed deployment guide, see: `LIVE_DEPLOYMENT_SETUP.md`
For quick start, see: `QUICK_START.sh`
For script reference, see: `SETUP_SCRIPTS_GUIDE.md`
