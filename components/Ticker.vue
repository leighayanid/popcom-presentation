<script setup lang="ts">
import { onUnmounted, ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  to: number
  dur?: number
  active?: boolean
  decimals?: number
  prefix?: string
  suffix?: string
}>(), { dur: 1200, active: true, decimals: 0, prefix: '', suffix: '' })

const shown = ref(0)
let raf = 0

function stop() {
  if (typeof cancelAnimationFrame !== 'undefined') cancelAnimationFrame(raf)
}

function run() {
  stop()
  if (typeof requestAnimationFrame === 'undefined') { shown.value = props.to; return }
  const from = shown.value
  const t0 = performance.now()
  const tick = (t: number) => {
    const k = Math.min(1, (t - t0) / props.dur)
    const e = 1 - (1 - k) ** 3
    shown.value = from + (props.to - from) * e
    if (k < 1) raf = requestAnimationFrame(tick)
  }
  raf = requestAnimationFrame(tick)
}

watch(() => [props.active, props.to], ([a]) => {
  if (a) run()
  else { stop(); shown.value = 0 }
}, { immediate: true })

onUnmounted(stop)
</script>

<template>
  <span class="tnum">{{ prefix }}{{ shown.toLocaleString('en-US', {
    minimumFractionDigits: decimals, maximumFractionDigits: decimals,
  }) }}{{ suffix }}</span>
</template>
