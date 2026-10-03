<script setup lang="ts">
/**
 * The legal mandate, drawn as four icon medallions standing on one
 * foundation — the Local Government Code.
 * step 1 - the four marks land, left to right
 * step 2 - the mandated function is spelled out under each
 * step 3 - the foundation lights and the marks come alive
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const risen = computed(() => props.step >= 1)
const worded = computed(() => props.step >= 2)
const alive = computed(() => props.step >= 3)

// `ink` overrides `color` for the wording where the fill-role colour is too
// bright to carry text on paper (see the -gold / -gold-fig split in the tokens)
type Fn = { key: string; icon: string; color: string; ink?: string; lead: string[]; tail: string[] }

// the four mandated functions, as the Code words them
const FUNCTIONS: Fn[] = [
  {
    key: 'integrate', icon: 'policy', color: 'var(--s2)',
    lead: ['Integrate population', 'development principles'],
    tail: ['into provincial policies,', 'strategies, and', 'development plans.'],
  },
  {
    key: 'promote', icon: 'family', color: 'var(--s3)',
    lead: ['Promote responsible', 'parenthood'],
    tail: ['and family well-being.'],
  },
  {
    key: 'implement', icon: 'training', color: 'var(--s1)', ink: 'var(--oppo-gold)',
    lead: ['Implement localized', 'capacity-building', 'initiatives.'],
    tail: [],
  },
  {
    key: 'maintain', icon: 'databank', color: 'var(--s5)',
    lead: ['Maintain a comprehensive', 'population databank'],
    tail: ['for evidence-based', 'provincial planning and', 'service implementation.'],
  },
]

// four columns on a 1000 x 400 stage
const CX = [125, 375, 625, 875]
const DIVIDER = [250, 500, 750]
const DISC_CY = 96
const R = 44

const LEAD_TOP = 176
const LEAD_STEP = 20
const TAIL_STEP = 17

const tailTop = (f: Fn) => LEAD_TOP + f.lead.length * LEAD_STEP + 3
</script>

<template>
  <div class="mp">
    <svg viewBox="0 0 1000 400" class="stage" role="img"
      aria-label="The four functions the Local Government Code mandates of the Office of the Provincial Population Officer">
      <defs>
        <clipPath id="mp-panel">
          <rect x="8" y="4" width="984" height="392" rx="22" />
        </clipPath>

        <linearGradient id="mp-base" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="var(--g-07)" />
          <stop offset="50%" stop-color="var(--g-20)" />
          <stop offset="100%" stop-color="var(--g-07)" />
        </linearGradient>

        <!-- the four marks, drawn once on a 24-unit grid -->
        <g id="mp-policy">
          <path d="M5.8 2.6h7.4L18.4 7.8v9.4H5.8z" />
          <path d="M13.2 2.6v5.2h5.2" />
          <path d="M8.6 10.2h6M8.6 13.4h4.4" />
          <circle cx="16.8" cy="17.4" r="3.4" />
          <path d="M16.8 12.9v1.4M16.8 20.5v1.4M12.3 17.4h1.4M19.9 17.4h1.4" />
        </g>
        <g id="mp-family">
          <path fill="currentColor" stroke="none" d="M12 7.5c-2-1.5-3.4-2.5-3.4-4 0-1.1 1-2 2-2 .6 0 1.1.3 1.4.7.3-.4.8-.7 1.4-.7 1 0 2 .9 2 2 0 1.5-1.4 2.5-3.4 4z" />
          <circle cx="5.2" cy="9.4" r="2.1" />
          <path d="M1.9 20.2v-6a3.3 3.3 0 0 1 6.6 0v6" />
          <circle cx="18.8" cy="9.4" r="2.1" />
          <path d="M15.5 20.2v-6a3.3 3.3 0 0 1 6.6 0v6" />
          <circle cx="12" cy="12.6" r="1.8" />
          <path d="M9.5 20.2v-3.6a2.5 2.5 0 0 1 5 0v3.6" />
        </g>
        <g id="mp-training">
          <path d="M8.6 2.4h12.6v8.8H8.6z" />
          <path d="M11.4 5.6h7M11.4 8.2h4.6" />
          <circle cx="4.4" cy="4.2" r="2" />
          <path d="M1.4 12.2V7.8a3 3 0 0 1 6 0v1.1" />
          <path d="M7.4 8.1h1.2" />
          <circle cx="5" cy="16.4" r="1.8" />
          <path d="M2.4 21.8v-1.2a2.6 2.6 0 0 1 5.2 0v1.2" />
          <circle cx="12" cy="16.4" r="1.8" />
          <path d="M9.4 21.8v-1.2a2.6 2.6 0 0 1 5.2 0v1.2" />
          <circle cx="19" cy="16.4" r="1.8" />
          <path d="M16.4 21.8v-1.2a2.6 2.6 0 0 1 5.2 0v1.2" />
        </g>
        <g id="mp-databank">
          <ellipse cx="10" cy="5" rx="6.6" ry="2.7" />
          <path d="M3.4 5v10.4c0 1.5 3 2.7 6.6 2.7.8 0 1.6-.06 2.3-.18" />
          <path d="M3.4 10.2c0 1.5 3 2.7 6.6 2.7.5 0 1-.02 1.5-.07" />
          <circle cx="17.4" cy="16.6" r="4.8" />
          <path d="M15.6 18.3v-2M17.4 18.3v-3.6M19.2 18.3v-1.3" />
        </g>
      </defs>

      <!-- ============ backdrop: the provincial ground ============ -->
      <g class="backdrop" aria-hidden="true">
        <rect x="8" y="4" width="984" height="392" rx="22" fill="var(--oppo-bg-0)" opacity="0.45" />
        <g clip-path="url(#mp-panel)">
          <circle cx="104" cy="72" r="120" fill="var(--s2-45)" opacity="0.09" />
          <circle cx="912" cy="60" r="104" fill="var(--g-07)" opacity="0.7" />
          <!-- a low civic skyline: the province the mandate sits over -->
          <g fill="var(--h-10)" opacity="0.5" transform="translate(0 26)">
            <path d="M96 318h10v-44l5-9 5 9v44h10v12H96z" />
            <path d="M212 330v-28h46v-18l23-13 23 13v18h46v28z" />
            <path d="M640 330v-34h18v-12h12v12h18v34z" />
            <path d="M742 330v-40h14v-10h12v10h14v40z" />
            <path d="M826 330v-26h58v-14h12v14h22v26z" />
          </g>
          <path d="M0 352c132-24 192 16 320 5s176-36 310-27 180 38 370 9v61H0z" fill="var(--s2-45)" opacity="0.12" />
          <path d="M0 368c148-20 208 13 332 4s182-29 306-22 196 31 362 5v45H0z" fill="var(--g-16)" opacity="0.45" />
        </g>
        <rect x="8" y="4" width="984" height="392" rx="22" fill="none" stroke="var(--h-10)" />
      </g>

      <!-- ============ the hairlines between the four ============ -->
      <g class="rules" :class="{ on: risen }">
        <line v-for="x in DIVIDER" :key="x" :x1="x" y1="52" :x2="x" y2="286"
          stroke="var(--h-14)" stroke-width="1" />
      </g>

      <!-- ============ the four functions ============ -->
      <g v-for="(f, i) in FUNCTIONS" :key="f.key">
        <!-- the mark -->
        <g class="mark" :class="{ on: risen }" :style="{ transitionDelay: (140 + i * 130) + 'ms' }">
          <ellipse :cx="CX[i] - 10" cy="82" rx="54" ry="45" :fill="f.color" opacity="0.1"
            :transform="'rotate(-16 ' + (CX[i] - 10) + ' 82)'" />
          <circle class="halo" :class="{ on: alive }" :cx="CX[i]" :cy="DISC_CY" :r="R"
            fill="none" :stroke="f.color" stroke-width="2"
            :style="{ animationDelay: (i * 0.55) + 's' }" />
          <circle :cx="CX[i]" :cy="DISC_CY" :r="R" :fill="f.color" fill-opacity="0.16"
            :stroke="f.color" stroke-opacity="0.75" stroke-width="2" />
          <g class="ico" :stroke="f.color" :style="{ color: f.color }"
            :transform="'translate(' + (CX[i] - 17.4) + ' ' + (DISC_CY - 17.4) + ') scale(1.45)'">
            <use :href="'#mp-' + f.icon" />
          </g>
        </g>

        <!-- what it asks of this Office -->
        <g class="words" :class="{ on: worded }" :style="{ transitionDelay: (120 + i * 110) + 'ms' }">
          <text :x="CX[i]" :y="LEAD_TOP" text-anchor="middle" class="lead" :fill="f.ink ?? f.color">
            <tspan v-for="(t, k) in f.lead" :key="k" :x="CX[i]" :dy="k ? LEAD_STEP : 0">{{ t }}</tspan>
          </text>
          <text v-if="f.tail.length" :x="CX[i]" :y="tailTop(f)" text-anchor="middle" class="tail">
            <tspan v-for="(t, k) in f.tail" :key="k" :x="CX[i]" :dy="k ? TAIL_STEP : 0">{{ t }}</tspan>
          </text>
        </g>
      </g>

      <!-- ============ the one foundation ============ -->
      <g class="base" :class="{ on: alive }">
        <rect x="120" y="316" width="760" height="46" rx="13" fill="url(#mp-base)"
          stroke="var(--g-45)" stroke-width="1.2" />
        <text x="500" y="338" text-anchor="middle" class="base-t">
          LOCAL GOVERNMENT CODE OF 1991 &#183; REPUBLIC ACT NO. 7160
        </text>
        <text x="500" y="353" text-anchor="middle" class="base-s">
          The one mandate all four functions stand on
        </text>
      </g>
    </svg>

    <div class="foot">
      <span class="oppo-tag">LEGAL MANDATE</span>
      <span class="oppo-fig-note">
        What the Code asks of the Office of the Provincial Population Officer &#8212;
        <strong>integrate</strong>, <strong>promote</strong>, <strong>implement</strong>, <strong>maintain</strong>.
      </span>
    </div>
  </div>
</template>

<style scoped>
.mp { width: 100%; display: flex; flex-direction: column; gap: 0.45rem; }
.stage { width: 100%; height: auto; }

.ico { fill: none; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }

.rules { opacity: 0; transition: opacity 620ms ease 240ms; }
.rules.on { opacity: 1; }

.mark {
  opacity: 0;
  transform: translateY(22px) scale(0.9);
  transform-box: fill-box;
  transform-origin: center;
  transition: opacity 520ms ease, transform 640ms cubic-bezier(.34, 1.3, .5, 1);
}
.mark.on { opacity: 1; transform: translateY(0) scale(1); }

.halo { opacity: 0; transform-box: fill-box; transform-origin: center; }
.halo.on { animation: mp-pulse 3.2s ease-out infinite; }
@keyframes mp-pulse {
  0%        { opacity: 0.5; transform: scale(1); }
  70%, 100% { opacity: 0; transform: scale(1.26); }
}

.words { opacity: 0; transform: translateY(12px);
  transition: opacity 520ms ease, transform 560ms cubic-bezier(.22, 1, .36, 1); }
.words.on { opacity: 1; transform: translateY(0); }

.lead { font-size: 16px; font-weight: 750; letter-spacing: 0.005em; }
.tail { font-size: 14px; fill: var(--oppo-ink-2); }

.base { opacity: 0.25; transition: opacity 620ms ease; }
.base.on { opacity: 1; }
.base-t { font-size: 13px; font-weight: 750; letter-spacing: 0.17em; fill: var(--oppo-gold); }
.base-s { font-size: 11.5px; letter-spacing: 0.07em; fill: var(--oppo-ink-2); }

@media (prefers-reduced-motion: reduce) {
  .halo.on { animation: none; }
}
</style>
