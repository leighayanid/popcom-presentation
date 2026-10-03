<script setup lang="ts">
/**
 * Dark / light switch.
 *
 * Slidev persists the choice in localStorage ('slidev-color-schema'), so it
 * survives a reload and a presenter-window open. The control hides itself in
 * exports and print so it never lands in the PDF.
 *
 * This is the quick switch. The same choice, plus the colour theme, lives in
 * the settings page (SettingsPanel.vue).
 */
import { useDarkMode } from '@slidev/client'

const { isDark, toggleDark } = useDarkMode()
</script>

<template>
  <button
    class="theme-toggle"
    type="button"
    :aria-label="isDark ? 'Switch to light theme' : 'Switch to dark theme'"
    :title="(isDark ? 'Light' : 'Dark') + ' theme (D)'"
    @click="toggleDark()"
  >
    <span class="track" :class="{ lit: !isDark }">
      <span class="knob">
        <svg v-if="isDark" viewBox="0 0 24 24" class="ico">
          <path
            d="M20.2 14.2A8.4 8.4 0 0 1 9.8 3.8a8.4 8.4 0 1 0 10.4 10.4Z"
            fill="none" stroke="currentColor" stroke-width="1.9"
            stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <svg v-else viewBox="0 0 24 24" class="ico">
          <circle cx="12" cy="12" r="4.4" fill="none" stroke="currentColor" stroke-width="1.9" />
          <path
            d="M12 2.6v2.6M12 18.8v2.6M2.6 12h2.6M18.8 12h2.6M5.3 5.3l1.9 1.9M16.8 16.8l1.9 1.9M18.7 5.3l-1.9 1.9M7.2 16.8l-1.9 1.9"
            stroke="currentColor" stroke-width="1.9" stroke-linecap="round" />
        </svg>
      </span>
    </span>
  </button>
</template>

<style scoped>
.theme-toggle {
  /* positioned by the control cluster in global-top.vue */
  display: block;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  opacity: 0.32;
  transition: opacity 260ms ease;
}
.theme-toggle:hover,
.theme-toggle:focus-visible { opacity: 1; }
.theme-toggle:focus-visible { outline: 2px solid var(--oppo-gold); outline-offset: 4px; border-radius: 999px; }

.track {
  display: block;
  width: 46px;
  height: 25px;
  border-radius: 999px;
  background: var(--oppo-bg-2);
  border: 1px solid var(--g-30);
  position: relative;
  transition: background-color 300ms ease, border-color 300ms ease;
}

.knob {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 19px;
  height: 19px;
  border-radius: 50%;
  background: var(--oppo-gold);
  color: var(--oppo-bg-1);
  display: grid;
  place-items: center;
  transition: transform 320ms cubic-bezier(.34, 1.4, .5, 1), background-color 300ms ease;
}
.track.lit .knob { transform: translateX(21px); }

.ico { width: 12px; height: 12px; display: block; }

/* never show up in a print or export render */
@media print { .theme-toggle { display: none !important; } }
</style>
