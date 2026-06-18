#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const cli = path.join(root, "dist", "cli", "index.js");

if (!existsSync(cli)) {
  const build = spawnSync("npm", ["run", "build"], { cwd: root, stdio: "inherit", shell: process.platform === "win32" });
  if (build.status !== 0) process.exit(build.status ?? 1);
}

const args = process.argv.slice(2);
const hasCommand = args[0] && !args[0].startsWith("-");
const finalArgs = hasCommand ? args : ["install", ...args];
const result = spawnSync(process.execPath, [cli, ...finalArgs], { cwd: root, stdio: "inherit" });
process.exit(result.status ?? 1);
