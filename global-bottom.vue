<script setup lang="ts">
import { computed } from 'vue'
import { useNav } from '@slidev/client'

const { currentPage, total } = useNav()
const pct = computed(() => {
  const t = Number(total.value) || 1
  return Math.min(100, (Number(currentPage.value) / t) * 100)
})
const hidden = computed(() => Number(currentPage.value) <= 1)
</script>

<template>
  <div class="oppo-foot" :class="{ hide: hidden }">
    <div class="bar"><div class="fill" :style="{ width: pct + '%' }" /></div>
    <div class="meta">
      <span class="who">
        <img class="seal" src="/oppo-seal.png" alt="" aria-hidden="true" >
        Office of the Provincial Population Officer &#183; Province of Bataan
      </span>
      <span class="tnum">{{ currentPage }} / {{ total }}</span>
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
</style>
