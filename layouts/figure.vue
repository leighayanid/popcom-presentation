<script setup lang="ts">
// Title rail on the left edge, figure gets the rest of the stage.
</script>

<template>
  <div class="slidev-layout oppo-figure">
    <slot />
  </div>
</template>

<style scoped>
.oppo-figure {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1.7rem 2.4rem 1.4rem;
}
.oppo-figure :deep(h1) { font-size: 1.85rem; margin: 0; }
.oppo-figure :deep(.fig) { flex: 1; min-height: 0; display: flex; align-items: center; }
.oppo-figure :deep(.fig) > * { width: 100%; }
</style>
