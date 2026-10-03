<script setup lang="ts">
/**
 * Executive Order No. 26, s. 2026 - the transfer of the Bataeno Pass to OPPO.
 * step 0 - the rail and its origin
 * step 1 - the order is signed (stamp impact + shockwave)
 * step 2 - the programme glides from the PGO across to OPPO
 * step 3 - province-wide registration begins to fill
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const signed = computed(() => props.step >= 1)
const handed = computed(() => props.step >= 2)
const rolling = computed(() => props.step >= 3)

const STATIONS = [
  { x: 130, year: '2022', title: 'Provincial Ordinance No. 23', body: 'Institutionalised the Provincial Personal Data Card (PPDC) System - the Bataeño Pass' },
  { x: 400, year: '2026', title: 'Executive Order No. 26', body: 'Issued by Governor Jose Enrique S. Garcia III, establishing the Program Management Structure' },
  { x: 660, year: 'JULY 2026', title: 'Transferred to OPPO', body: 'Implementation and operationalisation placed under the direct supervision and control of this Office' },
  { x: 900, year: 'PRESENT', title: 'Province-wide build-out', body: 'Expanding citizen registration while developing the digital system behind its use cases' },
]

const litUpTo = computed(() => {
  if (rolling.value) return 3
  if (handed.value) return 2
  if (signed.value) return 1
  return 0
})
</script>

<template>
  <div class="eo">
    <svg viewBox="0 0 1000 250" class="stage" role="img"
      aria-label="Timeline of the transfer of the Bataeño Pass programme to OPPO">
      <defs>
        <linearGradient id="eo-rail" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="var(--oppo-gold)" />
          <stop offset="100%" stop-color="var(--oppo-gold)" />
        </linearGradient>
        <path id="eo-hand" d="M 400 92 C 470 36, 590 36, 660 92" />
      </defs>

      <!-- rail -->
      <line x1="130" y1="92" x2="900" y2="92" stroke="var(--h-20)" stroke-width="2" />
      <line x1="130" y1="92" :x2="130 + (STATIONS[litUpTo].x - 130)" y2="92"
        stroke="url(#eo-rail)" stroke-width="3" stroke-linecap="round" class="rail-lit" />

      <!-- the hand-over arc: the programme crossing from the PGO to OPPO -->
      <g class="hand" :class="{ on: handed }">
        <use href="#eo-hand" fill="none" stroke="var(--g-45)"
          stroke-width="1.4" stroke-dasharray="5 5" class="hand-arc" />
        <template v-if="handed">
          <g opacity="0">
            <!-- the Pass itself, riding the arc -->
            <rect x="-15" y="-10" width="30" height="20" rx="3.5" fill="var(--oppo-bg-2)"
              stroke="var(--oppo-gold)" stroke-width="1.2" />
            <rect x="-11" y="-6" width="9" height="7" rx="1.5" fill="var(--oppo-gold-fig)" opacity="0.85" />
            <line x1="1" y1="-4" x2="11" y2="-4" stroke="var(--oppo-ink-2)" stroke-width="1.2" />
            <line x1="1" y1="0" x2="11" y2="0" stroke="var(--oppo-ink-2)" stroke-width="1.2" />
            <line x1="-11" y1="5" x2="11" y2="5" stroke="var(--oppo-ink-3)" stroke-width="1.2" />
            <animateMotion dur="3.4s" repeatCount="indefinite" rotate="auto">
              <mpath href="#eo-hand" />
            </animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="3.4s" repeatCount="indefinite" />
          </g>
        </template>
      </g>

      <!-- stations -->
      <g v-for="(s, i) in STATIONS" :key="i" class="st" :class="{ on: i <= litUpTo }"
        :style="{ transitionDelay: (i * 90) + 'ms' }">
        <circle v-if="i <= litUpTo" :cx="s.x" cy="92" r="10" fill="none"
          stroke="var(--oppo-gold)" stroke-width="1.2" class="ping"
          :style="{ animationDelay: (i * 0.4) + 's' }" />
        <circle :cx="s.x" cy="92" r="6.5" :fill="i <= litUpTo ? 'var(--oppo-gold)' : 'var(--oppo-bg-3)'"
          stroke="var(--g-60)" stroke-width="1.2" class="dot" />
        <text :x="s.x" y="68" text-anchor="middle" class="st-year">{{ s.year }}</text>
        <text :x="s.x" y="126" text-anchor="middle" class="st-title">{{ s.title }}</text>
      </g>

      <!-- the seal landing on EO 26 -->
      <g class="seal" :class="{ on: signed }" transform="translate(400 180)">
        <circle r="26" fill="none" stroke="var(--g-90)" stroke-width="1.6" />
        <circle r="20" fill="none" stroke="var(--g-45)" stroke-width="0.9" />
        <text y="-4" text-anchor="middle" class="seal-t">EO 26</text>
        <text y="9" text-anchor="middle" class="seal-s">S. 2026</text>
        <circle v-if="signed" r="26" fill="none" stroke="var(--oppo-gold)" stroke-width="1.4" class="shock" />
      </g>

      <!-- registration fill -->
      <g class="reg" :class="{ on: rolling }" transform="translate(900 172)">
        <rect x="-62" y="-9" width="124" height="18" rx="9" fill="var(--oppo-panel-2)"
          stroke="var(--h-22)" stroke-width="1" />
        <rect x="-60" y="-7" width="0" height="14" rx="7" fill="var(--s3)" class="reg-fill" />
        <text y="28" text-anchor="middle" class="reg-l">CITIZEN REGISTRATION</text>
      </g>
    </svg>

    <div class="cards">
      <div v-for="(s, i) in STATIONS" :key="i" class="card oppo-card"
        :class="{ on: i <= litUpTo }" :style="{ transitionDelay: (120 + i * 90) + 'ms' }">
        <div class="card-t">{{ s.title }}</div>
        <div class="card-b">{{ s.body }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.eo { width: 100%; display: flex; flex-direction: column; gap: 0.7rem; }
.stage { width: 100%; height: auto; }

.rail-lit { transition: all 700ms cubic-bezier(.22,1,.36,1); }

.st { transition: opacity 500ms ease; opacity: 0.45; }
.st.on { opacity: 1; }
.dot { transition: fill 500ms ease; }
.ping { animation: oppo-pulse-ring 2.4s ease-out infinite; }

.st-year { font-size: 12px; font-weight: 750; letter-spacing: 0.2em; fill: var(--oppo-gold); }
.st-title { font-size: 15px; font-weight: 650; fill: var(--oppo-ink); }

.seal {
  opacity: 0;
  transform: translate(400px, 180px) scale(2.6) rotate(-14deg);
  transition: opacity 260ms ease, transform 420ms cubic-bezier(.3,1.6,.5,1);
}
.seal.on { opacity: 1; transform: translate(400px, 180px) scale(1) rotate(-8deg); }
.seal-t { font-size: 12px; font-weight: 800; letter-spacing: 0.1em; fill: var(--oppo-gold); }
.seal-s { font-size: 8.5px; font-weight: 650; letter-spacing: 0.16em; fill: var(--oppo-ink-2); }
.shock { animation: shock 2.8s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes shock {
  0%   { transform: scale(1); opacity: 0.7; }
  60%  { transform: scale(2.4); opacity: 0; }
  100% { transform: scale(2.4); opacity: 0; }
}

.hand { opacity: 0; transition: opacity 500ms ease; }
.hand.on { opacity: 1; }
.hand-arc { animation: oppo-dash 18s linear infinite; }

.reg { opacity: 0; transition: opacity 500ms ease; }
.reg.on { opacity: 1; }
.reg-l { font-size: 11px; font-weight: 700; letter-spacing: 0.16em; fill: var(--oppo-ink-2); }
.reg.on .reg-fill { animation: reg-fill 3.6s ease-in-out infinite; }
@keyframes reg-fill {
  0%   { width: 0; }
  70%  { width: 92px; }
  100% { width: 92px; }
}

.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.7rem; }
.card {
  opacity: 0; transform: translateY(14px);
  transition: opacity 520ms ease, transform 520ms cubic-bezier(.22,1,.36,1);
}
.card.on { opacity: 1; transform: translateY(0); }
.card-t { font-size: 0.95rem; font-weight: 700; color: var(--oppo-gold); margin-bottom: 0.2rem; }
.card-b { font-size: 0.9rem; line-height: 1.4; color: var(--oppo-ink-2); }
</style>
