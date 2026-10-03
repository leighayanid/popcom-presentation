<template>
  <div class="slidev-layout oppo-statement">
    <div class="halo" />
    <div class="body"><slot /></div>
  </div>
</template>

<style scoped>
.oppo-statement {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.halo {
  position: absolute;
  inset: 0;
  background: radial-gradient(45% 45% at 50% 50%, var(--g-13), transparent 70%);
  animation: oppo-breathe 7s ease-in-out infinite;
  pointer-events: none;
}
.body { position: relative; z-index: 2; max-width: 62rem; }
</style>
