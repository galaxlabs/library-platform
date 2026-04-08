#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

cd "$BACKEND_DIR"
source venv/bin/activate

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"
export STATIC_ROOT="${STATIC_ROOT:-$BACKEND_DIR/staticfiles_host}"

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec python manage.py runserver 127.0.0.1:8001
