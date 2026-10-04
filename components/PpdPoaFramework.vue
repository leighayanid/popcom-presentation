<script setup lang="ts">
/**
 * PPD-POA 2023-2028 strategy framework.
 * step 0 - the empty frame, waiting
 * step 1 - the six strategies land, blue column then green column
 * step 2 - the two enabling strategies rise underneath and prop them up
 * step 3 - the lift carries everything into the goal
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const strategies = computed(() => props.step >= 1)
const enablers = computed(() => props.step >= 2)
const goal = computed(() => props.step >= 3)

const BLUE = 'var(--s2)'
const GREEN = 'var(--s3)'

type Card = { n: number; icon: string; color: string; title: string[]; sub: string[] }

// the six, laid out as the national framework prints them: 1-3 left, 4-6 right
const CARDS: Card[] = [
  {
    n: 1, icon: 'family', color: BLUE,
    title: ['PROMOTE RESPONSIBLE PARENTHOOD'],
    sub: ['Pre-Marriage Orientation and Counseling · KATROPA', 'Responsible Parenthood Sessions'],
  },
  {
    n: 2, icon: 'teen', color: BLUE,
    title: ['ADVANCE ADOLESCENT HEALTH AND', 'DEVELOPMENT (AHD)'],
    sub: ['AHD Sessions (schools and communities) · Teen', 'Information Center · Service Delivery Network'],
  },
  {
    n: 3, icon: 'work', color: BLUE,
    title: ['SUPPORT LABOR FORCE EMPOWERMENT', 'AND ACTIVE AND HEALTHY AGEING'],
    sub: [],
  },
  {
    n: 4, icon: 'growth', color: GREEN,
    title: ['ACCELERATE INCLUSIVE DEVELOPMENT', 'AMONG MARGINALIZED SECTORS'],
    sub: [],
  },
  {
    n: 5, icon: 'doc', color: GREEN,
    title: ['INTEGRATE POPULATION AGENDA IN', 'SECTORAL DEVELOPMENT'],
    sub: [],
  },
  {
    n: 6, icon: 'people', color: GREEN,
    title: ['STRENGTHEN PEOPLE-CENTERED', 'REGIONAL AND LOCAL DEVELOPMENT'],
    sub: [],
  },
]

// the two that hold the other six up
const BASE: Card[] = [
  {
    n: 7, icon: 'hands', color: BLUE,
    title: ['FOSTER PARTNERSHIP AND', 'COLLABORATION ON POPDEV'],
    sub: [],
  },
  {
    n: 8, icon: 'data', color: GREEN,
    title: ['INTENSIFY POPDEV DATABASES, REGISTRIES,', 'RESEARCH AND KNOWLEDGE MANAGEMENT'],
    sub: [],
  },
]

const COL_X = [22, 512]
const ROW_Y = [112, 192, 272]
const CARD_W = 466
const CARD_H = 72
const BASE_Y = 362
const BASE_H = 54

function place(i: number) {
  return { x: COL_X[i < 3 ? 0 : 1], y: ROW_Y[i % 3] }
}

// text block, vertically centred in whatever card height it sits in
function lineY(c: Card, h: number, y: number) {
  const block = c.title.length * 15 + (c.sub.length ? 5 + c.sub.length * 12 : 0)
  return y + h / 2 - block / 2 + 11
}
</script>

<template>
  <div class="pf">
    <svg viewBox="0 0 1000 424" class="stage" role="img"
      aria-label="The PPD-POA 2023-2028 strategy framework: eight strategies supporting one goal">
      <defs>
        <clipPath id="pf-panel">
          <rect x="8" y="98" width="984" height="318" rx="22" />
        </clipPath>

        <linearGradient id="pf-goal" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="var(--g-16)" />
          <stop offset="100%" stop-color="var(--g-07)" />
        </linearGradient>
        <linearGradient id="pf-rise" x1="0" y1="1" x2="0" y2="0">
          <stop offset="0%" stop-color="var(--oppo-gold)" stop-opacity="0.15" />
          <stop offset="100%" stop-color="var(--oppo-gold)" stop-opacity="0.95" />
        </linearGradient>

        <!-- the eight marks, drawn once on a 24-unit grid -->
        <g id="pf-family">
          <circle cx="7" cy="7.5" r="2.4" />
          <path d="M3 18.5v-1.6a4 4 0 0 1 8 0v1.6" />
          <path d="M17.2 18.4c-2-1.5-3.5-2.6-3.5-4.2 0-1.2 1-2 2-2 .7 0 1.2.3 1.5.8.3-.5.8-.8 1.5-.8 1 0 2 .8 2 2 0 1.6-1.5 2.7-3.5 4.2z" />
        </g>
        <g id="pf-teen">
          <circle cx="9.5" cy="7.5" r="2.6" />
          <path d="M4.5 18.5v-1.5a5 5 0 0 1 10 0v1.5" />
          <path d="M18.5 5.5v5M16 8h5" />
        </g>
        <g id="pf-work">
          <path d="M3.5 8.5h17v10h-17z" />
          <path d="M9 8.5V6.8c0-.7.6-1.3 1.3-1.3h3.4c.7 0 1.3.6 1.3 1.3v1.7" />
          <path d="M3.5 12.8h17" />
          <path d="M11 12h2v2.2h-2z" />
        </g>
        <g id="pf-growth">
          <path d="M3.5 19.5h17" />
          <path d="M5.5 17v-5h3v5zM10.5 17V8.5h3V17zM15.5 17V4.5h3V17z" />
        </g>
        <g id="pf-doc">
          <path d="M6.5 3.5H13l4.5 4.5v12h-11z" />
          <path d="M13 3.5V8h4.5" />
          <circle cx="12" cy="14.5" r="2.2" />
          <path d="M12 10.8v1.2M12 17v1.2M8.3 14.5h1.2M14.5 14.5h1.2" />
        </g>
        <g id="pf-people">
          <circle cx="12" cy="7" r="2.6" />
          <path d="M7.5 18.5v-1a4.5 4.5 0 0 1 9 0v1" />
          <circle cx="4.8" cy="10" r="1.9" />
          <path d="M1.5 17.5v-.7c0-1.3.9-2.5 2.1-2.9" />
          <circle cx="19.2" cy="10" r="1.9" />
          <path d="M22.5 17.5v-.7c0-1.3-.9-2.5-2.1-2.9" />
        </g>
        <g id="pf-hands">
          <path d="M2.5 9.5h5.2L11 12.8" />
          <path d="M21.5 9.5h-5.2L13 12.8" />
          <path d="M7.7 9.5 11.5 5.7a2.2 2.2 0 0 1 3 0l1.8 1.8" />
          <path d="m9.2 14.4 2.4 2.4a1.5 1.5 0 0 0 2.2 0l.3-.4.9.9a1.5 1.5 0 0 0 2.1-2.1l-2.3-2.3" />
        </g>
        <g id="pf-data">
          <ellipse cx="12" cy="6" rx="7.5" ry="3" />
          <path d="M4.5 6v12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6" />
          <path d="M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3" />
        </g>
      </defs>

      <!-- ============ backdrop ============ -->
      <g class="backdrop" aria-hidden="true">
        <rect x="8" y="98" width="984" height="318" rx="22" fill="var(--oppo-bg-0)" opacity="0.45" />
        <g clip-path="url(#pf-panel)">
          <circle cx="112" cy="168" r="112" fill="var(--g-07)" opacity="0.6" />
          <circle cx="900" cy="386" r="150" fill="var(--s2-45)" opacity="0.1" />
          <path d="M0 398c130-26 190 18 318 6s176-40 310-30 180 42 372 10v42H0z" fill="var(--s2-45)" opacity="0.14" />
          <path d="M0 412c148-22 206 14 330 4s182-32 306-24 196 34 364 6v28H0z" fill="var(--g-16)" opacity="0.5" />
        </g>
        <rect x="8" y="98" width="984" height="318" rx="22" fill="none" stroke="var(--h-10)" />
      </g>

      <!-- ============ the goal ============ -->
      <g class="goal" :class="{ on: goal }">
        <rect x="118" y="10" width="764" height="54" rx="14" fill="url(#pf-goal)"
          stroke="var(--g-45)" stroke-width="1.2" />
        <text x="500" y="32" text-anchor="middle" class="goal-t">
          <tspan class="hl">Optimize demographic opportunities</tspan><tspan> and address persistent population issues</tspan>
        </text>
        <text x="500" y="51" text-anchor="middle" class="goal-t">
          <tspan>to reap the demographic dividend and accelerate </tspan><tspan class="hl">sustainable, inclusive development</tspan><tspan> at all levels</tspan>
        </text>
      </g>

      <!-- the lift from the strategies into the goal -->
      <g class="rise" :class="{ on: goal }">
        <path d="M494 94v-20h12v20z" fill="url(#pf-rise)" />
        <path d="M486 76l14-16 14 16z" fill="var(--oppo-gold)" opacity="0.95" class="tip" />
      </g>

      <!-- ============ the band ============ -->
      <g class="band">
        <line x1="22" y1="88" x2="404" y2="88" stroke="var(--h-16)" />
        <line x1="596" y1="88" x2="978" y2="88" stroke="var(--h-16)" />
        <rect x="414" y="76" width="172" height="25" rx="12.5"
          fill="var(--oppo-bg-2)" stroke="var(--g-50)" stroke-width="1.1" />
        <text x="500" y="93" text-anchor="middle" class="band-t">STRATEGIES</text>
      </g>

      <!-- ============ the six ============ -->
      <g v-for="(c, i) in CARDS" :key="c.n" class="card" :class="{ on: strategies }"
        :style="{ transitionDelay: (120 + i * 110) + 'ms' }">
        <rect :x="place(i).x" :y="place(i).y" :width="CARD_W" :height="CARD_H" rx="12"
          fill="var(--oppo-bg-2)" stroke="var(--h-14)" />
        <rect :x="place(i).x" :y="place(i).y" width="4" :height="CARD_H" rx="2" :fill="c.color" />

        <rect :x="place(i).x + 16" :y="place(i).y + 16" width="40" height="40" rx="9" :fill="c.color" />
        <text :x="place(i).x + 36" :y="place(i).y + 44" text-anchor="middle" class="num">{{ c.n }}</text>

        <circle :cx="place(i).x + 90" :cy="place(i).y + 36" r="18"
          :fill="c.color" fill-opacity="0.14" :stroke="c.color" stroke-opacity="0.45" />
        <g class="ico" :stroke="c.color"
          :transform="'translate(' + (place(i).x + 77.4) + ' ' + (place(i).y + 23.4) + ') scale(1.05)'">
          <use :href="'#pf-' + c.icon" />
        </g>

        <text :x="place(i).x + 120" :y="lineY(c, CARD_H, place(i).y)" class="c-t">
          <tspan v-for="(t, k) in c.title" :key="k" :x="place(i).x + 120" :dy="k ? 15 : 0">{{ t }}</tspan>
        </text>
        <text v-if="c.sub.length" :x="place(i).x + 120"
          :y="lineY(c, CARD_H, place(i).y) + c.title.length * 15 + 2" class="c-s">
          <tspan v-for="(s, k) in c.sub" :key="k" :x="place(i).x + 120" :dy="k ? 12 : 0">{{ s }}</tspan>
        </text>
      </g>

      <!-- ============ the two that carry them ============ -->
      <g class="props" :class="{ on: enablers }">
        <path d="M249 358v-10h-8l12-14 12 14h-8v10z" fill="var(--s2)" opacity="0.7" />
        <path d="M739 358v-10h-8l12-14 12 14h-8v10z" fill="var(--s3)" opacity="0.7" />
      </g>

      <g v-for="(c, i) in BASE" :key="c.n" class="card base" :class="{ on: enablers }"
        :style="{ transitionDelay: (160 + i * 140) + 'ms' }">
        <rect :x="COL_X[i]" :y="BASE_Y" :width="CARD_W" :height="BASE_H" rx="12"
          :fill="c.color" fill-opacity="0.16" :stroke="c.color" stroke-opacity="0.55" />

        <rect :x="COL_X[i] + 14" :y="BASE_Y + 11" width="32" height="32" rx="8" :fill="c.color" />
        <text :x="COL_X[i] + 30" :y="BASE_Y + 34" text-anchor="middle" class="num sm">{{ c.n }}</text>

        <circle :cx="COL_X[i] + 78" :cy="BASE_Y + 27" r="16"
          fill="var(--oppo-bg-1)" :stroke="c.color" stroke-opacity="0.55" />
        <g class="ico" :stroke="c.color"
          :transform="'translate(' + (COL_X[i] + 66.8) + ' ' + (BASE_Y + 15.8) + ') scale(0.93)'">
          <use :href="'#pf-' + c.icon" />
        </g>

        <text :x="COL_X[i] + 106" :y="lineY(c, BASE_H, BASE_Y)" class="c-t">
          <tspan v-for="(t, k) in c.title" :key="k" :x="COL_X[i] + 106" :dy="k ? 15 : 0">{{ t }}</tspan>
        </text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.pf { width: 100%; display: flex; flex-direction: column; }
.stage { width: 100%; height: auto; }

.ico { fill: none; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }

.goal { opacity: 0.3; transition: opacity 620ms ease; }
.goal.on { opacity: 1; }
.goal-t { font-size: 13.5px; fill: var(--oppo-ink-1); }
.goal-t .hl { font-weight: 750; fill: var(--oppo-gold); }

.rise { opacity: 0; transition: opacity 560ms ease; }
.rise.on { opacity: 1; }
.rise.on .tip { animation: pf-lift 2.4s ease-in-out infinite; }
@keyframes pf-lift {
  0%, 100% { transform: translateY(0); opacity: 0.95; }
  50%      { transform: translateY(-4px); opacity: 0.55; }
}

.band-t { font-size: 11px; font-weight: 750; letter-spacing: 0.2em; fill: var(--oppo-gold); }

.card { opacity: 0; transform: translateY(14px);
  transition: opacity 520ms ease, transform 560ms cubic-bezier(.34, 1.3, .5, 1); }
.card.on { opacity: 1; transform: translateY(0); }
.card.base { transform: translateY(18px); }
.card.base.on { transform: translateY(0); }

.num { font-size: 21px; font-weight: 800; fill: var(--oppo-on-color); }
.num.sm { font-size: 17px; }

.c-t { font-size: 13.5px; font-weight: 700; letter-spacing: 0.035em; fill: var(--oppo-ink); }
.c-s { font-size: 11px; fill: var(--oppo-ink-2); letter-spacing: 0.01em; }

.props { opacity: 0; transition: opacity 520ms ease 420ms; }
.props.on { opacity: 1; }

@media (prefers-reduced-motion: reduce) {
  .rise.on .tip { animation: none; }
}
</style>
