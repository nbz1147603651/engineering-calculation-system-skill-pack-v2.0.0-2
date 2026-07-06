#!/usr/bin/env bash
set -Eeuo pipefail

log() {
  printf '[ecs-homepage] %s\n' "$*"
}

fail() {
  printf '[ecs-homepage] ERROR: %s\n' "$*" >&2
  exit 1
}

is_truthy() {
  case "${1:-}" in
    1|true|TRUE|yes|YES|on|ON) return 0 ;;
    *) return 1 ;;
  esac
}

escape_sed_replacement() {
  printf '%s' "$1" | sed -e 's/[\/&]/\\&/g'
}

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
package_root="$(cd -- "$script_dir/../.." && pwd)"
site_source="$package_root/site"
template_path="$package_root/deploy/nginx/ecs-homepage-linux.conf.template"
version_file="$package_root/VERSION"

[[ -d "$site_source" ]] || fail "Missing site directory: $site_source"
[[ -f "$site_source/index.html" ]] || fail "Missing site/index.html"
[[ -f "$site_source/home/index.html" ]] || fail "Missing site/home/index.html"
[[ -f "$site_source/version.json" ]] || fail "Missing site/version.json"
[[ -f "$template_path" ]] || fail "Missing Nginx template: $template_path"
[[ -f "$version_file" ]] || fail "Missing VERSION file: $version_file"

version="$(tr -d '[:space:]' < "$version_file")"
gui_installer_name="engineering-calc-system-installer-v${version}.exe"
download_file_path="data/$gui_installer_name"
download_url_path="downloads/$gui_installer_name"
[[ -f "$site_source/$download_file_path" ]] || fail "Missing GUI installer download: $site_source/$download_file_path"

install_root="${ECS_HOMEPAGE_INSTALL_ROOT:-/opt/ecs-homepage}"
site_root="${ECS_HOMEPAGE_SITE_ROOT:-$install_root/site}"
nginx_conf="${ECS_HOMEPAGE_NGINX_CONF:-/etc/nginx/conf.d/ecs-homepage.conf}"
server_name="${ECS_HOMEPAGE_SERVER_NAME:-_}"
skip_nginx="${ECS_HOMEPAGE_SKIP_NGINX:-0}"
reload_nginx="${ECS_HOMEPAGE_RELOAD_NGINX:-1}"

[[ -n "$site_root" && "$site_root" != "/" ]] || fail "Refusing unsafe ECS_HOMEPAGE_SITE_ROOT='$site_root'"

if [[ "$site_root" == /opt/* || "$nginx_conf" == /etc/* ]]; then
  [[ "${EUID:-$(id -u)}" -eq 0 ]] || fail "Run as root/sudo, or set ECS_HOMEPAGE_SITE_ROOT and ECS_HOMEPAGE_NGINX_CONF to writable paths."
fi

log "package root: $package_root"
log "install root: $install_root"
log "site root: $site_root"

install -d "$site_root"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$site_source"/ "$site_root"/
else
  find "$site_root" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  cp -a "$site_source"/. "$site_root"/
fi
log "site files installed"

if is_truthy "$skip_nginx"; then
  log "ECS_HOMEPAGE_SKIP_NGINX is set; skipping Nginx config and reload"
  exit 0
fi

command -v nginx >/dev/null 2>&1 || fail "nginx is not installed. Install nginx or set ECS_HOMEPAGE_SKIP_NGINX=1."

install -d "$(dirname "$nginx_conf")"
escaped_site_root="$(escape_sed_replacement "$site_root")"
escaped_server_name="$(escape_sed_replacement "$server_name")"
sed \
  -e "s/__ECS_HOMEPAGE_SITE_ROOT__/$escaped_site_root/g" \
  -e "s/__ECS_HOMEPAGE_SERVER_NAME__/$escaped_server_name/g" \
  "$template_path" > "$nginx_conf"
log "nginx config written: $nginx_conf"

nginx -t

if is_truthy "$reload_nginx"; then
  if command -v systemctl >/dev/null 2>&1; then
    if systemctl is-active --quiet nginx; then
      systemctl reload nginx
    else
      systemctl start nginx
    fi
  else
    nginx -s reload || nginx
  fi
  log "nginx started or reloaded"
else
  log "ECS_HOMEPAGE_RELOAD_NGINX=0; not reloading nginx"
fi

if command -v curl >/dev/null 2>&1; then
  curl -fsSI http://127.0.0.1/ >/dev/null
  curl -fsSI http://127.0.0.1/home/ >/dev/null
  curl -fsSI "http://127.0.0.1/$download_url_path" >/dev/null
  curl -fsS http://127.0.0.1/healthz >/dev/null
  curl -fsS http://127.0.0.1/version.json >/dev/null
  log "local health checks passed"
else
  log "curl not installed; skipped HTTP health checks"
fi
