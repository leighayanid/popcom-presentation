#!/usr/bin/env node
/**
 * Build a self-contained folder that presents the deck on a machine with no
 * Node, no npm and no network.
 *
 *   node scripts/offline.mjs [oppo|pass] [--out <dir>]
 *
 * What makes it portable is the PowerShell server copied in beside it: a
 * Slidev build is an ES-module SPA, and Chromium will not load those over
 * file://, so the folder has to be served -- just not by anything you have
 * to install. The default `/` base is deliberate: the server always serves
 * the bundle at its root, and a relative base would break the nested routes
 * (/presenter/3 would look for its assets under /presenter/).
 */
import { spawn } from 'node:child_process'
import { createRequire } from 'node:module'
import { copyFile, mkdir } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const argv = process.argv.slice(2)

const theme = argv.find(a => ['oppo', 'pass'].includes(a)) ?? 'oppo'
const outIdx = argv.indexOf('--out')
const out = outIdx !== -1 ? argv[outIdx + 1] : 'offline'

console.log(`building offline bundle  theme=${theme}  ->  ${out}/`)

const cli = createRequire(import.meta.url).resolve('@slidev/cli/bin/slidev.mjs')

// --download is deliberately absent: a whole-deck PDF comes out blank for
// this deck (see export.mjs), so it would ship a broken download button.
const child = spawn(
  process.execPath,
  [cli, 'build', '--out', out],
  { stdio: 'inherit', env: { ...process.env, VITE_DECK_THEME: theme } },
)

child.on('exit', async code => {
  if (code !== 0) process.exit(code ?? 1)
  await mkdir(out, { recursive: true })
  for (const f of ['serve-offline.ps1', 'Present.cmd']) {
    await copyFile(join(here, f), join(out, f))
  }
  console.log(`\n  ${out}/ is ready to copy anywhere.`)
  console.log(`  On the far machine: double-click Present.cmd\n`)
})
