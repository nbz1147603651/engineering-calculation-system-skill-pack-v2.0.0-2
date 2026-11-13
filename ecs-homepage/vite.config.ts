import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { createReadStream, existsSync, readFileSync, realpathSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, resolve, relative, isAbsolute } from "node:path";
import { fileURLToPath } from "node:url";
import type { Plugin, PreviewServer, ViteDevServer } from "vite";

type PackageJson = {
  name?: string;
  version?: string;
};

type ReleaseConfig = {
  version?: string;
  created_at?: string;
};

const projectRoot = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(projectRoot, "..");
const packageJson = readJson<PackageJson>(resolve(projectRoot, "package.json"));
const releaseConfigPath = resolve(
  repoRoot,
  "engineering-calculation-system",
  "tools",
  "release_config.json",
);
const releaseConfig = existsSync(releaseConfigPath)
  ? readJson<ReleaseConfig>(releaseConfigPath)
  : null;
const appVersion = releaseConfig?.version ?? packageJson.version ?? "0.0.0";

if (
  releaseConfig?.version &&
  packageJson.version &&
  releaseConfig.version !== packageJson.version
) {
  throw new Error(
    `Version mismatch: release_config.json has ${releaseConfig.version}, package.json has ${packageJson.version}. Run npm run version:sync.`,
  );
}

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf8")) as T;
}

function buildTimestamp() {
  if (process.env.BUILD_TIMESTAMP) return process.env.BUILD_TIMESTAMP;
  if (process.env.SOURCE_DATE_EPOCH) {
    return new Date(Number(process.env.SOURCE_DATE_EPOCH) * 1000).toISOString();
  }
  return new Date().toISOString();
}

function versionManifestPlugin(): Plugin {
  return {
    name: "ecs-homepage-version-manifest",
    generateBundle() {
      this.emitFile({
        type: "asset",
        fileName: "version.json",
        source: `${JSON.stringify(
          {
            name: packageJson.name ?? "ecs-homepage",
            version: appVersion,
            packageVersion: packageJson.version ?? "",
            releaseCreatedAt: releaseConfig?.created_at ?? "",
            source: releaseConfig
              ? "engineering-calculation-system/tools/release_config.json"
              : "package.json",
            builtAt: buildTimestamp(),
          },
          null,
          2,
        )}\n`,
      });
    },
  };
}

// Keep local preview downloads identical to the production Nginx /downloads alias.
// Only these two release-owned files are served; request paths never become disk paths.
function clientDownloadsPlugin(): Plugin {
  const filename = `engineering-calc-system-installer-v${appVersion}.exe`;
  function clientDirectory() {
    // The workspace keeps immutable deliveries outside the product's legacy dist.
    // Discover that workspace through the invocation path, including a junction.
    for (const start of [process.env.INIT_CWD, process.cwd(), projectRoot]) {
      if (!start) continue;
      for (let base = resolve(start); dirname(base) !== base; base = dirname(base)) {
        const management = resolve(base, "management");
        const portfolio = resolve(management, "registry/portfolio.json");
        if (!existsSync(portfolio)) continue;
        const product = readJson<{ products: { id: string; source: string }[] }>(portfolio)
          .products.find((item) => item.id === "nimo-engineering");
        if (!product || realpathSync(resolve(management, product.source)).toLowerCase() !== realpathSync(repoRoot).toLowerCase()) continue;
        const releases = resolve(management, "release-artifacts/nimo-engineering");
        for (const name of ["LATEST-CLIENT.json", "LATEST-RELEASE.json"]) {
          const index = resolve(releases, name);
          if (!existsSync(index)) continue;
          const receipt = readJson<{ version: string; clientDirectory: string }>(index);
          const directory = realpathSync(receipt.clientDirectory);
          const child = relative(realpathSync(releases), directory);
          if (receipt.version !== appVersion || !child || child.startsWith("..") || isAbsolute(child)) throw new Error("Invalid current client reference");
          return directory;
        }
      }
    }
    return resolve(repoRoot, "engineering-calculation-system/dist/ui-client");
  }
  const configure = (server: ViteDevServer | PreviewServer) => {
    server.middlewares.use((req, res, next) => {
      const pathname = (req.url ?? "").split("?")[0];
      if (!pathname.startsWith("/downloads/")) return next();
      if (![`/downloads/${filename}`, "/downloads/CHECKSUMS.txt"].includes(pathname)) {
        res.statusCode = 404;
        res.end("Unknown client download.");
        return;
      }
      if (!["GET", "HEAD"].includes(req.method ?? "")) {
        res.statusCode = 405;
        res.setHeader("Allow", "GET, HEAD");
        res.end();
        return;
      }
      let file: string;
      let digest: string;
      try {
        const directory = clientDirectory();
        file = resolve(directory, filename);
        const receipt = readJson<{ version: string; installer: string; sha256: string }>(resolve(directory, "CLIENT-BUILD.json"));
        digest = createHash("sha256").update(readFileSync(file)).digest("hex");
        if (receipt.version !== appVersion || receipt.installer !== filename || receipt.sha256 !== digest) throw new Error("Client identity mismatch");
      } catch {
        res.statusCode = 404;
        res.end("Verified client release is not available. Build the current client first.");
        return;
      }
      if (pathname.endsWith("CHECKSUMS.txt")) {
        const body = `${digest}  ${filename}\n`;
        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Content-Length", Buffer.byteLength(body));
        res.setHeader("X-Content-Type-Options", "nosniff");
        res.end(req.method === "HEAD" ? undefined : body);
        return;
      }
      res.setHeader(
        "Content-Type",
        pathname.endsWith(".exe")
          ? "application/octet-stream"
          : "text/plain; charset=utf-8",
      );
      res.setHeader("Content-Length", statSync(file).size);
      res.setHeader("X-Content-Type-Options", "nosniff");
      if (pathname.endsWith(".exe"))
        res.setHeader(
          "Content-Disposition",
          `attachment; filename="${filename}"`,
        );
      if (req.method === "HEAD") {
        res.end();
        return;
      }
      const stream = createReadStream(file);
      stream.on("error", () => {
        if (!res.headersSent) res.statusCode = 500;
        res.end();
      });
      res.on("close", () => stream.destroy());
      stream.pipe(res);
    });
  };
  return {
    name: "nimo-client-downloads",
    configureServer: configure,
    configurePreviewServer: configure,
  };
}

export default defineConfig({
  plugins: [react(), versionManifestPlugin(), clientDownloadsPlugin()],
  define: {
    __APP_VERSION__: JSON.stringify(appVersion),
  },
  resolve: {
    alias: {
      "@": resolve(projectRoot, "src"),
    },
  },
  base: "./",
  build: {
    outDir: "dist",
    assetsDir: "assets",
  },
});
