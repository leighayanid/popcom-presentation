<script setup lang="ts">
import { computed } from 'vue'
import { useNav } from '@slidev/client'
import { isExporting } from './composables/exporting'

const { currentPage, total, clicks, clicksTotal } = useNav()
const pct = computed(() => {
  const t = Number(total.value) || 1
  return Math.min(100, (Number(currentPage.value) / t) * 100)
})
const hidden = computed(() => Number(currentPage.value) <= 1)

// Click steps for the slide on screen. Each click state is its own page in a
// PDF, so the counter is meaningless there and stays out of the export.
const exporting = isExporting()
const steps = computed(() => Number(clicksTotal.value) || 0)
const taken = computed(() => Math.min(steps.value, Math.max(0, Number(clicks.value) || 0)))
const left = computed(() => steps.value - taken.value)
const showSteps = computed(() => !exporting && steps.value > 0)
</script>

<template>
  <div class="oppo-foot" :class="{ hide: hidden }">
    <div class="bar"><div class="fill" :style="{ width: pct + '%' }" /></div>
    <div class="meta">
      <span class="who">
        <img class="seal" src="/oppo-seal.png" alt="" aria-hidden="true" >
        Office of the Provincial Population Officer &#183; Province of Bataan
      </span>
      <span class="right">
        <span v-if="showSteps" class="steps" :title="`${left} of ${steps} click steps remaining`">
          <span class="dots" aria-hidden="true">
            <i v-for="n in steps" :key="n" :class="{ on: n <= taken }" />
          </span>
          <span class="tnum">{{ left }} left</span>
        </span>
        <span class="tnum">{{ currentPage }} / {{ total }}</span>
      </span>
    </div>
  </div>
</template>

<style scoped>
.oppo-foot {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  z-index: 20;
  pointer-events: none;
  transition: opacity 400ms ease;
}
.oppo-foot.hide { opacity: 0; }
.bar { height: 2px; background: var(--h-10); }
.fill {
  height: 100%;
  background: linear-gradient(to right, var(--g-35), var(--oppo-gold));
  transition: width 500ms cubic-bezier(.22, 1, .36, 1);
}
.meta {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem 1.1rem 0.4rem;
  font-size: 0.56rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--oppo-ink-4);
}
.who { display: inline-flex; align-items: center; gap: 0.45rem; }
.seal {
  height: 15px;
  width: 15px;
  border-radius: 50%;
  opacity: 0.85;
  flex: none;
}
.right { display: inline-flex; align-items: center; gap: 0.8rem; }
.steps { display: inline-flex; align-items: center; gap: 0.4rem; }
.dots { display: inline-flex; align-items: center; gap: 3px; }
.dots i {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--oppo-ink-5);
  transition: background-color 300ms ease;
}
.dots i.on { background: var(--oppo-gold); }
</style>
