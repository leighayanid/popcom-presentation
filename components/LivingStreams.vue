<script setup lang="ts">
/**
 * Standard of Living: four programmes, one household.
 * The ribbons run continuously because the sessions do; the house
 * assembles piece by piece as the programmes land, and only lights
 * up once all four are carrying.
 *
 * step 1 - the ribbons start carrying
 * step 2 - the household is built
 * step 3 - the lights come on
 * step 4 - what a well-planned household looks like
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const shown = (at: number) => props.step >= at

const HX = 640
const HY = 196

const PROGS = [
  {
    abbr: 'PMOC', color: 'var(--s2)', y: 44,
    name: 'Pre-Marriage Orientation and Counseling',
    body: 'Household size, child spacing, financial capability',
  },
  {
    abbr: 'RPS', color: 'var(--s3)', y: 124,
    name: 'Responsible Parenthood Sessions',
    body: 'Household resource management, long-term family planning',
  },
  {
    abbr: 'KATROPA', color: 'var(--s1)', y: 204,
    name: 'Kalalakihang Tapat sa Responsibilidad at Obligasyon sa Pamilya',
    body: 'Men in active caregiving and shared domestic responsibility',
  },
  {
    abbr: 'RP-LE', color: 'var(--s4)', y: 286,
    name: 'RP for Labor Force Empowerment',
    body: 'Formal workplaces and the informal sector',
  },
].map((p, i) => ({
  ...p, i,
  path: `M 268 ${p.y + 33} C 400 ${p.y + 33}, 440 ${HY}, ${HX - 126} ${HY}`,
}))

function nameLines(t: string, max = 42) {
  const words = t.split(' ')
  const out: string[] = []
  let cur = ''
  for (const w of words) {
    if ((cur + ' ' + w).trim().length > max && cur) { out.push(cur); cur = w }
    else cur = (cur + ' ' + w).trim()
  }
  if (cur) out.push(cur)
  return out
}

const OUTCOMES = [
  'Well-planned household size',
  'Financial capability',
  'Shared family responsibility',
  "Women's productive participation",
  'Labour force productivity',
  'Family economic resilience',
]
</script>

<template>
  <div class="ls">
    <svg viewBox="0 0 1000 380" class="stage" role="img"
      aria-label="Four responsible-parenthood programmes building one resilient household">
      <defs>
        <path v-for="p in PROGS" :key="'p' + p.i" :id="'ls-r-' + p.i" :d="p.path" />
        <radialGradient id="ls-warm" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="var(--oppo-gold-fig)" stop-opacity="0.55" />
          <stop offset="100%" stop-color="var(--oppo-gold-fig)" stop-opacity="0" />
        </radialGradient>
      </defs>

      <!-- programme cards -->
      <g v-for="p in PROGS" :key="p.abbr" class="prog on" :style="{ transitionDelay: (p.i * 90) + 'ms' }">
        <rect x="24" :y="p.y" width="244" height="70" rx="9" fill="var(--oppo-bg-2)"
          :stroke="p.color" stroke-width="1.1" stroke-opacity="0.55" />
        <rect x="24" :y="p.y" width="3.5" height="70" rx="2" :fill="p.color" />
        <text x="40" :y="p.y + 20" class="prog-a" :style="{ fill: p.color }">{{ p.abbr }}</text>
        <text x="40" :y="p.y + 33" class="prog-n">
          <tspan v-for="(ln, li) in nameLines(p.name)" :key="li" x="40" :dy="li === 0 ? 0 : 11">{{ ln }}</tspan>
        </text>
        <text x="40" :y="p.y + 33 + nameLines(p.name).length * 11 + 3" class="prog-b">{{ p.body }}</text>
      </g>

      <!-- ribbons -->
      <g class="ribbons" :class="{ on: shown(1) }">
        <use v-for="p in PROGS" :key="'u' + p.i" :href="'#ls-r-' + p.i" fill="none"
          :stroke="p.color" stroke-width="2" stroke-opacity="0.3"
          stroke-dasharray="7 10" class="ribbon" :style="{ animationDelay: (p.i * -2.2) + 's' }" />
        <template v-if="shown(1)">
          <g v-for="p in PROGS" :key="'c' + p.i">
            <circle v-for="k in 2" :key="k" r="3" :fill="p.color" opacity="0">
              <animateMotion dur="2.8s" repeatCount="indefinite"
                :begin="(p.i * 0.35 + (k - 1) * 1.4) + 's'">
                <mpath :href="'#ls-r-' + p.i" />
              </animateMotion>
              <animate attributeName="opacity" values="0;1;1;0" dur="2.8s"
                repeatCount="indefinite" :begin="(p.i * 0.35 + (k - 1) * 1.4) + 's'" />
            </circle>
          </g>
        </template>
      </g>

      <!-- the household -->
      <g :transform="'translate(' + HX + ' ' + HY + ')'">
        <ellipse v-if="shown(3)" cx="0" cy="-10" rx="150" ry="120" fill="url(#ls-warm)" class="warm" />

        <!-- foundation -->
        <rect class="piece" :class="{ on: shown(2) }" style="transition-delay:0ms"
          x="-124" y="68" width="248" height="14" rx="4" fill="var(--oppo-bg-3)"
          stroke="var(--h-30)" stroke-width="1" />
        <!-- walls -->
        <rect class="piece" :class="{ on: shown(2) }" style="transition-delay:120ms"
          x="-104" y="-8" width="208" height="76" fill="var(--oppo-panel-2)"
          stroke="var(--g-50)" stroke-width="1.4" />
        <!-- roof -->
        <path class="piece roof" :class="{ on: shown(2) }" style="transition-delay:240ms"
          d="M -122 -8 L 0 -86 L 122 -8 Z" fill="var(--oppo-bg-2)"
          stroke="var(--g-65)" stroke-width="1.5" stroke-linejoin="round" />
        <!-- door -->
        <rect class="piece" :class="{ on: shown(2) }" style="transition-delay:360ms"
          x="-19" y="24" width="38" height="44" rx="3" fill="var(--oppo-bg-3)"
          stroke="var(--g-50)" stroke-width="1.1" />
        <circle class="piece" :class="{ on: shown(2) }" style="transition-delay:360ms"
          cx="11" cy="47" r="2.2" fill="var(--oppo-gold)" />
        <!-- windows -->
        <g class="piece" :class="{ on: shown(2) }" style="transition-delay:300ms">
          <rect x="-78" y="10" width="40" height="32" rx="3"
            :fill="shown(3) ? 'var(--oppo-gold-fig)' : 'var(--oppo-bg-3)'" class="win"
            stroke="var(--g-50)" stroke-width="1.1" />
          <rect x="38" y="10" width="40" height="32" rx="3"
            :fill="shown(3) ? 'var(--oppo-gold-fig)' : 'var(--oppo-bg-3)'" class="win" style="animation-delay:.6s"
            stroke="var(--g-50)" stroke-width="1.1" />
          <line x1="-58" y1="10" x2="-58" y2="42" stroke="var(--oppo-panel-2)" stroke-width="1.6" />
          <line x1="58" y1="10" x2="58" y2="42" stroke="var(--oppo-panel-2)" stroke-width="1.6" />
          <line x1="-78" y1="26" x2="-38" y2="26" stroke="var(--oppo-panel-2)" stroke-width="1.6" />
          <line x1="38" y1="26" x2="78" y2="26" stroke="var(--oppo-panel-2)" stroke-width="1.6" />
        </g>

        <!-- the family in front of it -->
        <g class="family" :class="{ on: shown(3) }" transform="translate(0 82)">
          <g v-for="(f, i) in [{ x: -34, s: 1 }, { x: -12, s: 0.72 }, { x: 8, s: 0.72 }, { x: 32, s: 1 }]"
            :key="i" :transform="'translate(' + f.x + ' 0) scale(' + f.s + ')'">
            <g fill="var(--oppo-gold-fig)" class="fig" :style="{ animationDelay: (i * 0.4) + 's' }">
              <circle cx="0" cy="-16" r="5" />
              <path d="M -8 2 C -8 -7, -4 -10, 0 -10 C 4 -10, 8 -7, 8 2 Z" />
            </g>
          </g>
        </g>

        <text y="150" text-anchor="middle" class="house-l" :class="{ on: shown(2) }">
          A WELL-PLANNED, HEALTHY, EMPOWERED AND RESILIENT HOUSEHOLD
        </text>
      </g>

      <!-- outcomes -->
      <g class="outcomes" :class="{ on: shown(4) }">
        <g v-for="(o, i) in OUTCOMES" :key="i" class="out"
          :style="{ transitionDelay: (i * 80) + 'ms' }">
          <rect x="760" :y="44 + i * 48" width="216" height="34" rx="8" fill="var(--oppo-bg-2)"
            stroke="var(--g-30)" stroke-width="0.9" />
          <circle cx="776" :cy="61 + i * 48" r="3" fill="var(--oppo-gold)" />
          <text x="788" :y="65 + i * 48" class="out-t">{{ o }}</text>
        </g>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.ls { width: 100%; }
.stage { width: 100%; height: auto; }

.prog { opacity: 0; transform: translateX(-16px); transform-box: view-box;
  transition: opacity 520ms ease, transform 560ms cubic-bezier(.22,1,.36,1); }
.prog.on { opacity: 1; transform: translateX(0); }
.prog-a { font-size: 13px; font-weight: 800; letter-spacing: 0.14em; }
.prog-n { font-size: 11px; font-weight: 650; fill: var(--oppo-ink); }
.prog-b { font-size: 10.5px; fill: var(--oppo-ink-2); }

.ribbons { opacity: 0; transition: opacity 600ms ease; }
.ribbons.on { opacity: 1; }
.ribbon { animation: oppo-dash 26s linear infinite; }
/* the light series steps are paler, so the ribbons need more weight on paper */
html.light .ribbon { stroke-opacity: 0.6; }

.piece { opacity: 0; transform: translateY(16px); transform-box: view-box;
  transition: opacity 500ms ease, transform 620ms cubic-bezier(.3,1.4,.5,1); }
.piece.on { opacity: 1; transform: translateY(0); }
.roof { transform: translateY(-26px); }
.roof.on { transform: translateY(0); }

.win { transition: fill 800ms ease; animation: win-flicker 5s ease-in-out infinite; }
@keyframes win-flicker {
  0%, 100% { opacity: 1; }
  48%      { opacity: 0.82; }
}
.warm { animation: oppo-breathe 5s ease-in-out infinite; }

.family { opacity: 0; transform: translate(0, 94px); transform-box: view-box;
  transition: opacity 620ms ease 300ms, transform 700ms cubic-bezier(.3,1.3,.5,1) 300ms; }
.family.on { opacity: 1; transform: translate(0, 82px); }
.fig { animation: oppo-bob 3s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }

.house-l { font-size: 10.5px; font-weight: 750; letter-spacing: 0.12em; fill: var(--oppo-gold);
  opacity: 0; transition: opacity 600ms ease 400ms; }
.house-l.on { opacity: 1; }

.outcomes { opacity: 0; transition: opacity 500ms ease; }
.outcomes.on { opacity: 1; }
.out { opacity: 0; transform: translateX(14px); transform-box: view-box;
  transition: opacity 460ms ease, transform 520ms ease; }
.outcomes.on .out { opacity: 1; transform: translateX(0); }
.out-t { font-size: 10.5px; font-weight: 600; fill: var(--oppo-ink-1); }
</style>
