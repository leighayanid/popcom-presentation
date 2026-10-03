<script setup lang="ts">
/**
 * The HDI++ framework of House Bill No. 6145 as the Province is operationalising it.
 * Four dimensions, each with the proxy indicator and the data input behind it,
 * feeding one composite index. The emblems are iconic, not gauges - no index
 * values are published yet, so none are drawn.
 *
 * step 1 - the four dimensions
 * step 2 - proxy indicator and data input
 * step 3 - they feed the composite
 * step 4 - which of them this Office supplies
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const DIMS = [
  {
    key: 'health', x: 150, name: 'LIFE EXPECTANCY', color: 'var(--s3)',
    proxy: 'Age-Weighted Death Score (AWDS)',
    input: 'Monthly LCR death data — age, residence, cause',
    oppo: 'OPPO supplies the data input',
  },
  {
    key: 'educ', x: 383, name: 'EDUCATION', color: 'var(--s2)',
    proxy: 'Numeracy and Literacy Rate',
    input: 'School-based systems · Bataeño Pass registration',
    oppo: 'OPPO supplies registry and system support',
  },
  {
    key: 'living', x: 616, name: 'STANDARD OF LIVING', color: 'var(--s1)',
    proxy: 'Average Monthly Residential kWh per Household',
    input: 'Electric cooperative data + lifeline rate',
    oppo: 'OPPO works the household side',
  },
  {
    key: 'peace', x: 849, name: 'PEACE & ORDER', color: 'var(--s5)',
    proxy: 'Consummated and non-consummated crimes / CIRAS',
    input: 'Law enforcement records',
    oppo: '',
  },
]

const dimsIn = computed(() => props.step >= 1)
const labelled = computed(() => props.step >= 2)
const feeding = computed(() => props.step >= 3)
const credited = computed(() => props.step >= 4)

const CY = 236
const CX = 500
const HY = 92
</script>

<template>
  <div class="hdi">
    <svg viewBox="0 0 1000 322" class="stage" role="img"
      aria-label="The four HDI++ dimensions feeding one composite index">
      <defs>
        <filter id="hdi-glow" x="-70%" y="-70%" width="240%" height="240%">
          <feGaussianBlur stdDeviation="4" result="b" />
          <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
        <path v-for="d in DIMS" :key="'p' + d.key" :id="'hdi-f-' + d.key"
          :d="'M ' + d.x + ' ' + (CY - 46) + ' C ' + d.x + ' ' + (CY - 120) + ', ' + CX + ' ' + (HY + 118) + ', ' + CX + ' ' + (HY + 46)" />
      </defs>

      <!-- feed lines -->
      <g v-for="d in DIMS" :key="'l' + d.key" class="feed" :class="{ on: feeding }"
        :style="{ transitionDelay: (DIMS.indexOf(d) * 110) + 'ms' }">
        <use :href="'#hdi-f-' + d.key" fill="none" stroke="var(--g-28)" stroke-width="1.2" />
        <template v-if="feeding">
          <circle r="3" :fill="d.color" opacity="0">
            <animateMotion dur="2.4s" repeatCount="indefinite" :begin="(DIMS.indexOf(d) * 0.4) + 's'">
              <mpath :href="'#hdi-f-' + d.key" />
            </animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="2.4s"
              repeatCount="indefinite" :begin="(DIMS.indexOf(d) * 0.4) + 's'" />
          </circle>
        </template>
      </g>

      <!-- composite -->
      <g class="comp" :class="{ live: feeding }" :transform="'translate(' + CX + ' ' + HY + ')'"
        filter="url(#hdi-glow)">
        <path d="M 0 -48 L 41.6 -24 L 41.6 24 L 0 48 L -41.6 24 L -41.6 -24 Z"
          fill="var(--oppo-panel-2)" stroke="var(--oppo-gold)" stroke-width="1.6" />
        <path class="comp-ring" d="M 0 -48 L 41.6 -24 L 41.6 24 L 0 48 L -41.6 24 L -41.6 -24 Z"
          fill="none" stroke="var(--oppo-gold)" stroke-width="1.2" />
        <text y="-2" text-anchor="middle" class="comp-t">HDI<tspan class="comp-pp">++</tspan></text>
        <text y="16" text-anchor="middle" class="comp-s">COMPOSITE</text>
      </g>
      <text :x="CX" y="16" text-anchor="middle" class="comp-cap">
        Modified Human Development Index &#183; House Bill No. 6145
      </text>
      <text :x="CX" y="30" text-anchor="middle" class="comp-cap2">
        comparable from barangay to municipality to province
      </text>

      <!-- dimensions -->
      <g v-for="(d, i) in DIMS" :key="d.key" class="dim" :class="{ on: dimsIn }"
        :style="{ transitionDelay: (i * 120) + 'ms' }">
        <g :transform="'translate(' + d.x + ' ' + CY + ')'">
          <circle r="46" fill="var(--oppo-panel-2)" :stroke="d.color" stroke-width="1.6" opacity="0.95" />
          <circle class="orbit" r="52" fill="none" :stroke="d.color" stroke-width="1"
            stroke-dasharray="4 9" opacity="0.5" :style="{ animationDelay: (i * 0.7) + 's' }" />

          <!-- emblems -->
          <g v-if="d.key === 'health'" :stroke="d.color" stroke-width="2.2" fill="none"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M -22 0 H -12 L -7 -13 L 1 14 L 7 0 H 22" class="ecg" />
          </g>
          <g v-else-if="d.key === 'educ'" :stroke="d.color" stroke-width="2" fill="none"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M 0 -11 C -5 -16, -14 -16, -19 -14 V 11 C -14 9, -5 9, 0 14" />
            <path d="M 0 -11 C 5 -16, 14 -16, 19 -14 V 11 C 14 9, 5 9, 0 14" />
            <path d="M 0 -11 V 14" />
          </g>
          <g v-else-if="d.key === 'living'" :stroke="d.color" stroke-width="2" fill="none"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M -9 3 A 9 9 0 1 1 9 3 C 9 8, 5 9, 5 14 H -5 C -5 9, -9 8, -9 3 Z" />
            <path d="M -4 18 H 4" />
            <path d="M 0 -4 L -3 2 H 3 L 0 8" :stroke="d.color" stroke-width="1.4" class="spark" />
          </g>
          <g v-else :stroke="d.color" stroke-width="2" fill="none"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M 0 -16 L 15 -10 V 3 C 15 12, 8 17, 0 20 C -8 17, -15 12, -15 3 V -10 Z" />
            <path d="M -6 2 L -1 7 L 7 -4" stroke-width="2.2" />
          </g>

          <!-- OPPO credit -->
          <g class="credit" :class="{ on: credited && d.oppo }" transform="translate(32 -32)">
            <circle r="12" fill="var(--oppo-bg-1)" stroke="var(--oppo-gold)" stroke-width="1.3" />
            <circle r="12" fill="none" stroke="var(--oppo-gold)" stroke-width="1" class="credit-ping" />
            <text y="4" text-anchor="middle" class="credit-t">OPPO</text>
          </g>
        </g>

        <text :x="d.x" :y="CY + 68" text-anchor="middle" class="dim-n">{{ d.name }}</text>
      </g>
    </svg>

    <div class="grid">
      <div v-for="(d, i) in DIMS" :key="d.key" class="cell"
        :class="{ on: labelled, dimmed: credited && !d.oppo }"
        :style="{ transitionDelay: (i * 110) + 'ms', '--c': d.color }">
        <div class="cell-k">PROXY INDICATOR</div>
        <div class="cell-p">{{ d.proxy }}</div>
        <div class="cell-k">DATA INPUT</div>
        <div class="cell-i">{{ d.input }}</div>
        <div class="cell-o" :class="{ on: credited }">
          {{ d.oppo || 'Led by other provincial offices' }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hdi { width: 100%; display: flex; flex-direction: column; gap: 0.5rem; }
.stage { width: 100%; height: auto; }

.comp { opacity: 0.4; transition: opacity 700ms ease; }
.comp.live { opacity: 1; }
.comp-ring { animation: comp-ping 3s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes comp-ping {
  0%   { transform: scale(1); opacity: 0.7; }
  100% { transform: scale(1.5); opacity: 0; }
}
.comp-t { font-size: 23px; font-weight: 800; letter-spacing: 0.04em; fill: var(--oppo-ink); }
.comp-pp { fill: var(--oppo-gold); }
.comp-s { font-size: 9px; font-weight: 700; letter-spacing: 0.24em; fill: var(--oppo-ink-2); }
.comp-cap { font-size: 12px; font-weight: 600; fill: var(--oppo-ink-2); letter-spacing: 0.04em; }
.comp-cap2 { font-size: 11px; fill: var(--oppo-ink-2); letter-spacing: 0.04em; }

.dim { opacity: 0; transform: translateY(22px); transform-box: view-box;
  transition: opacity 560ms ease, transform 660ms cubic-bezier(.22,1,.36,1); }
.dim.on { opacity: 1; transform: translateY(0); }
.dim-n { font-size: 12.5px; font-weight: 750; letter-spacing: 0.14em; fill: var(--oppo-ink); }

.orbit { animation: oppo-spin 22s linear infinite; transform-box: fill-box; transform-origin: center; }
.ecg { stroke-dasharray: 74; animation: ecg 2.6s ease-in-out infinite; }
@keyframes ecg {
  0%   { stroke-dashoffset: 74; }
  55%  { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -74; }
}
.spark { animation: oppo-breathe 1.8s ease-in-out infinite; }

.feed { opacity: 0; transition: opacity 600ms ease; }
.feed.on { opacity: 1; }

.credit { opacity: 0; transition: opacity 460ms ease; }
.credit.on { opacity: 1; }
.credit-t { font-size: 8.5px; font-weight: 800; letter-spacing: 0.06em; fill: var(--oppo-gold); }
.credit-ping { animation: chip-ping2 2.6s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes chip-ping2 {
  0%   { transform: scale(1); opacity: 0.75; }
  100% { transform: scale(2); opacity: 0; }
}

.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.7rem; }
.cell {
  border-top: 2px solid var(--c);
  padding-top: 0.42rem;
  opacity: 0; transform: translateY(10px);
  transition: opacity 500ms ease, transform 500ms ease, filter 500ms ease;
}
.cell.on { opacity: 1; transform: translateY(0); }
.cell.dimmed { opacity: 0.42; filter: saturate(0.4); }
.cell-k { font-size: 0.74rem; font-weight: 750; letter-spacing: 0.18em; color: var(--oppo-ink-2); margin-top: 0.25rem; }
.cell-p { font-size: 0.95rem; font-weight: 650; color: var(--oppo-ink); line-height: 1.3; }
.cell-i { font-size: 0.88rem; color: var(--oppo-ink-2); line-height: 1.3; }
.cell-o {
  font-size: 0.85rem; font-weight: 650; color: var(--oppo-gold); margin-top: 0.3rem;
  opacity: 0; transition: opacity 460ms ease 200ms;
}
.cell-o.on { opacity: 1; }
.cell.dimmed .cell-o { color: var(--oppo-ink-3); }
</style>
