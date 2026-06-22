#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="$ROOT_DIR/deploy"
RAW_ENV_FILE="${ECS_ENV_FILE:-$DEPLOY_DIR/.env}"
case "$RAW_ENV_FILE" in
  /*) ENV_FILE="$RAW_ENV_FILE" ;;
  *) ENV_FILE="$(pwd)/$RAW_ENV_FILE" ;;
esac
MODE="${1:-auto}"

log() {
  printf '[engineering-calc] %s\n' "$*"
}

warn() {
  printf '[engineering-calc][warn] %s\n' "$*" >&2
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || {
    printf '[engineering-calc][error] missing command: %s\n' "$1" >&2
    exit 1
  }
}

ensure_env() {
  if [ ! -f "$ENV_FILE" ]; then
    mkdir -p "$(dirname "$ENV_FILE")"
    cp "$DEPLOY_DIR/env.example" "$ENV_FILE"
    warn "Created $ENV_FILE from env.example. Edit secrets before production use."
  fi

  # shellcheck disable=SC1090
  set -a
  . "$ENV_FILE"
  set +a

  if [ "${SECRET_KEY:-}" = "change-me-on-server" ]; then
    warn "SECRET_KEY still uses the example value."
  fi
  if [ "${ADMIN_REVIEW_PASSWORD:-}" = "change-this-admin-review-password" ]; then
    warn "ADMIN_REVIEW_PASSWORD still uses the example value."
  fi
  if [ "${ADMIN_REVIEW_TOKEN:-}" = "change-this-admin-review-token" ]; then
    warn "ADMIN_REVIEW_TOKEN still uses the example value."
  fi
}

compose_available() {
  command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1
}

check_marimo_host() {
  if python3 - <<'PY' >/dev/null 2>&1
import importlib.util
raise SystemExit(0 if importlib.util.find_spec("marimo") else 1)
PY
  then
    log "Marimo is available on the host."
  else
    warn "Marimo is not available on the host. The Flask admin page will show the install prompt."
  fi
}

deploy_compose() {
  require_command docker
  log "Starting Docker Compose services with $ENV_FILE"
  (
    cd "$DEPLOY_DIR"
    ECS_ENV_FILE="$ENV_FILE" docker compose up -d --build
  )
  log "Docker Compose services started."
}

install_local_python_deps() {
  require_command python3
  if [ ! -d "$ROOT_DIR/.venv" ]; then
    python3 -m venv "$ROOT_DIR/.venv"
  fi
  "$ROOT_DIR/.venv/bin/python" -m pip install --upgrade pip
  "$ROOT_DIR/.venv/bin/python" -m pip install -e "$ROOT_DIR[web,report]" || \
    "$ROOT_DIR/.venv/bin/python" -m pip install "flask>=3.0" "gunicorn>=21.2" "jinja2>=3.1"
}

start_local_service() {
  install_local_python_deps
  mkdir -p "$ROOT_DIR/outputs/logs"
  export PYTHONPATH="$ROOT_DIR/src"
  log "Starting gunicorn on ${APP_HOST:-0.0.0.0}:${APP_PORT:-5000}"
  nohup "$ROOT_DIR/.venv/bin/gunicorn" "webapp.app:create_app()" \
    --bind "${APP_HOST:-0.0.0.0}:${APP_PORT:-5000}" \
    --workers "${GUNICORN_WORKERS:-2}" \
    > "$ROOT_DIR/outputs/logs/web.log" 2>&1 &
  echo "$!" > "$ROOT_DIR/outputs/logs/web.pid"

  if "$ROOT_DIR/.venv/bin/python" - <<'PY' >/dev/null 2>&1
import importlib.util
raise SystemExit(0 if importlib.util.find_spec("marimo") else 1)
PY
  then
    if [ -n "${ADMIN_REVIEW_TOKEN:-}" ]; then
      # Equivalent commands:
      # marimo run apps/review/calculation_review.py --token --token-password "$ADMIN_REVIEW_TOKEN"
      # marimo run apps/review/admin_formula_review.py --token --token-password "$ADMIN_REVIEW_TOKEN"
      log "Starting Marimo calculation review and formula admin services."
      nohup "$ROOT_DIR/.venv/bin/marimo" run apps/review/calculation_review.py \
        --host 127.0.0.1 \
        --port "${MARIMO_PORT:-2718}" \
        --base-url "${MARIMO_BASE_URL:-/admin/review}" \
        --headless --token --token-password "$ADMIN_REVIEW_TOKEN" \
        > "$ROOT_DIR/outputs/logs/marimo-review.log" 2>&1 &
      echo "$!" > "$ROOT_DIR/outputs/logs/marimo-review.pid"

      nohup "$ROOT_DIR/.venv/bin/marimo" run apps/review/admin_formula_review.py \
        --host 127.0.0.1 \
        --port "${FORMULA_ADMIN_PORT:-2719}" \
        --base-url "${FORMULA_ADMIN_BASE_URL:-/admin/formulas}" \
        --headless --token --token-password "$ADMIN_REVIEW_TOKEN" \
        > "$ROOT_DIR/outputs/logs/marimo-formula-admin.log" 2>&1 &
      echo "$!" > "$ROOT_DIR/outputs/logs/marimo-formula-admin.pid"
    else
      warn "ADMIN_REVIEW_TOKEN is not set; Marimo services were not started."
    fi
  else
    warn "Marimo is not installed in the local venv; admin page will show the install prompt."
  fi
}

health_check() {
  local url="http://127.0.0.1:${APP_PORT:-5000}/health"
  if command -v curl >/dev/null 2>&1; then
    for _ in 1 2 3 4 5; do
      if curl -fsS "$url" >/dev/null; then
        log "Health check passed: $url"
        return 0
      fi
      sleep 2
    done
    warn "Health check did not pass yet: $url"
  else
    warn "curl is missing; skipped health check."
  fi
}

main() {
  ensure_env
  check_marimo_host

  case "$MODE" in
    auto)
      if compose_available; then
        deploy_compose
      else
        start_local_service
      fi
      ;;
    compose)
      deploy_compose
      ;;
    local)
      start_local_service
      ;;
    *)
      printf 'Usage: %s [auto|compose|local]\n' "$0" >&2
      exit 2
      ;;
  esac

  health_check
  log "Main app: http://127.0.0.1:${APP_PORT:-5000}/"
  log "Admin shell: http://127.0.0.1:${APP_PORT:-5000}/admin/"
  log "Formula admin proxy path: ${FORMULA_ADMIN_BASE_URL:-/admin/formulas}/"
}

main "$@"
