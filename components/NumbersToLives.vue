<script setup lang="ts">
/**
 * Signature figure: a field of bare digits ripples outward into human figures.
 * step 0 — the headcount: anonymous digits
 * step 1 — the morph: digits dissolve into people, centre-out
 * step 2 — the point: a heartbeat lights the field, "TAO ANG PUSO NG PAG-UNLAD"
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const COLS = 20
const ROWS = 8
const CW = 50
const CH = 50
const W = COLS * CW
const H = ROWS * CH

// deterministic pseudo-random so the field is identical on every render
function rnd(i: number, salt: number) {
  const x = Math.sin(i * 12.9898 + salt * 78.233) * 43758.5453
  return x - Math.floor(x)
}

const cells = computed(() => {
  const cx = (COLS - 1) / 2
  const cy = (ROWS - 1) / 2
  const maxD = Math.hypot(cx, cy)
  const out = []
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const i = r * COLS + c
      const d = Math.hypot(c - cx, r - cy) / maxD
      out.push({
        i,
        x: c * CW + CW / 2,
        y: r * CH + CH / 2,
        digit: Math.floor(rnd(i, 1) * 10),
        // centre-out ripple, with a little jitter so it never looks mechanical
        delay: d * 900 + rnd(i, 2) * 160,
        bob: 2.6 + rnd(i, 3) * 1.8,
        bobDelay: rnd(i, 4) * 3,
        d,
        lit: rnd(i, 5) > 0.72,
      })
    }
  }
  return out
})

const morphed = computed(() => props.step >= 1)
const alive = computed(() => props.step >= 2)
</script>

<template>
  <div class="n2l">
    <svg :viewBox="`0 0 ${W} ${H}`" class="field" role="img"
      aria-label="A field of digits transforming into human figures">
      <defs>
        <radialGradient id="n2l-warm" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="var(--oppo-gold-fig)" stop-opacity="0.95" />
          <stop offset="100%" stop-color="var(--s1)" stop-opacity="0.75" />
        </radialGradient>
        <filter id="n2l-glow" x="-60%" y="-60%" width="220%" height="220%">
          <feGaussianBlur stdDeviation="5" result="b" />
          <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>

      <g v-for="c in cells" :key="c.i" :transform="`translate(${c.x} ${c.y})`">
        <!-- the number -->
        <text
          class="glyph digit" text-anchor="middle" dominant-baseline="central"
          :style="{ opacity: morphed ? 0 : 0.42 - c.d * 0.16, transitionDelay: `${c.delay}ms` }"
        >{{ c.digit }}</text>

        <!-- the person -->
        <g
          class="glyph person"
          :style="{
            opacity: morphed ? (alive && c.lit ? 1 : 0.55 - c.d * 0.2) : 0,
            transitionDelay: `${c.delay}ms`,
            animationDuration: `${c.bob}s`,
            animationDelay: `${c.bobDelay}s`,
          }"
          :fill="alive && c.lit ? 'url(#n2l-warm)' : 'var(--oppo-ink-2)'"
        >
          <circle cx="0" cy="-8.5" r="4.6" />
          <path d="M -7.4 11 C -7.4 1.6 -4 -1.4 0 -1.4 C 4 -1.4 7.4 1.6 7.4 11 Z" />
        </g>
      </g>

      <!-- heartbeat at the centre of the field -->
      <g v-if="alive" :transform="`translate(${W / 2} ${H / 2})`" filter="url(#n2l-glow)">
        <g class="heart">
          <circle r="34" fill="var(--oppo-bg-1)" opacity="0.92" />
          <circle r="34" fill="none" stroke="var(--oppo-gold)" stroke-width="1.2" opacity="0.45" />
          <path
            d="M 0 15 C -20 2 -18.5 -13 -8.3 -13 C -3.2 -13 0 -8.8 0 -5.5 C 0 -8.8 3.2 -13 8.3 -13 C 18.5 -13 20 2 0 15 Z"
            fill="var(--oppo-gold-fig)" />
        </g>
      </g>
    </svg>

    <div class="captions">
      <span class="cap from" :class="{ off: morphed }">HUMAN NUMBERS</span>
      <svg class="arrow" viewBox="0 0 60 16" :class="{ on: morphed }">
        <path d="M 2 8 H 50" stroke="var(--oppo-gold)" stroke-width="1.6" fill="none" stroke-linecap="round" />
        <path d="M 44 3 L 52 8 L 44 13" stroke="var(--oppo-gold)" stroke-width="1.6" fill="none"
          stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <span class="cap to" :class="{ on: morphed }">HUMAN LIVES</span>
    </div>
  </div>
</template>

<style scoped>
.n2l { width: 100%; display: flex; flex-direction: column; gap: 0.5rem; }
.field { width: 100%; height: auto; }

.glyph {
  transition: opacity 620ms cubic-bezier(0.22, 1, 0.36, 1), fill 700ms ease;
}
.digit {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 19px;
  font-weight: 500;
  fill: var(--oppo-ink-3);
}
.person { animation: oppo-bob ease-in-out infinite; transform-box: fill-box; transform-origin: center; }

.heart { animation: oppo-heartbeat 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }

.captions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.4rem;
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.2em;
}
.cap { transition: color 700ms ease, opacity 700ms ease, filter 700ms ease; }
.cap.from { color: var(--oppo-ink-3); }
.cap.from.off { color: var(--oppo-ink-4); filter: blur(0.4px); }
.cap.to { color: var(--oppo-ink-5); opacity: 0.5; }
.cap.to.on { color: var(--oppo-gold); opacity: 1; }
.arrow { width: 60px; opacity: 0.15; transition: opacity 700ms ease 300ms; }
.arrow.on { opacity: 1; }
</style>
