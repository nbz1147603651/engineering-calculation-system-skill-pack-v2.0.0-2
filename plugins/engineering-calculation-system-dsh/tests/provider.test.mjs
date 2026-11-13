/**
 * Contract tests for the packaged DeepSeek Harness skill provider.
 *
 * Run from this directory: `node --test tests/provider.test.mjs`
 */

import assert from 'node:assert/strict'
import { cp, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import test from 'node:test'

const PLUGIN_ROOT = dirname(dirname(fileURLToPath(import.meta.url)))
const BUNDLE_DIR = join(PLUGIN_ROOT, 'skills', 'engineering-calculation-system')
const INSTRUCTIONS = join(BUNDLE_DIR, 'SKILL.md')
const SKILL_NAME = 'engineering-calculation-system'

/** Import the plugin and capture the provider `apply` registers. */
async function loadProvider() {
  const module = await import(pathToFileURL(join(PLUGIN_ROOT, 'lib', 'index.js')).href)
  let registered
  module.apply({ skills: { registerProvider: (factory) => { registered = factory() } } })
  assert.ok(registered, 'apply must register a skill provider')
  return registered
}

/** Drop the YAML frontmatter the way the provider does, for body comparison. */
function bodyOf(text) {
  const lines = text.split(/\r?\n/)
  const closing = lines.indexOf('---', 1)
  return lines.slice(closing + 1).join('\n').trim()
}

test('publishes exactly the packaged skill with bundled metadata', async () => {
  const provider = await loadProvider()
  assert.equal(provider.name, SKILL_NAME)

  const candidates = await provider.list({})
  assert.equal(candidates.length, 1, 'the package ships one skill')
  const [candidate] = candidates
  assert.equal(candidate.name, SKILL_NAME)
  assert.equal(candidate.source, 'bundled')
  assert.equal(candidate.rank, 600, 'bundled rank loses to project and user scopes')
  assert.deepEqual(candidate.invocation, { modelInvocable: true, userInvocable: true })
  assert.equal(candidate.provider, provider.name)
  assert.equal(candidate.resourceBase.kind, 'directory')
  assert.equal(candidate.resourceBase.path, BUNDLE_DIR, 'relative references resolve inside the bundle')
  assert.ok(candidate.description.length > 40)
  const contract = JSON.parse(await readFile(join(BUNDLE_DIR, 'schemas', 'artifact_contracts.json'), 'utf8'))
  const manifest = JSON.parse(await readFile(join(PLUGIN_ROOT, 'package.json'), 'utf8'))
  assert.equal(candidate.metadata.version, contract.version, 'provider metadata must match the bundled artifact contract')
  assert.equal(manifest.version.split('+')[0], contract.version, 'plugin package must match the bundled artifact contract')
  const releaseConfig = join(PLUGIN_ROOT, '..', '..', 'engineering-calculation-system', 'tools', 'release_config.json')
  if (existsSync(releaseConfig)) {
    const release = JSON.parse(await readFile(releaseConfig, 'utf8'))
    assert.equal(contract.version, release.version, 'source checkout must match the canonical release version')
  }
})

test('loads the current body and keeps its relative references resolvable', async () => {
  const provider = await loadProvider()
  const [candidate] = await provider.list({})
  const skill = await provider.get(candidate, {})

  const raw = await readFile(INSTRUCTIONS, 'utf8')
  assert.equal(skill.content, bodyOf(raw))
  assert.ok(skill.content.startsWith('# Engineering Calculation System'))
  assert.match(skill.content, /## DSH Plugin Adapter/)
  assert.ok(skill.content.includes('skills/00-engineering-calculation-router.skill.md'))

  for (const relative of [
    'skills/00-engineering-calculation-router.skill.md',
    'shared/lifecycle.md',
    'shared/dsh-plugin-adapter.md',
    'scripts/validate_artifacts.py',
    'scripts/delivery_policy.py',
    'project_template/engineering_calc_project/pyproject.toml',
    'project_template/engineering_calc_project/src/pkg/interfaces/input_mapping.py',
    'project_template/engineering_calc_project/src/pkg/report/context_helpers.py',
  ]) {
    assert.ok(existsSync(join(skill.resourceBase.path, relative)), `${relative} must ship in the bundle`)
  }
})

test('rereads the body on every load', async () => {
  const provider = await loadProvider()
  const [candidate] = await provider.list({})
  const loaded = await provider.get(candidate, {})
  assert.ok(loaded.content.length > 0)
  assert.equal(typeof loaded.provider, 'string')
})

test('honours an abort signal while listing', async () => {
  const provider = await loadProvider()
  const controller = new AbortController()
  controller.abort(new Error('cancelled'))
  await assert.rejects(provider.list({ signal: controller.signal }))
})

test('rejects a bundle whose frontmatter cannot produce a catalog entry', async (t) => {
  const scratch = await mkdtemp(join(tmpdir(), 'ecs-dsh-provider-'))
  t.after(() => rm(scratch, { recursive: true, force: true }))
  const modulePath = join(scratch, 'lib', 'index.js')
  await cp(join(PLUGIN_ROOT, 'lib'), join(scratch, 'lib'), { recursive: true })
  await cp(join(PLUGIN_ROOT, 'skills'), join(scratch, 'skills'), { recursive: true })
  const brokenInstructions = join(scratch, 'skills', SKILL_NAME, 'SKILL.md')

  const cases = [
    ['missing description', '---\nname: engineering-calculation-system\n---\n\n# Body\n'],
    ['non kebab-case name', '---\nname: Engineering_Calculation\nversion: 1\n---\n\n# Body\n'],
    ['unclosed frontmatter', '---\nname: engineering-calculation-system\ndescription: A long enough description for the catalog entry to be accepted.\n'],
    ['non-scalar scalar field', '---\nname: engineering-calculation-system\ndescription: >-\n  folded\n---\n\n# Body\n'],
  ]

  const module = await import(pathToFileURL(modulePath).href)
  for (const [label, content] of cases) {
    await writeFile(brokenInstructions, content, 'utf8')
    let provider
    module.apply({ skills: { registerProvider: (factory) => { provider = factory() } } })
    await assert.rejects(provider.list({}), `${label} must fail loudly`)
  }
})

test('returns undefined when the packaged instructions disappear', async (t) => {
  const scratch = await mkdtemp(join(tmpdir(), 'ecs-dsh-provider-'))
  t.after(() => rm(scratch, { recursive: true, force: true }))
  await cp(join(PLUGIN_ROOT, 'lib'), join(scratch, 'lib'), { recursive: true })
  await cp(join(PLUGIN_ROOT, 'skills'), join(scratch, 'skills'), { recursive: true })
  const module = await import(pathToFileURL(join(scratch, 'lib', 'index.js')).href)
  let provider
  module.apply({ skills: { registerProvider: (factory) => { provider = factory() } } })
  const [candidate] = await provider.list({})
  await rm(join(scratch, 'skills', SKILL_NAME, 'SKILL.md'))
  assert.equal(await provider.get(candidate, {}), undefined)
})

test('fails at load when the package ships no skill bundle', async (t) => {
  const scratch = await mkdtemp(join(tmpdir(), 'ecs-dsh-provider-'))
  t.after(() => rm(scratch, { recursive: true, force: true }))
  await cp(join(PLUGIN_ROOT, 'lib'), join(scratch, 'lib'), { recursive: true })
  await cp(join(PLUGIN_ROOT, 'skills'), join(scratch, 'skills'), { recursive: true })
  await rm(join(scratch, 'skills'), { recursive: true, force: true })
  const module = await import(pathToFileURL(join(scratch, 'lib', 'index.js')).href)
  assert.throws(
    () => module.apply({ skills: { registerProvider: () => {} } }),
    /no skill bundle found/,
  )
})
