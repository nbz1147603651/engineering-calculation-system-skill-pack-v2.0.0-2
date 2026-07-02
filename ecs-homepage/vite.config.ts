import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { existsSync, readFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import type { Plugin } from 'vite'

type PackageJson = {
  name?: string
  version?: string
}

type ReleaseConfig = {
  version?: string
  created_at?: string
}

const projectRoot = dirname(fileURLToPath(import.meta.url))
const repoRoot = resolve(projectRoot, '..')
const packageJson = readJson<PackageJson>(resolve(projectRoot, 'package.json'))
const releaseConfigPath = resolve(repoRoot, 'engineering-calculation-system', 'tools', 'release_config.json')
const releaseConfig = existsSync(releaseConfigPath) ? readJson<ReleaseConfig>(releaseConfigPath) : null
const appVersion = releaseConfig?.version ?? packageJson.version ?? '0.0.0'

if (releaseConfig?.version && packageJson.version && releaseConfig.version !== packageJson.version) {
  throw new Error(
    `Version mismatch: release_config.json has ${releaseConfig.version}, package.json has ${packageJson.version}. Run npm run version:sync.`,
  )
}

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, 'utf8')) as T
}

function buildTimestamp() {
  if (process.env.BUILD_TIMESTAMP) return process.env.BUILD_TIMESTAMP
  if (process.env.SOURCE_DATE_EPOCH) {
    return new Date(Number(process.env.SOURCE_DATE_EPOCH) * 1000).toISOString()
  }
  return new Date().toISOString()
}

function versionManifestPlugin(): Plugin {
  return {
    name: 'ecs-homepage-version-manifest',
    generateBundle() {
      this.emitFile({
        type: 'asset',
        fileName: 'version.json',
        source: `${JSON.stringify(
          {
            name: packageJson.name ?? 'ecs-homepage',
            version: appVersion,
            packageVersion: packageJson.version ?? '',
            releaseCreatedAt: releaseConfig?.created_at ?? '',
            source: releaseConfig ? 'engineering-calculation-system/tools/release_config.json' : 'package.json',
            builtAt: buildTimestamp(),
          },
          null,
          2,
        )}\n`,
      })
    },
  }
}

export default defineConfig({
  plugins: [react(), tailwindcss(), versionManifestPlugin()],
  define: {
    __APP_VERSION__: JSON.stringify(appVersion),
  },
  resolve: {
    alias: {
      '@': resolve(projectRoot, 'src'),
    },
  },
  base: './',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
})
