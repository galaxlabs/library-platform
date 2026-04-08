#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_PY="$BACKEND_DIR/venv/bin/python"
VENV_GUNICORN="$BACKEND_DIR/venv/bin/gunicorn"

if [[ ! -x "$VENV_PY" || ! -x "$VENV_GUNICORN" ]]; then
  echo "Backend virtualenv is missing required executables in $BACKEND_DIR/venv" >&2
  exit 1
fi

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"
export PYTHONPATH="$BACKEND_DIR"
export STATIC_ROOT="${STATIC_ROOT:-$BACKEND_DIR/staticfiles_host}"

cd "$BACKEND_DIR"

"$VENV_PY" manage.py migrate --noinput
"$VENV_PY" manage.py collectstatic --noinput
exec "$VENV_GUNICORN" config.wsgi:application \
  --bind "${BIND_ADDRESS:-127.0.0.1:8001}" \
  --workers "${GUNICORN_WORKERS:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-120}"
