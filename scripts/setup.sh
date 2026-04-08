#!/bin/bash

# Library Platform Setup Script

set -e

echo "========================================="
echo "Library Platform Setup"
echo "========================================="

# Backend Setup
echo "Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file - please update with your settings"
fi

# Run migrations
python manage.py migrate

echo "Backend setup complete!"

# Frontend Setup
echo ""
echo "Setting up Frontend..."
cd ../frontend

# Install dependencies
npm install

# Create .env from template
if [ ! -f ".env.local" ]; then
    cp .env.example .env.local
fi

echo "Frontend setup complete!"

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To start development:"
echo "  Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "  Frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up"
echo ""
