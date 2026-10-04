<script setup lang="ts">
/**
 * Where the plan lines up: the Philippine Development Plan 2023-2028
 * carried out to the two global commitments it answers to - the ICPD
 * Programme of Action and the Sustainable Development Goals.
 *
 * step 0 - the PDP banner alone
 * step 1 - the arrow swings out and the ICPD mark lands
 * step 2 - the SDG mark lands beside it
 *
 * The PDP banner and the UN emblem are the official artwork, each carried
 * whole at its own aspect rather than cropped to fit. Only the SDG colour
 * wheel is still drawn, from the seventeen goals in their official order
 * and colours, since no file for it was to hand. Those colours are kept
 * literal, so the banner carries its own white plate in either theme: the
 * same bargain BrandLockup makes for the OPPO seal.
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number; caption?: string }>(), { step: 2 })

const globals = computed(() => props.step >= 1)
const sdg = computed(() => props.step >= 2)

/* the official banner, carried at its own aspect so nothing is cropped off it */
const PDP = { x: 16, y: 32, w: 424, h: 424 / 3.1654 }

/* The UN emblem, cropped to the mark and sized off its height; it rides
   above the SDG wordmark and beside the ICPD one, so both call sites want
   a centre point rather than a corner. */
const UN_ASPECT = 1.1792

function emblem(cx: number, cy: number, h: number) {
  const w = h * UN_ASPECT
  return { x: cx - w / 2, y: cy - h / 2, width: w, height: h }
}

const UN_ICPD = emblem(570, 100, 84)
const UN_SDG = emblem(876, 42, 58)

/* ---------- the SDG wheel ----------
   The seventeen goals, in order, as the ring reads clockwise from the top. */
const GOALS = [
  '#E5243B', '#DDA63A', '#4C9F38', '#C5192D', '#FF3A21', '#26BDE2',
  '#FCC30B', '#A21942', '#FD6925', '#DD1367', '#FD9D24', '#BF8B2E',
  '#3F7E44', '#0A97D9', '#56C02B', '#00689D', '#19486A',
]

const WHEEL_R = 25
const WHEEL_W = 9.5

const WEDGES = GOALS.map((fill, i) => {
  const span = 360 / GOALS.length
  const gap = 2.6
  const a0 = -90 + i * span + gap / 2
  const a1 = -90 + (i + 1) * span - gap / 2
  const rad = (deg: number) => (deg * Math.PI) / 180
  const ri = WHEEL_R - WHEEL_W
  const p = (r: number, deg: number) =>
    `${(Math.cos(rad(deg)) * r).toFixed(2)} ${(Math.sin(rad(deg)) * r).toFixed(2)}`
  return {
    fill,
    d: `M ${p(WHEEL_R, a0)} A ${WHEEL_R} ${WHEEL_R} 0 0 1 ${p(WHEEL_R, a1)}`
      + ` L ${p(ri, a1)} A ${ri} ${ri} 0 0 0 ${p(ri, a0)} Z`,
  }
})
</script>

<template>
  <div class="ga">
    <svg viewBox="0 0 1000 200" class="stage" role="img"
      aria-label="The Philippine Development Plan 2023-2028 aligned to the ICPD Programme of Action and the Sustainable Development Goals">

      <!-- the white plate all three marks are drawn for -->
      <rect x="0" y="0" width="1000" height="200" rx="4" class="plate" />

      <!-- ============ Philippine Development Plan 2023-2028 ============ -->
      <image href="/pdp-2023-2028.png" :x="PDP.x" :y="PDP.y" :width="PDP.w" :height="PDP.h"
        preserveAspectRatio="xMidYMid meet" />
      <rect :x="PDP.x" :y="PDP.y" :width="PDP.w" :height="PDP.h" rx="2" class="card-edge" />

      <!-- ============ the carry-across ============ -->
      <g class="reveal arrow" :class="{ on: globals }">
        <path d="M 462 91 h 28 v -12 l 24 18 -24 18 v -12 h -28 Z" fill="#2E5FA3" />
      </g>

      <!-- ============ ICPD ============ -->
      <g class="reveal icpd" :class="{ on: globals }">
        <image href="/un-emblem.png" v-bind="UN_ICPD" />
        <text x="626" y="100" class="icpd-word">ICPD</text>
        <text x="628" y="118" class="icpd-sub">International Conference on</text>
        <text x="628" y="131" class="icpd-sub">Population and Development</text>
        <text x="628" y="144" class="icpd-sub">Beyond 2014</text>
      </g>

      <!-- ============ Sustainable Development Goals ============ -->
      <g class="reveal sdg" :class="{ on: sdg }">
        <image href="/un-emblem.png" v-bind="UN_SDG" />
        <text x="794" y="110" class="sdg-word sdg-line">SUSTAINABLE</text>
        <text x="794" y="134" class="sdg-word sdg-line">DEVELOPMENT</text>
        <text x="794" y="178" class="sdg-word sdg-goals">G</text>
        <g transform="translate(847 163) scale(0.88)">
          <path v-for="(w, i) in WEDGES" :key="i" :d="w.d" :fill="w.fill" />
        </g>
        <text x="871" y="178" class="sdg-word sdg-goals">ALS</text>
      </g>
    </svg>

    <div v-if="caption" class="cap">{{ caption }}</div>
  </div>
</template>

<style scoped>
.ga { display: flex; flex-direction: column; align-items: center; gap: 0.7rem; width: 100%; }
.stage { width: 100%; height: auto; display: block; }

/* the marks are drawn for paper, so the banner brings its own */
.plate { fill: #ffffff; }
.card-edge { fill: none; stroke: rgba(46, 95, 163, 0.16); stroke-width: 1; }

/* ---- wordmarks ----
   Sizes live here rather than on the elements, because UnoCSS attributify
   claims the font-size attribute: it rewrites a 47 there into 11.75rem and
   bursts the text clean out of the plate. The deck's other SVG components
   size their text through classes for the same reason. */
.icpd-word { font-size: 47px; font-weight: 800; fill: #3C3C3B; letter-spacing: -0.5px; }
.icpd-sub { font-size: 9.5px; fill: #58585A; font-weight: 400; }
.sdg-word { font-weight: 800; fill: #00558F; letter-spacing: -0.4px; }
.sdg-line { font-size: 23px; }
.sdg-goals { font-size: 40px; }

/* ---- reveal ---- */
.reveal { opacity: 0; transition: opacity 520ms ease, transform 560ms cubic-bezier(.34, 1.3, .5, 1); }
.arrow { transform: translateX(-16px); }
.icpd, .sdg { transform: translateX(22px); }
.reveal.on { opacity: 1; transform: none; }
.icpd.on { transition-delay: 160ms; }
.sdg.on { transition-delay: 60ms; }

.cap {
  font-size: 0.74rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--oppo-ink-3);
  font-weight: 600;
  text-align: center;
}

@media (prefers-reduced-motion: reduce) {
  .reveal { transition-duration: 1ms; transform: none; }
}
</style>
