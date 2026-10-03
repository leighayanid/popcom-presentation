<script setup lang="ts">
/**
 * The Education dimension: Bataeno Pass student registration as the system
 * layer, and Adolescent Health and Development as the protective layer.
 * Both end at the same place - a young person who stays in school.
 *
 * step 1 - the Pass is issued
 * step 2 - it is tapped at the school, with the partners who make that possible
 * step 3 - what the tap records
 * step 4 - what that may support
 * step 5 - the AHD interventions guarding the same outcome
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const shown = (at: number) => props.step >= at

const PARTNERS = ['DepEd', "Provincial Governor's Office", 'Provincial School Board']

const RECORDS = [
  ['Attendance monitoring'],
  ['Provincial social and educational', 'services received'],
]

const AHD = [
  { t: 'Adolescent Pregnancy Prevention Response Program', n: '' },
  { t: 'School-based and community-based AHD sessions', n: '' },
  { t: 'Teen Information Centers established', n: '103' },
]
</script>

<template>
  <div class="ef">
    <svg viewBox="0 0 1000 400" class="stage" role="img"
      aria-label="Bataeño Pass student registration feeding the Education Index, with adolescent health programmes alongside">
      <defs>
        <linearGradient id="ef-sheen" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="var(--oppo-gold)" stop-opacity="0" />
          <stop offset="50%" stop-color="var(--oppo-gold)" stop-opacity="0.55" />
          <stop offset="100%" stop-color="var(--oppo-gold)" stop-opacity="0" />
        </linearGradient>
        <clipPath id="ef-cardclip"><rect x="-62" y="-39" width="124" height="78" rx="8" /></clipPath>
        <filter id="ef-cardlift" x="-40%" y="-40%" width="180%" height="190%">
          <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#000" flood-opacity="0.42" />
        </filter>
        <path id="ef-tap" d="M 318 120 C 360 120, 380 120, 404 120" />
        <path id="ef-rec1" d="M 506 99 H 596" />
        <path id="ef-rec2" d="M 506 137 H 596" />
        <path id="ef-out" d="M 816 99 C 846 99, 842 118, 836 118" />
        <path id="ef-out2" d="M 816 137 C 846 137, 842 118, 836 118" />
        <path id="ef-ahd" d="M 700 320 C 780 320, 802 240, 836 150" />
      </defs>

      <!-- partners rail -->
      <g class="partners" :class="{ on: shown(2) }">
        <text x="42" y="29" class="rail-k">IN PARTNERSHIP WITH</text>
        <g v-for="(p, i) in PARTNERS" :key="p" :transform="'translate(' + (214 + i * 190) + ' 14)'">
          <g class="pill" :style="{ transitionDelay: (i * 110) + 'ms' }">
            <rect x="0" y="0" width="180" height="22" rx="11" fill="var(--oppo-bg-2)"
              stroke="var(--s2-45)" stroke-width="0.9" />
            <text x="90" y="15" text-anchor="middle" class="pill-t">{{ p }}</text>
          </g>
        </g>
      </g>

      <!-- 1. the student -->
      <g class="node on" transform="translate(70 120)">
        <circle r="38" fill="var(--oppo-panel-2)" stroke="var(--h-30)" stroke-width="1.3" />
        <g fill="var(--s2)" class="pupil">
          <circle cx="0" cy="-12" r="7.5" />
          <path d="M -12.5 18 C -12.5 2.5, -6.5 -1.5, 0 -1.5 C 6.5 -1.5, 12.5 2.5, 12.5 18 Z" />
        </g>
        <text y="58" text-anchor="middle" class="node-n">STUDENT</text>
      </g>

      <!-- 2. the Pass is issued -->
      <g class="flow" :class="{ on: shown(1) }">
        <path d="M 112 120 H 182" stroke="var(--g-45)" stroke-width="1.3" />
        <path d="M 176 116 L 182 120 L 176 124" fill="none" stroke="var(--oppo-gold)" stroke-width="1.3" />
      </g>
      <g class="card-wrap" :class="{ on: shown(1) }" transform="translate(250 120)">
        <g class="card" filter="url(#ef-cardlift)">
          <g clip-path="url(#ef-cardclip)">
            <image href="/bataeno-pass-card.jpg" x="-62" y="-39" width="124" height="78"
              preserveAspectRatio="xMidYMid slice" />
            <rect class="sheen" x="-62" y="-39" width="56" height="78" fill="url(#ef-sheen)" />
          </g>
          <rect x="-62" y="-39" width="124" height="78" rx="8" fill="none"
            stroke="var(--oppo-gold)" stroke-width="1.2" />
        </g>
        <text y="62" text-anchor="middle" class="node-n">PASS ISSUED</text>
        <text y="75" text-anchor="middle" class="card-s2">STUDENT REGISTRATION</text>
      </g>

      <!-- 3. the tap -->
      <g class="flow" :class="{ on: shown(2) }">
        <use href="#ef-tap" fill="none" stroke="var(--g-45)" stroke-width="1.3" />
        <template v-if="shown(2)">
          <circle r="3" fill="var(--oppo-gold)" opacity="0">
            <animateMotion dur="1.5s" repeatCount="indefinite"><mpath href="#ef-tap" /></animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="1.5s" repeatCount="indefinite" />
          </circle>
        </template>
      </g>
      <g class="node" :class="{ on: shown(2) }" transform="translate(450 120)">
        <circle v-if="shown(2)" r="34" fill="none" stroke="var(--s2)" stroke-width="1.2" class="tap-ring" />
        <circle v-if="shown(2)" r="34" fill="none" stroke="var(--s2)" stroke-width="1.2" class="tap-ring"
          style="animation-delay: 1.1s" />
        <rect x="-30" y="-34" width="60" height="68" rx="7" fill="var(--oppo-panel-2)"
          stroke="var(--s2)" stroke-width="1.4" />
        <!-- school -->
        <g stroke="var(--s2)" stroke-width="1.6" fill="none" stroke-linejoin="round">
          <path d="M -18 -2 L 0 -16 L 18 -2 V 18 H -18 Z" />
          <path d="M -6 18 V 6 H 6 V 18" />
          <path d="M 0 -16 V -24" />
        </g>
        <text y="30" text-anchor="middle" class="tap-t">TAP</text>
        <text y="58" text-anchor="middle" class="node-n">AT SCHOOL</text>
      </g>

      <!-- 4. what the tap records -->
      <g class="flow" :class="{ on: shown(3) }">
        <use href="#ef-rec1" fill="none" stroke="var(--g-35)" stroke-width="1.1" />
        <use href="#ef-rec2" fill="none" stroke="var(--g-35)" stroke-width="1.1" />
        <template v-if="shown(3)">
          <circle r="2.4" fill="var(--oppo-gold)" opacity="0">
            <animateMotion dur="1.4s" repeatCount="indefinite"><mpath href="#ef-rec1" /></animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="1.4s" repeatCount="indefinite" />
          </circle>
          <circle r="2.4" fill="var(--oppo-gold)" opacity="0">
            <animateMotion dur="1.4s" repeatCount="indefinite" begin="0.5s"><mpath href="#ef-rec2" /></animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="1.4s" repeatCount="indefinite" begin="0.5s" />
          </circle>
        </template>
      </g>
      <g class="records" :class="{ on: shown(3) }">
        <g v-for="(r, i) in RECORDS" :key="i" class="rec" :style="{ transitionDelay: (i * 130) + 'ms' }">
          <rect x="600" :y="86 + i * 34" width="216" :height="r.length > 1 ? 34 : 26" rx="7"
            fill="var(--oppo-bg-2)" stroke="var(--g-30)" stroke-width="0.9" />
          <text x="708" :y="103 + i * 34 - (r.length - 1) * 5" text-anchor="middle" class="rec-t">
            <tspan v-for="(ln, li) in r" :key="li" x="708" :dy="li === 0 ? 0 : 11">{{ ln }}</tspan>
          </text>
        </g>
      </g>

      <!-- 5. the index -->
      <g class="flow" :class="{ on: shown(4) }">
        <use href="#ef-out" fill="none" stroke="var(--g-40)" stroke-width="1.2" />
        <use href="#ef-out2" fill="none" stroke="var(--g-40)" stroke-width="1.2" />
      </g>
      <g class="node idx" :class="{ on: shown(4) }" transform="translate(906 118)">
        <rect x="-70" y="-34" width="140" height="68" rx="9" fill="var(--oppo-panel-2)"
          stroke="var(--oppo-gold)" stroke-width="1.6" />
        <text y="-12" text-anchor="middle" class="lei-k">HDI++</text>
        <text y="8" text-anchor="middle" class="lei-t">EDUCATION</text>
        <text y="24" text-anchor="middle" class="lei-s">INDEX</text>
      </g>
      <text x="708" y="172" text-anchor="middle" class="idx-note" :class="{ on: shown(4) }">
        may support analysis of attendance,
      </text>
      <text x="708" y="185" text-anchor="middle" class="idx-note" :class="{ on: shown(4) }">
        completion and other education outcomes
      </text>

      <!-- AHD: the protective layer -->
      <g class="ahd" :class="{ on: shown(5) }">
        <line x1="42" y1="268" x2="958" y2="268" stroke="var(--h-14)" stroke-width="1" />
        <text x="46" y="292" class="rail-k">ADOLESCENT HEALTH AND DEVELOPMENT</text>
        <g v-for="(a, i) in AHD" :key="i" class="ahd-card" :style="{ transitionDelay: (i * 130) + 'ms' }">
          <rect :x="46 + i * 222" y="304" width="206" height="48" rx="8" fill="var(--oppo-bg-2)"
            stroke="var(--s5-45)" stroke-width="1" />
          <text v-if="a.n" :x="46 + i * 222 + 18" y="336" class="ahd-n">{{ a.n }}</text>
          <text :x="a.n ? 46 + i * 222 + 60 : 46 + i * 222 + 14" y="324" class="ahd-t">
            <tspan :x="a.n ? 46 + i * 222 + 60 : 46 + i * 222 + 14">{{ a.t.split(' ').slice(0, 3).join(' ') }}</tspan>
            <tspan :x="a.n ? 46 + i * 222 + 60 : 46 + i * 222 + 14" dy="13">{{ a.t.split(' ').slice(3).join(' ') }}</tspan>
          </text>
        </g>
        <use href="#ef-ahd" fill="none" stroke="var(--s5-45)" stroke-width="1.2"
          stroke-dasharray="4 5" class="ahd-arc" />
        <template v-if="shown(5)">
          <circle r="2.6" fill="var(--s5)" opacity="0">
            <animateMotion dur="2.4s" repeatCount="indefinite"><mpath href="#ef-ahd" /></animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="2.4s" repeatCount="indefinite" />
          </circle>
        </template>
        <text x="371" y="372" text-anchor="middle" class="ahd-out">
          protecting the educational opportunity and the health of Bataeño youth
        </text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.ef { width: 100%; }
.stage { width: 100%; height: auto; }

.node, .flow, .records, .partners, .ahd, .card-wrap {
  opacity: 0; transition: opacity 560ms ease;
}
.node.on, .flow.on, .records.on, .partners.on, .ahd.on, .card-wrap.on { opacity: 1; }
.node-n { font-size: 11px; font-weight: 750; letter-spacing: 0.16em; fill: var(--oppo-ink-2); }

.pupil { animation: oppo-bob 3.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }

.rail-k { font-size: 10px; font-weight: 750; letter-spacing: 0.22em; fill: var(--oppo-ink-2); }
.pill { opacity: 0; transform: translateY(-8px); transition: opacity 480ms ease, transform 520ms ease; }
.partners.on .pill { opacity: 1; transform: translateY(0); }
.pill-t { font-size: 11.5px; font-weight: 600; fill: var(--oppo-ink-1); }

.card { transform: scaleX(0.04); transform-box: fill-box; transform-origin: center;
  transition: transform 720ms cubic-bezier(.3,1.35,.45,1); }
.card-wrap.on .card { transform: scaleX(1); }
.card-s2 { font-size: 8.5px; font-weight: 650; letter-spacing: 0.18em; fill: var(--oppo-ink-2); }
.sheen { animation: oppo-sheen 4.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }

.tap-ring { animation: tap 2.2s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes tap {
  0%   { transform: scale(0.8); opacity: 0.7; }
  100% { transform: scale(1.6); opacity: 0; }
}
.tap-t { font-size: 9.5px; font-weight: 800; letter-spacing: 0.2em; fill: var(--s2); }

.rec { opacity: 0; transform: translateX(-12px); transition: opacity 460ms ease, transform 520ms ease; }
.records.on .rec { opacity: 1; transform: translateX(0); }
.rec-t { font-size: 12px; font-weight: 600; fill: var(--oppo-ink-1); }

.lei-k { font-size: 9.5px; font-weight: 800; letter-spacing: 0.2em; fill: var(--oppo-gold); }
.lei-t { font-size: 15px; font-weight: 750; fill: var(--oppo-ink); }
.lei-s { font-size: 10.5px; font-weight: 650; letter-spacing: 0.2em; fill: var(--oppo-ink-2); }
.idx-note { font-size: 10.5px; fill: var(--oppo-ink-2); opacity: 0; transition: opacity 560ms ease 200ms; }
.idx-note.on { opacity: 1; }

.ahd-card { opacity: 0; transform: translateY(12px); transition: opacity 480ms ease, transform 520ms ease; }
.ahd.on .ahd-card { opacity: 1; transform: translateY(0); }
.ahd-n { font-size: 19px; font-weight: 800; fill: var(--s5); }
.ahd-t { font-size: 11px; font-weight: 600; fill: var(--oppo-ink-1); }
.ahd-out { font-size: 10.5px; font-style: italic; fill: var(--oppo-ink-2); }
.ahd-arc { animation: oppo-dash 22s linear infinite; }
</style>
