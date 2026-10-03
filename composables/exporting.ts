/**
 * True when this page was opened by `slidev export` (or the print routes).
 *
 * Slidev's exporter has three entry shapes, and it emulates `media: screen`
 * throughout — so `@media print` never fires and the pathname alone is not
 * enough:
 *   /{no}?print=true     per-slide export
 *   /{no}?print=clicks   export with --with-clicks
 *   /presenter/print     notes export
 */
export function isExporting(): boolean {
  if (typeof window === 'undefined') return false
  const { pathname, search } = window.location
  return /\/(print|export)\b/.test(pathname)
    || new URLSearchParams(search).has('print')
}
