/**
 * Which brand palette the deck is wearing.
 *
 * This is a second, independent axis from Slidev's own dark/light mode:
 *
 *   palette  →  html[data-deck-theme]   (oppo | pass)
 *   mode     →  html.dark / html.light  (Slidev's useDarkMode)
 *
 * Four token sets live in styles/index.css, one per combination. Components
 * never see any of this — they keep reading the same --oppo-* token names.
 */
import { ref, watch } from 'vue'

export type DeckTheme = 'oppo' | 'pass'

export interface ThemeMeta {
  id: DeckTheme
  name: string
  owner: string
  blurb: string
  /** Swatches for the settings preview, dark mode then light mode. */
  swatches: { dark: string[], light: string[] }
}

export const THEMES: ThemeMeta[] = [
  {
    id: 'oppo',
    name: 'OPPO Gold',
    owner: 'Office of the Provincial Population Officer',
    blurb: 'Deep navy stage with a single amber accent. Built for a projector in a lit hall — one accent colour carries every emphasis, so nothing competes with the figures.',
    swatches: {
      dark: ['#0a1a2f', '#12263f', '#f2b33d', '#f4f7fb', '#3987e5'],
      light: ['#f6f8fc', '#e9eff7', '#9c6f0a', '#0c1b2b', '#2a78d6'],
    },
  },
  {
    id: 'pass',
    name: 'Bataeño Pass',
    owner: 'Bataeño Pass Program · Province of Bataan',
    blurb: 'The Pass card\'s own palette: Bataan navy as the field, with the wordmark green and the circuit cyan carrying accent and data. Use this when the deck is shown alongside Pass collateral.',
    swatches: {
      dark: ['#002a5e', '#073a78', '#4fd6ff', '#eef6ff', '#8fd426'],
      light: ['#f4f8fd', '#e4eefa', '#06647f', '#04254a', '#5f8f00'],
    },
  },
]

const KEY = 'oppo-deck-theme'

function valid(v: unknown): DeckTheme | null {
  return v === 'oppo' || v === 'pass' ? v : null
}

/**
 * Resolution order, most explicit first:
 *
 *   ?theme=pass          one-off, e.g. a link handed to someone
 *   VITE_DECK_THEME      the whole run — this is how an export picks a palette,
 *                        since `slidev export` opens a fresh browser and the
 *                        saved choice below is never there to find
 *   localStorage         the viewer's own choice, from the settings page
 *   oppo                 the Office's own theme
 */
function restore(): DeckTheme {
  const fromQuery = valid(new URLSearchParams(location.search).get('theme'))
  if (fromQuery) return fromQuery

  const fromEnv = valid(import.meta.env?.VITE_DECK_THEME)
  if (fromEnv) return fromEnv

  try {
    const stored = valid(localStorage.getItem(KEY))
    if (stored) return stored
  }
  catch {
    // private mode / blocked storage — fall through to the default
  }
  return 'oppo'
}

/** Module-level so every caller shares one source of truth. */
export const deckTheme = ref<DeckTheme>(
  typeof window === 'undefined' ? 'oppo' : restore(),
)

export function applyDeckTheme(theme: DeckTheme = deckTheme.value) {
  if (typeof document === 'undefined') return
  document.documentElement.dataset.deckTheme = theme
}

if (typeof window !== 'undefined') {
  applyDeckTheme()
  watch(deckTheme, (v) => {
    applyDeckTheme(v)
    try {
      localStorage.setItem(KEY, v)
    }
    catch {
      // nothing to do — the choice just will not survive a reload
    }
  })
}

export function useDeckTheme() {
  return {
    theme: deckTheme,
    themes: THEMES,
    setTheme: (v: DeckTheme) => { deckTheme.value = v },
  }
}
