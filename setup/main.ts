import { defineAppSetup } from '@slidev/types'
import { useDarkMode } from '@slidev/client'
import { isExporting } from '../composables/exporting'

/**
 * The deck is authored for a projector, so it opens dark the first time a
 * browser sees it, whatever the OS prefers. After that the viewer's own
 * choice wins — Slidev persists it in localStorage.
 *
 * Exports are left alone: the exporter emulates a colour scheme (light by
 * default, dark with `--dark`), and seeding here would override that and make
 * `slidev export` ignore the flag.
 */
const SEED = 'oppo-theme-seeded'

export default defineAppSetup(() => {
  if (isExporting()) return
  try {
    if (typeof localStorage === 'undefined') return
    if (!localStorage.getItem(SEED)) {
      localStorage.setItem(SEED, '1')
      useDarkMode().isDark.value = true
    }
  }
  catch {
    // private mode / blocked storage — fall back to the OS preference
  }
})
