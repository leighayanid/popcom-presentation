<script setup lang="ts">
defineProps<{ num?: string }>()
</script>

<template>
  <div class="slidev-layout oppo-section">
    <div class="rule-sweep" />
    <div class="section-num" v-if="num">{{ num }}</div>
    <div class="section-body"><slot /></div>
  </div>
</template>

<style scoped>
.oppo-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 4.2rem;
}
.section-num {
  font-size: 7.5rem;
  font-weight: 800;
  line-height: 0.85;
  letter-spacing: -0.05em;
  color: transparent;
  -webkit-text-stroke: 1.5px var(--g-45);
  margin-bottom: 0.6rem;
}
.section-body :deep(h1) { font-size: 3rem; }
.rule-sweep {
  position: absolute;
  left: 0; top: 50%;
  height: 1px; width: 100%;
  background: linear-gradient(to right, transparent, var(--g-35), transparent);
  animation: sweep 7s ease-in-out infinite;
}
@keyframes sweep {
  0%, 100% { transform: translateY(-120px); opacity: 0.25; }
  50%      { transform: translateY(120px); opacity: 0.7; }
}
</style>
