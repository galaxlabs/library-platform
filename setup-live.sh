#!/bin/bash

##############################################################################
# Library Platform - Live Production Setup Script
# 
# This script sets up the library-platform for live deployment
# - Backend runs on localhost:8001
# - Frontend runs on localhost:3000
# - Nginx (port 80/443) reverse proxies both
# 
# Usage: bash setup-live.sh
##############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}=========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

print_header "Library Platform - Live Setup"

# Check if running as root or can sudo
if [[ $EUID -ne 0 ]]; then
    print_warning "This script needs some sudo commands. Password may be required."
fi

# ============================================================================
# 1. Check Prerequisites
# ============================================================================

print_header "Step 1: Checking Prerequisites"

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 is required but not installed."
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python3 found: $PYTHON_VERSION"

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed."
    exit 1
fi
NODE_VERSION=$(node --version)
print_success "Node.js found: $NODE_VERSION"

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is required but not installed."
    exit 1
fi
NPM_VERSION=$(npm --version)
print_success "npm found: $NPM_VERSION"

# Check Git
if ! command -v git &> /dev/null; then
    print_warning "Git not found (optional but recommended)"
else
    print_success "Git found"
fi

# ============================================================================
# 2. Backend Setup
# ============================================================================

print_header "Step 2: Setting up Backend"

if [ ! -d "backend" ]; then
    print_error "Backend directory not found at $PROJECT_DIR/backend"
    exit 1
fi

cd "$PROJECT_DIR/backend"
print_info "Working directory: $(pwd)"

# Create virtual environment
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    print_info "Installing Python dependencies (this may take a few minutes)..."
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_error "requirements.txt not found in backend directory"
    exit 1
fi

# Create .env file from template
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_success ".env file created"
        print_warning "IMPORTANT: Please edit .env file with your actual values:"
        print_warning "  - DB_PASSWORD (use strong password)"
        print_warning "  - DJANGO_SECRET_KEY"
        print_warning "  - REDIS_URL"
        print_warning "  - EMAIL credentials (if needed)"
        print_warning "  - AI provider keys (if needed)"
    else
        print_error ".env.example not found"
        exit 1
    fi
else
    print_info ".env file already exists (skipping)"
fi

# Run database migrations
print_info "Running database migrations..."
python manage.py migrate --noinput
print_success "Database migrations completed"

# Collect static files
print_info "Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1
print_success "Static files collected"

# Create superuser if doesn't exist (non-interactive)
print_info "Setting up admin user..."
python manage.py shell << 'EOF' > /dev/null 2>&1
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@library.local', 'admin123')
    print("Superuser 'admin' created (password: admin123)")
else:
    print("Superuser already exists")
EOF
print_success "Admin user ready (username: admin, password: admin123)"

print_success "Backend setup completed"

# ============================================================================
# 3. Frontend Setup
# ============================================================================

print_header "Step 3: Setting up Frontend"

cd "$PROJECT_DIR/frontend"
print_info "Working directory: $(pwd)"

# Install npm dependencies
if [ -f "package.json" ]; then
    print_info "Installing frontend dependencies (this may take a few minutes)..."
    npm install --legacy-peer-deps > /dev/null 2>&1
    print_success "Frontend dependencies installed"
else
    print_error "package.json not found in frontend directory"
    exit 1
fi

# Create .env.production file
if [ ! -f ".env.production" ]; then
    if [ -f ".env.example" ]; then
        print_info "Creating .env.production file..."
        cp .env.example .env.production
        print_success ".env.production created"
    else
        print_info "Creating .env.production with defaults..."
        cat > .env.production << 'ENVEOF'
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_APP_NAME="مكتبة النحو"
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_LANGUAGES=ar,en
NEXT_PUBLIC_DEFAULT_LANGUAGE=ar
ENVEOF
        print_success ".env.production created"
    fi
else
    print_info ".env.production already exists (skipping)"
fi

# Build frontend for production
print_info "Building frontend for production (this may take a few minutes)..."
npm run build > /dev/null 2>&1
print_success "Frontend build completed"

print_success "Frontend setup completed"

# ============================================================================
# 4. Nginx Configuration
# ============================================================================

print_header "Step 4: Preparing Nginx Configuration"

if [ -f "infra/nginx/library.conf" ]; then
    print_info "Nginx configuration found at infra/nginx/library.conf"
    print_info "To activate it, run:"
    echo -e "  ${YELLOW}sudo cp $PROJECT_DIR/infra/nginx/library.conf /etc/nginx/sites-available/${NC}"
    echo -e "  ${YELLOW}sudo ln -s /etc/nginx/sites-available/library.conf /etc/nginx/sites-enabled/${NC}"
    echo -e "  ${YELLOW}sudo nginx -t${NC}"
    echo -e "  ${YELLOW}sudo systemctl restart nginx${NC}"
else
    print_warning "Nginx configuration not found"
fi

# ============================================================================
# 5. Create Service Management Scripts
# ============================================================================

print_header "Step 5: Creating Service Management Scripts"

cd "$PROJECT_DIR"

# Create start script
cat > start-live.sh << 'SCRIPTEOF'
#!/bin/bash

# Start all services for live deployment

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "Starting Library Platform services..."

# Start Backend
echo "Starting backend on port 8001..."
cd "$BACKEND_DIR"
source venv/bin/activate
nohup gunicorn config.wsgi:application --bind 127.0.0.1:8001 --workers 4 --timeout 120 \
    --access-logfile logs/gunicorn_access.log \
    --error-logfile logs/gunicorn_error.log \
    --daemon > /dev/null 2>&1
echo "Backend started (PID: check logs/gunicorn_error.log)"

# Start Frontend
echo "Starting frontend on port 3000..."
cd "$FRONTEND_DIR"
nohup npm start > logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "Services are starting..."
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8001/api/v1"
echo "Nginx:     http://localhost (port 80)"
echo ""
echo "Check logs:"
echo "  Backend:  tail -f $BACKEND_DIR/logs/gunicorn_error.log"
echo "  Frontend: tail -f $FRONTEND_DIR/logs/frontend.log"
echo ""
SCRIPTEOF

chmod +x start-live.sh
print_success "Created start-live.sh"

# Create stop script
cat > stop-live.sh << 'SCRIPTEOF'
#!/bin/bash

echo "Stopping Library Platform services..."

# Stop Frontend
echo "Stopping frontend..."
pkill -f "npm start" || true
sleep 2

# Stop Backend
echo "Stopping backend..."
pkill -f "gunicorn config.wsgi" || true
sleep 2

echo "All services stopped"
SCRIPTEOF

chmod +x stop-live.sh
print_success "Created stop-live.sh"

# Create restart script
cat > restart-live.sh << 'SCRIPTEOF'
#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

$PROJECT_DIR/stop-live.sh
sleep 3
$PROJECT_DIR/start-live.sh
SCRIPTEOF

chmod +x restart-live.sh
print_success "Created restart-live.sh"

# Create status script
cat > status-live.sh << 'SCRIPTEOF'
#!/bin/bash

echo "Checking services status..."
echo ""

# Check Backend
if pgrep -f "gunicorn config.wsgi" > /dev/null; then
    echo "✓ Backend (gunicorn) - Running on port 8001"
else
    echo "✗ Backend (gunicorn) - Not running"
fi

# Check Frontend
if pgrep -f "npm start" > /dev/null; then
    echo "✓ Frontend (Next.js) - Running on port 3000"
else
    echo "✗ Frontend (Next.js) - Not running"
fi

# Check Nginx
if systemctl is-active --quiet nginx; then
    echo "✓ Nginx - Running (port 80/443)"
else
    echo "✗ Nginx - Not running"
fi

echo ""
echo "Port Status:"
netstat -tlnp 2>/dev/null | grep -E ':(80|3000|8001)' || echo "netstat not available, trying lsof..."
lsof -i -P -n 2>/dev/null | grep -E 'LISTEN.*:(80|3000|8001)' || echo "lsof not available"
SCRIPTEOF

chmod +x status-live.sh
print_success "Created status-live.sh"

# ============================================================================
# 6. Create Environment Info
# ============================================================================

print_header "Step 6: Creating Configuration Info"

cat > DEPLOYMENT_INFO.md << 'DEPLOYEOF'
# Library Platform - Live Deployment Information

## Services & Ports

- **Frontend (Next.js)**: http://localhost:3000
- **Backend (Django + Gunicorn)**: http://localhost:8001
- **Nginx Reverse Proxy**: http://localhost (port 80)
- **Database**: PostgreSQL on default port 5432
- **Cache**: Redis on default port 6379

## Service Management

### Quick Start
```bash
bash start-live.sh
```

### Quick Stop
```bash
bash stop-live.sh
```

### Quick Restart
```bash
bash restart-live.sh
```

### Check Status
```bash
bash status-live.sh
```

## Logs

### Backend Logs
```bash
tail -f backend/logs/gunicorn_error.log
tail -f backend/logs/gunicorn_access.log
```

### Frontend Logs
```bash
tail -f frontend/logs/frontend.log
```

### Nginx Logs
```bash
sudo tail -f /var/log/nginx/library_access.log
sudo tail -f /var/log/nginx/library_error.log
```

## Useful URLs

- **Frontend**: http://localhost:3000
- **Admin Panel**: http://localhost/admin (via Nginx)
- **API Docs**: http://localhost/api/v1 (via Nginx)

## Initial Credentials

- **Admin Username**: admin
- **Admin Password**: admin123

**IMPORTANT**: Change these credentials immediately in production!

## Frontend First Setup

The system is configured to serve the frontend by default:
1. Requests to `/` (root) are forwarded to frontend (port 3000)
2. Requests to `/api/*` are forwarded to backend (port 8001)
3. Requests to `/admin/*` are forwarded to backend admin panel

## Production Checklist

- [ ] Update .env file with production secrets
- [ ] Change admin password
- [ ] Configure email settings
- [ ] Set up SSL/TLS certificates (if using HTTPS)
- [ ] Configure Redis password
- [ ] Set database backup strategy
- [ ] Enable monitoring and logging
- [ ] Set up error alerting
- [ ] Test backup restoration
- [ ] Document runbook

## Troubleshooting

### Backend won't start
```bash
cd backend
source venv/bin/activate
python manage.py check
```

### Frontend won't build
```bash
cd frontend
npm install --legacy-peer-deps
npm run build
```

### Port already in use
```bash
# Find what's using port 8001
lsof -i :8001

# Find what's using port 3000
lsof -i :3000

# Kill process (dangerous, check carefully first)
kill -9 <PID>
```

### Database connection error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U <DB_USER> -d <DB_NAME> -c "SELECT 1;"
```

## Stack Information

- **Backend**: Django 5.0 + Django REST Framework
- **Frontend**: Next.js 14 (App Router) + React 18
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **API Server**: Gunicorn
- **Reverse Proxy**: Nginx
- **Language Support**: Arabic (RTL) + English (LTR)

DEPLOYEOF

print_success "Created DEPLOYMENT_INFO.md"

# ============================================================================
# 7. Create logs directory
# ============================================================================

print_header "Step 7: Setting up Directories"

mkdir -p "$PROJECT_DIR/backend/logs"
mkdir -p "$PROJECT_DIR/frontend/logs"
print_success "Created logs directories"

# ============================================================================
# 8. Summary and Next Steps
# ============================================================================

print_header "🎉 Setup Complete!"

echo -e "${GREEN}What's been done:${NC}"
echo "  ✓ Python virtual environment created"
echo "  ✓ Backend dependencies installed"
echo "  ✓ Frontend dependencies installed"
echo "  ✓ Database migrations run"
echo "  ✓ Frontend built for production"
echo "  ✓ Admin user created"
echo "  ✓ Service scripts created"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Update Configuration Files:"
echo "   • Edit backend/.env with production values"
echo "     - DB_PASSWORD, DJANGO_SECRET_KEY, REDIS_URL, etc."
echo ""
echo "2. Configure Nginx (if not already done):"
echo "   sudo cp infra/nginx/library.conf /etc/nginx/sites-available/"
echo "   sudo ln -s /etc/nginx/sites-available/library.conf /etc/nginx/sites-enabled/"
echo "   sudo nginx -t"
echo "   sudo systemctl restart nginx"
echo ""
echo "3. Install Gunicorn (for backend):"
echo "   cd backend && source venv/bin/activate"
echo "   pip install gunicorn"
echo ""
echo "4. Start Services:"
echo "   bash start-live.sh"
echo ""
echo "5. Check Status:"
echo "   bash status-live.sh"
echo ""
echo "6. Access Application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8001"
echo "   Via Nginx: http://localhost (or your domain)"
echo ""

echo -e "${YELLOW}Default Admin Credentials:${NC}"
echo "   Username: admin"
echo "   Password: admin123"
echo "   CHANGE THESE IMMEDIATELY IN PRODUCTION!"
echo ""

echo -e "${BLUE}For more information, see: DEPLOYMENT_INFO.md${NC}"
echo ""

print_success "Setup script completed successfully!"
