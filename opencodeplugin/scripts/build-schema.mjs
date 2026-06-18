#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createConfigJsonSchema } from "../dist/config/json-schema.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputPath = path.join(root, "assets", "engineering-calc-system.schema.json");

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(outputPath, `${JSON.stringify(createConfigJsonSchema(), null, 2)}\n`, "utf8");
console.log(`Generated ${outputPath}`);

