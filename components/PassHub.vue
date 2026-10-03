<script setup lang="ts">
/**
 * The Bataeno Pass as infrastructure: a service side (the identified use cases
 * it carries) and a data side (the registry it standardises). The ring pulses
 * continuously because registration and tapping are continuous.
 *
 * step 1 - the use cases it serves
 * step 2 - the registry it builds
 * step 3 - who owns what
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const shown = (at: number) => props.step >= at

const CX = 300
const CY = 212
const R = 158

const USES = [
  'School Implementation',
  'Libreng Sakay',
  'Social Services',
  'READI',
  'Bataan Jobs',
  'Iskolar ng Bataan',
  'BHSS',
  'EduChild',
].map((label, i, a) => {
  const deg = -90 + (360 / a.length) * i
  const rad = deg * Math.PI / 180
  const x = CX + Math.cos(rad) * R
  const y = CY + Math.sin(rad) * R
  const cos = Math.cos(rad)
  return {
    label, i, x, y,
    lx: x + cos * 16,
    ly: y + Math.sin(rad) * 10 + (Math.abs(cos) < 0.25 ? (Math.sin(rad) > 0 ? 14 : -10) : 3.5),
    anchor: Math.abs(cos) < 0.25 ? 'middle' : (cos > 0 ? 'start' : 'end'),
  }
})

const DATA_POINTS = [
  'A standardised citizen registry',
  'Verified, barangay-disaggregated information',
  'A system for capturing and organising it',
  'May support future human-development analysis',
]
</script>

<template>
  <div class="ph">
    <svg viewBox="0 0 1000 400" class="stage" role="img"
      aria-label="The Bataeno Pass as service infrastructure for provincial use cases and as a standardised citizen registry">
      <defs>
        <linearGradient id="ph-sheen" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="var(--oppo-gold)" stop-opacity="0" />
          <stop offset="50%" stop-color="var(--oppo-gold)" stop-opacity="0.5" />
          <stop offset="100%" stop-color="var(--oppo-gold)" stop-opacity="0" />
        </linearGradient>
        <clipPath id="ph-clip"><rect x="-70" y="-44" width="140" height="88" rx="9" /></clipPath>
        <filter id="ph-glow" x="-70%" y="-70%" width="240%" height="240%">
          <feGaussianBlur stdDeviation="5" result="b" />
          <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>

      <!-- ===== SERVICE: the ring of use cases ===== -->
      <g class="halo" :class="{ on: shown(1) }">
        <circle :cx="CX" :cy="CY" :r="R" fill="none" stroke="var(--g-16)" stroke-width="1" />
        <circle :cx="CX" :cy="CY" :r="R" fill="none" stroke="var(--oppo-gold)" stroke-width="1.6"
          stroke-dasharray="26 992" class="runner" />
        <line v-for="u in USES" :key="'l' + u.i" :x1="CX" :y1="CY" :x2="u.x" :y2="u.y"
          stroke="var(--g-20)" stroke-width="1" class="spoke"
          :style="{ transitionDelay: (u.i * 70) + 'ms' }" />
        <template v-if="shown(1)">
          <circle v-for="u in USES" :key="'p' + u.i" r="2.4" fill="var(--oppo-gold)" opacity="0">
            <animate attributeName="cx" :values="CX + ';' + u.x" dur="2.6s"
              repeatCount="indefinite" :begin="(u.i * 0.32) + 's'" />
            <animate attributeName="cy" :values="CY + ';' + u.y" dur="2.6s"
              repeatCount="indefinite" :begin="(u.i * 0.32) + 's'" />
            <animate attributeName="opacity" values="0;1;1;0" dur="2.6s"
              repeatCount="indefinite" :begin="(u.i * 0.32) + 's'" />
          </circle>
        </template>
        <g v-for="u in USES" :key="'n' + u.i" class="use" :style="{ transitionDelay: (120 + u.i * 70) + 'ms' }">
          <circle :cx="u.x" :cy="u.y" r="7.5" fill="var(--oppo-bg-2)" stroke="var(--oppo-gold)" stroke-width="1.3" />
          <circle :cx="u.x" :cy="u.y" r="3" fill="var(--oppo-gold)" />
          <text :x="u.lx" :y="u.ly" :text-anchor="u.anchor" class="use-t">{{ u.label }}</text>
        </g>
        <text x="28" y="22" class="side-k">SERVICE &#183; IDENTIFIED USE CASES</text>
      </g>

      <!-- ===== the Pass itself ===== -->
      <g :transform="'translate(' + CX + ' ' + CY + ')'">
      <g filter="url(#ph-glow)" class="card-g">
        <rect x="-70" y="-44" width="140" height="88" rx="9" fill="var(--oppo-bg-2)"
          stroke="var(--oppo-gold)" stroke-width="1.6" />
        <rect x="-58" y="-32" width="34" height="28" rx="4" fill="var(--oppo-gold-fig)" opacity="0.9" />
        <circle cx="-41" cy="-22" r="5" fill="var(--oppo-panel-2)" />
        <path d="M -50 -8 C -50 -16, -32 -16, -32 -8 Z" fill="var(--oppo-panel-2)" />
        <line x1="-14" y1="-28" x2="58" y2="-28" stroke="var(--oppo-ink-1)" stroke-width="2" />
        <line x1="-14" y1="-18" x2="42" y2="-18" stroke="var(--oppo-ink-3)" stroke-width="2" />
        <line x1="-14" y1="-8" x2="50" y2="-8" stroke="var(--oppo-ink-3)" stroke-width="2" />
        <text x="-58" y="18" class="card-t">BATAE&#209;O PASS</text>
        <text x="-58" y="32" class="card-s">PROVINCIAL PERSONAL DATA CARD</text>
        <g clip-path="url(#ph-clip)">
          <rect class="sheen" x="-70" y="-44" width="40" height="88" fill="url(#ph-sheen)" />
        </g>
      </g>
      </g>

      <!-- ===== DATA: the registry ===== -->
      <g class="data" :class="{ on: shown(2) }">
        <line x1="620" y1="14" x2="620" y2="386" stroke="var(--h-14)" stroke-width="1" />
        <text x="660" y="22" class="side-k">DATA &#183; CITIZEN REGISTRY</text>

        <!-- databank glyph -->
        <g transform="translate(700 110)" stroke="var(--s3)" stroke-width="1.6" fill="none">
          <ellipse cx="0" cy="-20" rx="26" ry="9" />
          <path d="M -26 -20 V 18 A 26 9 0 0 0 26 18 V -20" />
          <path d="M -26 -7 A 26 9 0 0 0 26 -7" opacity="0.55" />
          <path d="M -26 5 A 26 9 0 0 0 26 5" opacity="0.55" />
        </g>
        <template v-if="shown(2)">
          <circle v-for="k in 3" :key="k" r="2.4" fill="var(--s3)" cx="700">
            <animate attributeName="cy" values="50;86" dur="1.8s"
              repeatCount="indefinite" :begin="((k - 1) * 0.6) + 's'" />
            <animate attributeName="opacity" values="0;1;1;0" dur="1.8s"
              repeatCount="indefinite" :begin="((k - 1) * 0.6) + 's'" />
          </circle>
        </template>

        <g v-for="(d, i) in DATA_POINTS" :key="i" class="dp" :style="{ transitionDelay: (i * 110) + 'ms' }">
          <circle cx="672" :cy="190 + i * 44" r="3" fill="var(--oppo-gold)" />
          <text x="688" :y="194 + i * 44" class="dp-t">{{ d }}</text>
        </g>
      </g>

    </svg>

    <div class="own" :class="{ on: shown(3) }">
      <span class="oppo-tag">Who does what</span>
      <span>The respective provincial offices remain responsible for implementing and delivering
        their programmes and services. The Bataeño Pass provides the system and citizen registry
        infrastructure that supports their use cases.</span>
    </div>
  </div>
</template>

<style scoped>
.ph { width: 100%; display: flex; flex-direction: column; gap: 0.5rem; }
.stage { width: 100%; height: auto; }

.halo, .data { opacity: 0; transition: opacity 600ms ease; }
.halo.on, .data.on { opacity: 1; }
.own {
  display: flex; align-items: center; gap: 0.8rem;
  font-size: 0.8rem; line-height: 1.4; color: var(--oppo-ink-2);
  opacity: 0; transform: translateY(8px);
  transition: opacity 520ms ease, transform 520ms ease;
}
.own.on { opacity: 1; transform: translateY(0); }
.own .oppo-tag { flex: none; }

.runner { animation: runner 6s linear infinite; transform-box: fill-box; transform-origin: center; }
@keyframes runner { to { stroke-dashoffset: -1018; } }

.spoke { stroke-dasharray: 170; stroke-dashoffset: 170; transition: stroke-dashoffset 620ms ease; }
.halo.on .spoke { stroke-dashoffset: 0; }

.use { opacity: 0; transform: scale(0.4); transform-box: fill-box; transform-origin: center;
  transition: opacity 440ms ease, transform 560ms cubic-bezier(.34,1.5,.5,1); }
.halo.on .use { opacity: 1; transform: scale(1); }
.use-t { font-size: 10px; font-weight: 650; fill: var(--oppo-ink-1); }

.side-k { font-size: 8.5px; font-weight: 750; letter-spacing: 0.22em; fill: var(--oppo-ink-3); }

.card-g { animation: card-float 6s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes card-float {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-4px); }
}
.card-t { font-size: 11px; font-weight: 800; letter-spacing: 0.09em; fill: var(--oppo-gold); }
.card-s { font-size: 6.5px; font-weight: 650; letter-spacing: 0.1em; fill: var(--oppo-ink-3); }
.sheen { animation: oppo-sheen 5.2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }

.dp { opacity: 0; transform: translateX(14px); transform-box: view-box;
  transition: opacity 460ms ease, transform 520ms ease; }
.data.on .dp { opacity: 1; transform: translateX(0); }
.dp-t { font-size: 11px; font-weight: 600; fill: var(--oppo-ink-1); }

</style>
