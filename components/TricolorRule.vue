<script setup lang="ts">
/**
 * The divider under each cover line: a hairline either side of the Bataan
 * tricolour.
 *
 * The flag block is a fixed 192px across whatever the rule's total span, so
 * the two hairlines absorb the difference — which is how the printed cover
 * does it, where the second rule is wider than the first but the colours sit
 * at the same size directly under one another.
 */
withDefaults(defineProps<{ width?: number }>(), { width: 560 })
</script>

<template>
  <div class="tricolour" :style="{ width: `${width}px` }">
    <span class="hair" />
    <span class="bar blue" />
    <span class="bar gold" />
    <span class="bar red" />
    <span class="hair" />
  </div>
</template>

<style scoped>
.tricolour {
  display: flex;
  align-items: center;
  height: 11.4px;
}
.hair {
  flex: 1;
  height: 1.7px;
  background: #2b3a66;
}
.bar {
  width: 64.1px;
  height: 11.4px;
}
.blue { background: #0a71e0; }
.gold { background: #ffc02e; }
.red { background: #e9142f; }
</style>
