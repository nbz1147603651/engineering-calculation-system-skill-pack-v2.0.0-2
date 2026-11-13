/**
 * Bundled Engineering Calculation System skill provider for DeepSeek Harness.
 *
 * The package ships one complete skill bundle under `skills/` and registers a
 * `ctx.skills` provider that publishes it to every session of the profiles the
 * bundle is installed into. Discovery reads each bundle's `SKILL.md`
 * frontmatter into a catalog entry; every load re-reads the instructions file,
 * so editing a body changes later loads without a version bump. Relative paths
 * inside a body resolve against the published directory resource base, which is
 * the whole shipped bundle.
 *
 * @module @engineering-calculation-system/dsh-plugin
 */

import { readdirSync, statSync } from 'node:fs'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

/**
 * Rank reserved for packaged skill providers and local bundled roots. It
 * restates `BUNDLED_SKILL_RANK` from `@deepseek-ai/dsh-skill` so this module
 * needs no runtime import from the host's package graph.
 */
const BUNDLED_SKILL_RANK = 600

/** Unique provider name inside the `ctx.skills` registry. */
const PROVIDER_NAME = 'engineering-calculation-system'

/** Directory holding the shipped skill bundles, one directory bundle per skill. */
const SKILLS_ROOT = fileURLToPath(new URL('../skills/', import.meta.url))

/** Cordis plugin name, matching the composition row in `cordis.patch.yml`. */
export const name = 'engineering-calculation-system'

/** Services this plugin registers on. */
export const inject = ['skills']

/**
 * Register the packaged skill provider on `ctx.skills`.
 *
 * A package that ships no usable skill bundle is a broken installation rather
 * than a profile without skills, so the packaged root is validated here, where
 * the failure names its own cause instead of surfacing as an empty catalog.
 *
 * @param ctx - Cordis context carrying the `skills` registry.
 * @throws When the packaged `skills` root holds no `SKILL.md` bundle.
 */
export function apply(ctx) {
  const bundles = discoverBundlesSync(SKILLS_ROOT)
  if (bundles.length === 0) {
    throw new Error(`engineering-calculation-system: no skill bundle found under ${SKILLS_ROOT}`)
  }
  ctx.skills.registerProvider(() => new PackagedSkillProvider(bundles))
}

/** Provider that serves the skill bundles shipped inside this package. */
class PackagedSkillProvider {
  /**
   * @param bundles - absolute `SKILL.md` paths discovered at load time.
   */
  constructor(bundles) {
    this.name = PROVIDER_NAME
    this.bundles = bundles
  }

  /**
   * Discover the packaged skill catalog.
   *
   * @param options - lookup options; `signal` cancels pending reads.
   * @returns one candidate per shipped skill bundle.
   */
  async list(options) {
    const candidates = []
    for (const instructionsPath of this.bundles) {
      options?.signal?.throwIfAborted()
      const parsed = await readSkill(instructionsPath, options?.signal)
      if (parsed === undefined) continue
      candidates.push(candidateFor(parsed))
    }
    return candidates
  }

  /**
   * Load one complete skill definition.
   *
   * @param candidate - a candidate previously returned by this provider.
   * @param options - lookup options; `signal` cancels pending reads.
   * @returns the current definition, or undefined when the shipped file is gone
   *   or now declares a different skill name.
   */
  async get(candidate, options) {
    const parsed = await readSkill(candidate.locator, options?.signal)
    if (parsed === undefined || parsed.name !== candidate.name) return undefined
    return { ...definitionFields(parsed), content: parsed.body }
  }
}

/**
 * Build the catalog entry for one parsed bundle.
 *
 * @param parsed - parsed instructions file.
 * @returns the candidate the registry merges with other providers.
 */
function candidateFor(parsed) {
  return {
    ...definitionFields(parsed),
    rank: BUNDLED_SKILL_RANK,
    locator: parsed.instructionsPath,
  }
}

/**
 * Build every definition field except the body, shared by the candidate and the
 * loaded definition so both consumers observe one description and resource base.
 *
 * @param parsed - parsed instructions file.
 * @returns the shared definition fields.
 */
function definitionFields(parsed) {
  return {
    name: parsed.name,
    description: parsed.description,
    ...parsed.whenToUse === undefined ? {} : { whenToUse: parsed.whenToUse },
    invocation: parsed.invocation,
    provider: PROVIDER_NAME,
    source: 'bundled',
    resourceBase: parsed.resourceBase,
    path: parsed.instructionsPath,
    ...parsed.metadata === undefined ? {} : { metadata: parsed.metadata },
  }
}

/**
 * Read and parse one shipped `SKILL.md`.
 *
 * @param instructionsPath - absolute path to the instructions file.
 * @param signal - optional abort signal for the file read.
 * @returns the parsed bundle, or undefined when the file is absent.
 */
async function readSkill(instructionsPath, signal) {
  signal?.throwIfAborted()
  let raw
  try {
    raw = await readFile(instructionsPath, 'utf8')
  } catch (error) {
    if (isAbsentPathError(error)) return undefined
    throw error
  }
  signal?.throwIfAborted()
  return parseSkill(raw, instructionsPath)
}

/**
 * Discover the shipped bundles synchronously so a broken package fails at load.
 *
 * @param skillsRoot - packaged skills directory.
 * @returns `SKILL.md` paths of every directory bundle, sorted by name.
 */
function discoverBundlesSync(skillsRoot) {
  let entries
  try {
    entries = readdirSync(skillsRoot, { withFileTypes: true })
  } catch (error) {
    if (isAbsentPathError(error)) return []
    throw error
  }
  return entries
    .filter(entry => entry.isDirectory())
    .map(entry => join(skillsRoot, entry.name, 'SKILL.md'))
    .filter(instructionsPath => {
      try {
        return statSync(instructionsPath).isFile()
      } catch (error) {
        if (isAbsentPathError(error)) return false
        throw error
      }
    })
    .sort()
}

/**
 * Parse one instructions file into the fields the skill registry consumes.
 *
 * Frontmatter is the skill pack's own authoring format: a flat mapping of
 * single-line scalars. A missing or non-scalar `name`/`description`, and a name
 * outside the registry's kebab-case grammar, are packaging errors, so they throw
 * rather than publishing a partial skill into the session catalog.
 *
 * @param raw - file content.
 * @param instructionsPath - absolute path, used in messages and as the locator.
 * @returns the parsed bundle fields including the body.
 */
function parseSkill(raw, instructionsPath) {
  const lines = raw.split(/\r?\n/)
  if (lines[0] !== '---') {
    throw new Error(`${instructionsPath}: skill frontmatter must start on the first line`)
  }
  const closingIndex = lines.indexOf('---', 1)
  if (closingIndex < 0) {
    throw new Error(`${instructionsPath}: skill frontmatter is not closed`)
  }
  const frontmatter = lines.slice(1, closingIndex)
  const skillName = requireScalar(frontmatter, 'name', instructionsPath)
  const description = requireScalar(frontmatter, 'description', instructionsPath)
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(skillName)) {
    throw new Error(`${instructionsPath}: skill name "${skillName}" is not kebab-case`)
  }
  const directory = instructionsPath.slice(0, instructionsPath.length - 'SKILL.md'.length - 1)
  const metadata = collectMetadata(frontmatter, instructionsPath)
  return {
    name: skillName,
    description,
    ...optionalScalar(frontmatter, 'whenToUse', instructionsPath),
    invocation: parseInvocation(frontmatter, instructionsPath),
    ...metadata === undefined ? {} : { metadata },
    instructionsPath,
    resourceBase: { kind: 'directory', path: directory },
    body: lines.slice(closingIndex + 1).join('\n').trim(),
  }
}

/**
 * Read one required non-empty single-line frontmatter scalar.
 *
 * @param frontmatter - frontmatter lines without the delimiters.
 * @param key - field name.
 * @param instructionsPath - absolute path, used in messages.
 * @returns the unquoted scalar value.
 */
function requireScalar(frontmatter, key, instructionsPath) {
  const value = scalarField(frontmatter, key, instructionsPath)
  if (value === undefined || value.length === 0) {
    throw new Error(`${instructionsPath}: skill frontmatter requires a non-empty "${key}"`)
  }
  return value
}

/**
 * Read one optional single-line frontmatter scalar.
 *
 * @param frontmatter - frontmatter lines without the delimiters.
 * @param key - field name.
 * @param instructionsPath - absolute path, used in messages.
 * @returns an object carrying the field when present, otherwise an empty object.
 */
function optionalScalar(frontmatter, key, instructionsPath) {
  const value = scalarField(frontmatter, key, instructionsPath)
  return value === undefined || value.length === 0 ? {} : { [key]: value }
}

/**
 * Read one frontmatter scalar field.
 *
 * @param frontmatter - frontmatter lines without the delimiters.
 * @param key - field name.
 * @param instructionsPath - absolute path, used in messages.
 * @returns the unquoted value, or undefined when the field is absent.
 */
function scalarField(frontmatter, key, instructionsPath) {
  const prefix = `${key}:`
  const line = frontmatter.find(candidate => candidate.startsWith(prefix))
  if (line === undefined) return undefined
  const value = line.slice(prefix.length).trim()
  if (value === '' || /^[>|[{]/.test(value)) {
    throw new Error(`${instructionsPath}: frontmatter field "${key}" must be a single-line scalar`)
  }
  if (value.startsWith('"') || value.startsWith("'")) {
    if (value.length < 2 || value.at(-1) !== value[0]) {
      throw new Error(`${instructionsPath}: frontmatter field "${key}" has an unterminated quote`)
    }
    return value.slice(1, -1)
  }
  return value
}

/**
 * Collect every frontmatter field the registry does not consume into metadata.
 *
 * @param frontmatter - frontmatter lines without the delimiters.
 * @param instructionsPath - absolute path, used in messages.
 * @returns the metadata object, or undefined when the frontmatter carries none.
 */
function collectMetadata(frontmatter, instructionsPath) {
  const consumed = new Set(['name', 'description', 'whenToUse', 'user-invocable', 'disable-model-invocation'])
  const metadata = {}
  for (const line of frontmatter) {
    const separator = line.indexOf(':')
    if (separator < 1) continue
    const key = line.slice(0, separator).trim()
    if (consumed.has(key) || key in metadata) continue
    metadata[key] = scalarField(frontmatter, key, instructionsPath)
  }
  return Object.keys(metadata).length === 0 ? undefined : metadata
}

/**
 * Resolve the two invocation controls from frontmatter.
 *
 * @param frontmatter - frontmatter lines without the delimiters.
 * @param instructionsPath - absolute path, used in messages.
 * @returns the invocation policy; an omitted field permits its surface.
 */
function parseInvocation(frontmatter, instructionsPath) {
  const disableModelInvocation = optionalBoolean(frontmatter, 'disable-model-invocation', instructionsPath)
  const userInvocable = optionalBoolean(frontmatter, 'user-invocable', instructionsPath)
  return {
    modelInvocable: disableModelInvocation !== true,
    userInvocable: userInvocable !== false,
  }
}

/**
 * Read one optional boolean frontmatter field.
 *
 * @param frontmatter - frontmatter lines without the delimiters.
 * @param key - field name.
 * @param instructionsPath - absolute path, used in messages.
 * @returns the boolean, or undefined when the field is absent.
 */
function optionalBoolean(frontmatter, key, instructionsPath) {
  const value = scalarField(frontmatter, key, instructionsPath)
  if (value === undefined) return undefined
  switch (value.toLowerCase()) {
    case 'true':
    case 'yes':
    case 'on':
    case '1':
      return true
    case 'false':
    case 'no':
    case 'off':
    case '0':
      return false
    default:
      throw new Error(`${instructionsPath}: frontmatter field "${key}" must be a boolean`)
  }
}

/**
 * Report whether a filesystem error means the path is absent.
 *
 * @param error - suspected filesystem error.
 * @returns whether the error code is ENOENT or ENOTDIR.
 */
function isAbsentPathError(error) {
  return typeof error === 'object'
    && error !== null
    && 'code' in error
    && (error.code === 'ENOENT' || error.code === 'ENOTDIR')
}
