FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.27-alpine

ARG ECS_HOMEPAGE_VERSION=0.0.0
LABEL org.opencontainers.image.title="ECS Homepage" \
      org.opencontainers.image.description="Engineering Calculation System public homepage" \
      org.opencontainers.image.version="${ECS_HOMEPAGE_VERSION}"

COPY deploy/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=build /app/dist /usr/share/nginx/html/home

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1/healthz >/dev/null || exit 1
