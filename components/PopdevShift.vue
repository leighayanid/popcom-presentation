<script setup lang="ts">
/**
 * The paradigm shift, staged left to right.
 * step 0 - Population Management: a tally that only counts
 * step 1 - the PPD-POA 2023-2028 carries it across
 * step 2 - Population and Development: the count becomes a web of life chances
 * step 3 - the verdict on each side
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const crossing = computed(() => props.step >= 1)
const web = computed(() => props.step >= 2)
const verdict = computed(() => props.step >= 3)

// tally bars on the left - pure headcount, no meaning attached
const BARS = [52, 78, 41, 95, 66, 84, 58, 72]

// the development web on the right
const R = 80
const RAW = [
  { label: 'Health', color: 'var(--s3)' },
  { label: 'Education', color: 'var(--s2)' },
  { label: 'Livelihood', color: 'var(--s1)' },
  { label: 'Housing', color: 'var(--s4)' },
  { label: 'Mobility', color: 'var(--s5)' },
  { label: 'Services', color: 'var(--s6)' },
]
const NODES = RAW.map((n, i) => {
  const ang = (-90 + (360 / RAW.length) * i) * (Math.PI / 180)
  return { label: n.label, color: n.color, i, x: Math.cos(ang) * R, y: Math.sin(ang) * R }
})
</script>

<template>
  <div class="ps">
    <svg viewBox="0 0 1000 340" class="stage" role="img"
      aria-label="Population management becoming population and development">
      <defs>
        <linearGradient id="ps-bridge" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="var(--oppo-gold)" stop-opacity="0" />
          <stop offset="35%" stop-color="var(--oppo-gold)" stop-opacity="0.9" />
          <stop offset="100%" stop-color="var(--oppo-gold)" stop-opacity="0.9" />
        </linearGradient>
        <path id="ps-arc" d="M 300 150 C 400 60, 560 60, 660 150" />
      </defs>

      <!-- ============ LEFT: population management ============ -->
      <g class="side" :class="{ dim: verdict }">
        <text x="170" y="38" text-anchor="middle" class="side-title">POPULATION MANAGEMENT</text>
        <text x="170" y="56" text-anchor="middle" class="side-sub">HISTORICAL</text>

        <g transform="translate(60 230)">
          <rect v-for="(b, i) in BARS" :key="i"
            :x="i * 27" :y="-b" width="17" :height="b" rx="3"
            fill="var(--oppo-neutral)" class="tally" :style="{ animationDelay: (i * 0.22) + 's' }" />
          <line x1="-6" y1="2" x2="224" y2="2" stroke="var(--h-30)" stroke-width="1.2" />
        </g>

        <text x="170" y="272" text-anchor="middle" class="side-note">
          size &#183; growth &#183; demographic characteristics
        </text>
        <g class="strike" :class="{ on: verdict }">
          <line x1="52" y1="291" x2="288" y2="291" stroke="var(--s4)" stroke-width="1.6" />
          <text x="170" y="309" text-anchor="middle" class="side-verdict">controlling headcount</text>
        </g>
      </g>

      <!-- ============ BRIDGE: the PPD-POA ============ -->
      <g class="bridge" :class="{ on: crossing }">
        <use href="#ps-arc" fill="none" stroke="url(#ps-bridge)" stroke-width="2.2"
          stroke-linecap="round" class="arc" />
        <path d="M 652 142 L 664 150 L 652 158" fill="none" stroke="var(--oppo-gold)"
          stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
        <!-- carriers running the arc -->
        <template v-if="crossing">
          <circle v-for="k in 4" :key="k" r="3.4" fill="var(--oppo-gold)" opacity="0">
            <animateMotion dur="2.6s" repeatCount="indefinite" :begin="((k - 1) * 0.65) + 's'">
              <mpath href="#ps-arc" />
            </animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="2.6s"
              repeatCount="indefinite" :begin="((k - 1) * 0.65) + 's'" />
          </circle>
        </template>
        <rect x="406" y="68" width="148" height="21" rx="10.5" fill="var(--oppo-bg-1)"
          stroke="var(--g-50)" stroke-width="1" />
        <text x="480" y="83" text-anchor="middle" class="bridge-label">PPD-POA 2023&#8211;2028</text>
      </g>

      <!-- ============ RIGHT: population and development ============ -->
      <g class="side right" :class="{ on: web }">
        <text x="820" y="38" text-anchor="middle" class="side-title">POPULATION &amp; DEVELOPMENT</text>
        <text x="820" y="56" text-anchor="middle" class="side-sub accent">PRESENT</text>

        <g transform="translate(820 186)">
          <!-- links -->
          <line v-for="n in NODES" :key="'l' + n.i" x1="0" y1="0" :x2="n.x" :y2="n.y"
            stroke="var(--g-30)" stroke-width="1.1" class="link"
            :style="{ transitionDelay: (260 + n.i * 90) + 'ms' }" />
          <!-- travelling pulses along the links, inward -->
          <template v-if="web">
            <circle v-for="n in NODES" :key="'p' + n.i" r="2.6" :fill="n.color" opacity="0">
              <animate attributeName="cx" :values="n.x + ';0'" dur="2.2s"
                repeatCount="indefinite" :begin="(n.i * 0.3) + 's'" />
              <animate attributeName="cy" :values="n.y + ';0'" dur="2.2s"
                repeatCount="indefinite" :begin="(n.i * 0.3) + 's'" />
              <animate attributeName="opacity" values="0;1;1;0" dur="2.2s"
                repeatCount="indefinite" :begin="(n.i * 0.3) + 's'" />
            </circle>
          </template>
          <!-- hub -->
          <circle r="34" fill="var(--oppo-panel-2)" stroke="var(--g-60)" stroke-width="1.4" />
          <circle r="34" fill="none" stroke="var(--oppo-gold)" stroke-width="1" opacity="0.35" class="hub-ring" />
          <text y="-2" text-anchor="middle" class="hub-l">THE</text>
          <text y="12" text-anchor="middle" class="hub-l">PERSON</text>
          <!-- satellites -->
          <g v-for="n in NODES" :key="'n' + n.i" :transform="'translate(' + n.x + ' ' + n.y + ')'">
            <g class="node" :style="{ transitionDelay: (360 + n.i * 90) + 'ms' }">
              <circle r="7" :fill="n.color" opacity="0.9" />
              <text :y="n.y < -10 ? -15 : 21" text-anchor="middle" class="node-l">{{ n.label }}</text>
            </g>
          </g>
        </g>

        <text x="820" y="300" text-anchor="middle" class="side-note accent2">
          demographic dynamics &#183; dependency ratios &#183; household needs
        </text>
      </g>
    </svg>

    <div class="rail">
      <div class="rail-item" :class="{ on: verdict }">
        <span class="oppo-kicker">From</span>
        <strong>managing how many people we have</strong>
      </div>
      <div class="rail-item right" :class="{ on: verdict }" style="transition-delay: 220ms">
        <span class="oppo-kicker accent">To</span>
        <strong class="gold">human capital, workforce capability and economic growth</strong>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ps { width: 100%; display: flex; flex-direction: column; gap: 0.6rem; }
.stage { width: 100%; height: auto; }

.side { transition: opacity 700ms ease, filter 700ms ease; }
.side.dim { opacity: 0.42; filter: saturate(0.4); }
.side.right { opacity: 0; transition: opacity 700ms ease 120ms; }
.side.right.on { opacity: 1; }

.side-title { font-size: 14px; font-weight: 750; letter-spacing: 0.16em; fill: var(--oppo-ink); }
.side-sub { font-size: 10px; font-weight: 650; letter-spacing: 0.3em; fill: var(--oppo-ink-3); }
.side-sub.accent { fill: var(--oppo-gold); }
.side-note { font-size: 11px; fill: var(--oppo-ink-2); letter-spacing: 0.04em; }
.side-note.accent2 { fill: var(--oppo-ink-1); }
.side-verdict { font-size: 11px; font-weight: 650; letter-spacing: 0.1em; fill: var(--s4); }

.tally { animation: tally-breathe 2.8s ease-in-out infinite; transform-origin: bottom; }
@keyframes tally-breathe {
  0%, 100% { transform: scaleY(1); opacity: 0.75; }
  50%      { transform: scaleY(0.88); opacity: 1; }
}

.strike { opacity: 0; transition: opacity 600ms ease 300ms; }
.strike.on { opacity: 1; }
.strike line { stroke-dasharray: 240; stroke-dashoffset: 240; transition: stroke-dashoffset 700ms ease 400ms; }
.strike.on line { stroke-dashoffset: 0; }

.bridge { opacity: 0; transition: opacity 600ms ease; }
.bridge.on { opacity: 1; }
.arc { stroke-dasharray: 460; stroke-dashoffset: 460; transition: stroke-dashoffset 900ms ease 150ms; }
.bridge.on .arc { stroke-dashoffset: 0; }
.bridge-label { font-size: 10.5px; font-weight: 700; letter-spacing: 0.12em; fill: var(--oppo-gold); }

.link { stroke-dasharray: 100; stroke-dashoffset: 100; transition: stroke-dashoffset 620ms ease; }
.side.right.on .link { stroke-dashoffset: 0; }

.node { opacity: 0; transform: scale(0.4); transform-box: fill-box; transform-origin: center;
  transition: opacity 460ms ease, transform 560ms cubic-bezier(.34,1.5,.5,1); }
.side.right.on .node { opacity: 1; transform: scale(1); }

.hub-ring { animation: hub-ping 2.8s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes hub-ping {
  0%   { transform: scale(1); opacity: 0.5; }
  100% { transform: scale(1.75); opacity: 0; }
}
.hub-l { font-size: 10px; font-weight: 750; letter-spacing: 0.14em; fill: var(--oppo-gold); }
.node-l { font-size: 10.5px; font-weight: 600; fill: var(--oppo-ink-1); }

.rail { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; padding: 0 1rem; }
.rail-item {
  opacity: 0; transform: translateY(10px);
  transition: opacity 520ms ease, transform 520ms ease;
  display: flex; flex-direction: column; gap: 0.15rem;
}
.rail-item.on { opacity: 1; transform: translateY(0); }
.rail-item.right { text-align: right; align-items: flex-end; }
.rail-item strong { font-size: 0.9rem; font-weight: 600; color: var(--oppo-ink-1); }
.gold { color: var(--oppo-gold) !important; }
.accent { color: var(--oppo-gold); }
</style>
