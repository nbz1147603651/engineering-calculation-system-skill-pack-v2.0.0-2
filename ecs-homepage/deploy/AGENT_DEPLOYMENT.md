# Agent Deployment Runbook

Use this when a cloud-side coding agent receives the ECS homepage Linux web
package and needs to deploy it without asking follow-up questions.

## Success Criteria

- Static files are installed under `/opt/ecs-homepage/site` unless an override is supplied.
- Nginx serves `/`, `/home/`, `/healthz`, and `/version.json`.
- `/version.json` reports the same version as `deployment-manifest.json`.
- `nginx -t` passes before reload.

## Default Autonomous Flow

```bash
sha256sum -c ecs-homepage-<version>-linux-web.zip.sha256
unzip ecs-homepage-<version>-linux-web.zip
cd ecs-homepage-<version>-linux-web
sudo bash deploy/linux/deploy.sh
```

For a domain-backed host:

```bash
sudo ECS_HOMEPAGE_SERVER_NAME=example.com bash deploy/linux/deploy.sh
```

## Environment Overrides

- `ECS_HOMEPAGE_INSTALL_ROOT`: parent install directory. Default: `/opt/ecs-homepage`.
- `ECS_HOMEPAGE_SITE_ROOT`: exact static site root. Default: `$ECS_HOMEPAGE_INSTALL_ROOT/site`.
- `ECS_HOMEPAGE_NGINX_CONF`: generated server block path. Default: `/etc/nginx/conf.d/ecs-homepage.conf`.
- `ECS_HOMEPAGE_SERVER_NAME`: Nginx `server_name`. Default: `_`.
- `ECS_HOMEPAGE_SKIP_NGINX=1`: copy files only, useful behind an existing reverse proxy.
- `ECS_HOMEPAGE_RELOAD_NGINX=0`: write config and run `nginx -t`, but do not reload.

## Verification Commands

```bash
nginx -t
curl -fsSI http://127.0.0.1/
curl -fsSI http://127.0.0.1/home/
curl -fsS http://127.0.0.1/healthz
curl -fsS http://127.0.0.1/version.json
```

## Rollback

The deployment is static and idempotent. To roll back, unpack an older package
and rerun:

```bash
sudo bash deploy/linux/deploy.sh
```

If Nginx was configured manually, restore the previous server block and run:

```bash
sudo nginx -t
sudo systemctl reload nginx
```
