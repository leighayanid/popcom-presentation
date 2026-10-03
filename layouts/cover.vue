<script setup lang="ts">
/**
 * Cover: a handful of slow-breathing citizen dots.
 *
 * Placed by hand rather than generated, so they sit in the margins the title
 * block and the mark rail leave empty instead of scattering across the words.
 * x/y are viewBox units (160 x 90); o is opacity, d seeds the breathe delay.
 */
const dots = [
  { x: 24, y: 13, r: 1.5, o: 0.26, d: 0 },
  { x: 58, y: 8, r: 1.0, o: 0.16, d: 3 },
  { x: 97, y: 19, r: 1.8, o: 0.22, d: 6 },
  { x: 88, y: 47, r: 1.1, o: 0.14, d: 2 },
  { x: 113, y: 71, r: 1.6, o: 0.2, d: 8 },
  { x: 142, y: 81, r: 1.0, o: 0.13, d: 5 },
  { x: 19, y: 80, r: 1.3, o: 0.18, d: 10 },
]
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
