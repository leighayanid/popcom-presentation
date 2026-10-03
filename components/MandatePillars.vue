<script setup lang="ts">
/**
 * The legal mandate drawn as a classical order:
 * the Local Government Code is the plinth, the four mandated
 * functions are the columns, OPPO is the entablature they carry.
 */
import { computed } from 'vue'
const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const PILLARS = [
  { key: 'integrate', title: 'INTEGRATE', body: 'POPDEV principles into provincial policies, strategies and development plans', color: 'var(--s2)' },
  { key: 'promote', title: 'PROMOTE', body: 'Responsible parenthood and family well-being', color: 'var(--s3)' },
  { key: 'build', title: 'IMPLEMENT', body: 'Localized and responsive capacity-building initiatives', color: 'var(--s1)' },
  { key: 'maintain', title: 'MAINTAIN', body: 'A comprehensive population databank for evidence-based planning', color: 'var(--s5)' },
]

const risen = computed(() => props.step >= 1)
const crowned = computed(() => props.step >= 2)
const flowing = computed(() => props.step >= 3)

// column geometry inside a 1000 x 300 stage
const COL_W = 74
const GAP = 108
const START = 500 - ((COL_W * 4 + GAP * 3) / 2)
const xOf = (i: number) => START + i * (COL_W + GAP)
</script>

<template>
  <div class="mp">
    <svg viewBox="0 0 1000 366" class="temple" role="img"
      aria-label="Four mandate columns carrying the Office of the Provincial Population Officer">
      <defs>
        <linearGradient id="mp-stone" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="var(--oppo-bg-3)" />
          <stop offset="45%" stop-color="var(--oppo-bg-3)" />
          <stop offset="100%" stop-color="var(--oppo-bg-2)" />
        </linearGradient>
        <linearGradient id="mp-gold" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="var(--oppo-gold-dim)" />
          <stop offset="50%" stop-color="var(--oppo-gold)" />
          <stop offset="100%" stop-color="var(--oppo-gold-dim)" />
        </linearGradient>
      </defs>

      <!-- entablature: OPPO -->
      <g class="crown" :class="{ on: crowned }">
        <rect x="150" y="30" width="700" height="46" rx="6" fill="var(--oppo-bg-2)" stroke="url(#mp-gold)" stroke-width="1.4" />
        <rect x="134" y="18" width="732" height="14" rx="4" fill="var(--oppo-bg-3)" stroke="var(--g-35)" stroke-width="1" />
        <text x="500" y="58" text-anchor="middle" class="crown-label">
          OFFICE OF THE PROVINCIAL POPULATION OFFICER
        </text>
      </g>

      <!-- columns -->
      <g v-for="(p, i) in PILLARS" :key="p.key">
        <g class="col" :class="{ on: risen }" :style="{ transitionDelay: `${160 + i * 130}ms` }">
          <!-- capital -->
          <rect :x="xOf(i) - 8" y="82" :width="COL_W + 16" height="12" rx="3" fill="var(--oppo-bg-3)"
            stroke="var(--h-22)" stroke-width="0.8" />
          <!-- shaft -->
          <rect :x="xOf(i)" y="94" :width="COL_W" height="172" fill="var(--oppo-shaft)"
            stroke="var(--h-18)" stroke-width="0.8" />
          <!-- fluting -->
          <line v-for="f in 3" :key="f" :x1="xOf(i) + f * (COL_W / 4)" y1="98"
            :x2="xOf(i) + f * (COL_W / 4)" y2="262" stroke="var(--h-10)" stroke-width="1" />
          <!-- the function this column carries, lit from inside -->
          <rect :x="xOf(i) + 6" y="104" :width="COL_W - 12" height="152" rx="3"
            :fill="p.color" class="core" :class="{ flow: flowing }"
            :style="{ animationDelay: `${i * 0.45}s` }" />
          <!-- base -->
          <rect :x="xOf(i) - 10" y="266" :width="COL_W + 20" height="14" rx="3" fill="var(--oppo-bg-3)"
            stroke="var(--h-22)" stroke-width="0.8" />
          <text :x="xOf(i) + COL_W / 2" y="184" text-anchor="middle" class="col-label"
            :transform="`rotate(-90 ${xOf(i) + COL_W / 2} 184)`">{{ p.title }}</text>
        </g>
      </g>

      <!-- plinth: the Local Government Code -->
      <g class="plinth">
        <rect x="120" y="284" width="760" height="40" rx="5" fill="var(--oppo-panel-2)"
          stroke="var(--g-30)" stroke-width="1.2" />
        <rect x="104" y="324" width="792" height="12" rx="4" fill="var(--oppo-bg-1)"
          stroke="var(--h-16)" stroke-width="0.8" />
        <text x="500" y="310" text-anchor="middle" class="plinth-label">
          LOCAL GOVERNMENT CODE OF 1991 &#183; REPUBLIC ACT NO. 7160
        </text>
      </g>
    </svg>

    <div class="legend">
      <div v-for="(p, i) in PILLARS" :key="p.key" class="leg"
        :class="{ on: risen }" :style="{ transitionDelay: `${320 + i * 130}ms` }">
        <span class="swatch" :style="{ background: p.color }" />
        <div>
          <div class="leg-t">{{ p.title }}</div>
          <div class="leg-b">{{ p.body }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mp { width: 100%; display: flex; flex-direction: column; gap: 0.9rem; }
.temple { width: 100%; height: auto; }

.col {
  opacity: 0;
  transform: translateY(46px);
  transition: opacity 620ms cubic-bezier(.22,1,.36,1), transform 760ms cubic-bezier(.34,1.3,.5,1);
}
.col.on { opacity: 1; transform: translateY(0); }

.core { opacity: 0.2; }
.core.flow { animation: core-lift 3.6s ease-in-out infinite; }
@keyframes core-lift {
  0%, 100% { opacity: 0.16; }
  50%      { opacity: 0.6; }
}

.crown {
  opacity: 0;
  transform: translateY(-34px);
  transition: opacity 520ms ease, transform 680ms cubic-bezier(.34,1.25,.5,1);
}
.crown.on { opacity: 1; transform: translateY(0); }

.crown-label {
  font-size: 15px; font-weight: 700; letter-spacing: 0.14em; fill: var(--oppo-ink);
}
.plinth-label {
  font-size: 12px; font-weight: 600; letter-spacing: 0.2em; fill: var(--oppo-ink-2);
}
.col-label {
  font-size: 13px; font-weight: 700; letter-spacing: 0.22em; fill: var(--oppo-ink); opacity: 0.9;
}

.legend { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem; }
.leg {
  display: flex; gap: 0.55rem; align-items: flex-start;
  opacity: 0; transform: translateY(12px);
  transition: opacity 520ms ease, transform 520ms cubic-bezier(.22,1,.36,1);
}
.leg.on { opacity: 1; transform: translateY(0); }
.swatch { width: 3px; height: 100%; min-height: 34px; border-radius: 2px; flex: none; }
.leg-t { font-size: 0.72rem; font-weight: 750; letter-spacing: 0.14em; color: var(--oppo-ink); }
.leg-b { font-size: 0.74rem; line-height: 1.35; color: var(--oppo-ink-2); margin-top: 0.1rem; }
</style>
