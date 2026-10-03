#!/usr/bin/env node
/**
 * Export the deck in a chosen colour theme.
 *
 *   node scripts/export.mjs [oppo|pass] [dark|light] [pdf|png]
 *
 * `slidev export` opens a fresh browser, so the palette saved by the settings
 * page is never there to find — it has to be passed in. The deck reads
 * VITE_DECK_THEME (see composables/deck-theme.ts), and setting an env var
 * straight in an npm script is not portable across cmd.exe and sh, so it is
 * set here instead.
 *
 * Dark/light is a separate matter: the exporter emulates its own colour
 * scheme, so that one travels as slidev's own --dark flag.
 */
import { spawn } from 'node:child_process'
import { createRequire } from 'node:module'

const argv = process.argv.slice(2)
const pick = (allowed, fallback) => argv.find(a => allowed.includes(a)) ?? fallback

const theme = pick(['oppo', 'pass'], 'oppo')
const mode = pick(['dark', 'light'], 'dark')
const format = pick(['pdf', 'png'], 'pdf')

const BASE = 'Flag Ceremony - OPPO Department Report'
const suffix = [
  theme === 'pass' ? 'Bataeno Pass' : null,
  mode === 'light' ? 'light' : null,
].filter(Boolean).join(', ')
const name = suffix ? `${BASE} (${suffix})` : BASE

// --per-slide is not optional for this deck: a whole-deck export comes out blank.
const args = ['export', '--per-slide']
if (mode === 'dark') args.push('--dark')
if (format === 'png') args.push('--format', 'png')
args.push('--output', format === 'png' ? name : `${name}.pdf`)

console.log(`exporting  theme=${theme}  mode=${mode}  format=${format}\n       ->  ${name}`)

// Run the CLI's entry directly rather than through a shell: the output name
// has spaces in it, and a shell would split it into separate arguments.
const cli = createRequire(import.meta.url).resolve('@slidev/cli/bin/slidev.mjs')

const child = spawn(process.execPath, [cli, ...args], {
  stdio: 'inherit',
  env: { ...process.env, VITE_DECK_THEME: theme },
})
child.on('exit', code => process.exit(code ?? 1))
