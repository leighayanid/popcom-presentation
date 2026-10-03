<script setup lang="ts">
// Cover: slow-drifting constellation of citizen dots behind the title block.
const dots = Array.from({ length: 16 }, (_, i) => ({
  x: (i * 83) % 160,
  y: (i * 37) % 90,
  r: 0.8 + ((i * 13) % 5) * 0.28,
  d: 5 + ((i * 7) % 11),
  o: 0.1 + ((i * 11) % 6) * 0.04,
}))
</script>

<template>
  <div class="slidev-layout oppo-cover">
    <svg class="cover-field" viewBox="0 0 160 90">
      <circle
        v-for="(d, i) in dots" :key="i"
        :cx="d.x" :cy="d.y" :r="d.r * 0.34"
        fill="var(--oppo-gold)" :opacity="d.o"
        style="animation: oppo-breathe 6s ease-in-out infinite"
        :style="{ animationDelay: `${d.d * 0.37}s` }"
      />
    </svg>
    <div class="cover-glow" />
    <div class="cover-body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.oppo-cover {
  display: flex;
  align-items: center;
  padding: 0 4.2rem;
}
.cover-field { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; }
.cover-glow {
  position: absolute;
  left: -10%; top: 20%;
  width: 70%; height: 90%;
  background: radial-gradient(closest-side, var(--g-13), transparent 70%);
  filter: blur(10px);
  pointer-events: none;
  z-index: 0;
}
.cover-body { position: relative; z-index: 2; width: 100%; }

/* the mark rail, opposite the title block */
.oppo-cover :deep(.cover-marks) {
  position: absolute;
  right: 4.2rem;
  top: 50%;
  transform: translateY(-50%);
  z-index: 3;
}
</style>
