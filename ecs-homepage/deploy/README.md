# ECS Homepage Deployment

This homepage follows the same deployment shape used by the CAD- homepage:
build static files first, then let Nginx serve them directly at `/` and `/home/`.

## Version control

`engineering-calculation-system/tools/release_config.json` is the central product
version source. `ecs-homepage/package.json` is only the npm mirror so Docker builds
can still work when the parent repository is outside the Docker context.

```powershell
npm run version:sync
npm run version:check
```

The built site exposes the release identity at:

```text
/version.json
```

## Local build

```powershell
npm ci
npm run version:check
npm run build
npm run preview
```

The production assets are written to `dist/`.

## Linux cloud web package

```powershell
python ..\engineering-calculation-system\tools\build_release.py --profile ui-client
npm run package:static
```

The package script builds `dist/`, verifies the matching GUI installer exists,
copies it into the server `/downloads/` path, creates a cloud-server-ready
package, and writes both the zip and checksum to:

```text
release/ecs-homepage-<version>-linux-web.zip
release/ecs-homepage-<version>-linux-web.zip.sha256
```

The zip contains:

```text
ecs-homepage-<version>-linux-web/
  README.md
  VERSION
  deployment-manifest.json
  site/
  site/downloads/engineering-calc-system-installer-v<version>.exe
  site/home/
  deploy/AGENT_DEPLOYMENT.md
  deploy/linux/deploy.sh
  deploy/nginx/ecs-homepage-linux.conf.template
```

The duplicated `site/home/` directory intentionally matches the Docker
deployment shape, so the same Nginx routes work for `/` and `/home/`.
The homepage CTA uses the absolute `/downloads/` URL, so one installer copy
serves both entrypoints.

## Docker deployment

```powershell
npm run docker:build
npm run docker:up
```

The site is served at:

```text
http://localhost:8080/
http://localhost:8080/home/
http://localhost:8080/healthz
http://localhost:8080/version.json
```

Change the published port with:

```powershell
$env:ECS_HOMEPAGE_PORT=8088
npm run docker:up
```

## Linux Nginx handoff

For a non-container server, prefer the Linux web package:

```bash
sha256sum -c ecs-homepage-<version>-linux-web.zip.sha256
unzip ecs-homepage-<version>-linux-web.zip
cd ecs-homepage-<version>-linux-web
sudo bash deploy/linux/deploy.sh
```

For a custom domain:

```bash
sudo ECS_HOMEPAGE_SERVER_NAME=example.com bash deploy/linux/deploy.sh
```

For a manual handoff, copy the package `site/` directory to:

```text
/opt/ecs-homepage/site
```

Then adapt `deploy/nginx/ecs-homepage-linux.conf.template` so `root` points at
that exact `site` directory. Keep both `/` and `/home/` available if older links
may exist.

Before exposing the server:

```bash
nginx -t
curl -fsSI http://127.0.0.1/
curl -fsSI http://127.0.0.1/home/
curl -fsS http://127.0.0.1/healthz
curl -fsS http://127.0.0.1/version.json
```
