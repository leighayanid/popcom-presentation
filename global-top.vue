<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import ThemeToggle from './components/ThemeToggle.vue'
import SettingsPanel from './components/SettingsPanel.vue'
import { isExporting } from './composables/exporting'
import { applyDeckTheme } from './composables/deck-theme'

// Global layers render on the export routes too, and the controls have no
// business in a PDF. Those are distinct entry URLs, so one read at setup is
// enough.
const hidden = isExporting()

// The saved palette is written to <html> by the composable on import; this
// re-applies it once the app is mounted, which also covers the presenter
// window opening into a fresh document.
onMounted(() => applyDeckTheme())

const settingsOpen = ref(false)

// ',' is the usual "settings" key and Slidev binds nothing to it. Ignored while
// typing into a field, and while the page itself is open (it stops its own
// keys from reaching the window).
function onKey(e: KeyboardEvent) {
  if (e.key !== ',' || e.metaKey || e.ctrlKey || e.altKey) return
  const el = e.target as HTMLElement | null
  if (el?.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el?.tagName ?? '')) return
  settingsOpen.value = !settingsOpen.value
}

onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <template v-if="!hidden">
    <div class="deck-controls">
      <button
        class="gear"
        type="button"
        aria-label="Deck settings"
        title="Deck settings (,)"
        @click="settingsOpen = true"
      >
        <svg viewBox="0 0 24 24" class="ico">
          <circle cx="12" cy="12" r="3.1" fill="none" stroke="currentColor" stroke-width="1.9" />
          <path
            d="M19.4 14a1.7 1.7 0 0 0 .34 1.87l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.7 1.7 0 0 0-1.87-.34 1.7 1.7 0 0 0-1.03 1.56V20a2 2 0 1 1-4 0v-.09A1.7 1.7 0 0 0 8.9 18.3a1.7 1.7 0 0 0-1.87.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 14a1.7 1.7 0 0 0-1.56-1.03H3a2 2 0 1 1 0-4h.09A1.7 1.7 0 0 0 4.6 7.94a1.7 1.7 0 0 0-.34-1.87l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 3.6a1.7 1.7 0 0 0 1.03-1.56V2a2 2 0 1 1 4 0v.09A1.7 1.7 0 0 0 15.06 3.6a1.7 1.7 0 0 0 1.87-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 8v.06a1.7 1.7 0 0 0 1.56 1.03H21a2 2 0 1 1 0 4h-.09A1.7 1.7 0 0 0 19.4 14Z"
            fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"
          />
        </svg>
      </button>
      <ThemeToggle />
    </div>
    <SettingsPanel v-model:open="settingsOpen" />
  </template>
</template>

<style scoped>
.deck-controls {
  position: fixed;
  top: 0.85rem;
  right: 0.85rem;
  z-index: 60;
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.gear {
  display: grid;
  place-items: center;
  width: 25px;
  height: 25px;
  padding: 0;
  border-radius: 999px;
  border: 1px solid var(--g-30);
  background: var(--oppo-bg-2);
  color: var(--oppo-gold);
  cursor: pointer;
  opacity: 0.32;
  transition: opacity 260ms ease, border-color 260ms ease;
}
.gear:hover,
.gear:focus-visible { opacity: 1; }
.gear:focus-visible { outline: 2px solid var(--oppo-gold); outline-offset: 3px; }
.ico { width: 13px; height: 13px; display: block; }

@media print { .deck-controls { display: none !important; } }
</style>
