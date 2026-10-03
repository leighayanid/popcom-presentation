<script setup lang="ts">
/**
 * The Province of Bataan 2030 Strategy Map, rebuilt so it can be staged.
 * The perspectives rise from the bottom in the order they actually support
 * one another - Organization carries Internal Process carries Finance
 * carries Constituency - and the last step lights only the objectives this
 * Office's PPAs answer to.
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

function wrap(t: string, max: number) {
  const words = t.split(' ')
  const lines: string[] = []
  let cur = ''
  for (const w of words) {
    if ((cur + ' ' + w).trim().length > max && cur) { lines.push(cur); cur = w }
    else cur = (cur + ' ' + w).trim()
  }
  if (cur) lines.push(cur)
  return lines
}

const L = 132 // left edge of the box field
const RW = 854 // field width

function row(n: number, gap = 10) {
  const w = (RW - gap * (n - 1)) / n
  return Array.from({ length: n }, (_, i) => ({ x: L + i * (w + gap), w }))
}

const CONSTITUENCY = [
  { t: 'Ensure easier access to rights-based and needs-based social protection and development services', mine: true },
  { t: 'Guarantee integration of Province-wide health system for the effective UHC implementation', mine: false },
  { t: 'Sustain the synergy among stakeholders to sponsor programs for continuous workforce and livelihood development', mine: false },
].map((b, i) => ({ ...b, ...row(3)[i], y: 66, h: 72, fill: 'var(--sm-const)', max: 34 }))

const FINANCE = [
  { t: 'Effectively implement policies on resource mobilization', mine: false, x: L, w: RW, y: 150, h: 42, fill: 'var(--sm-fin)', max: 90 },
]

const PROCESS = [
  { t: 'Enhance access and connectivity to and from tourism and investment destination', mine: false },
  { t: 'Promote industrial peace and sustain business-friendly environment', mine: false },
  { t: 'Harmonize national and local programs, plans and policies', mine: true },
  { t: 'Engage stakeholders as partners in the implementation of PPPAs', mine: true },
  { t: 'Provide a peaceful, safe, and secured community', mine: false },
  { t: 'Improve Environmental Quality and safeguard Ecosystem Integrity', mine: false },
].map((b, i) => ({ ...b, ...row(6, 8)[i], y: 204, h: 84, fill: 'var(--sm-proc)', max: 17 }))

const ORG = [
  { t: 'Establish and nurture an engaged, empowered and responsive workforce', mine: false, x: L, w: RW, y: 300, h: 42, fill: 'var(--sm-org)', max: 90 },
]

const BANDS = [
  { key: 'const', lines: ['CONSTITUENCY'], y: 66, h: 72, fill: 'var(--sm-const)', at: 4 },
  { key: 'fin', lines: ['FINANCE'], y: 150, h: 42, fill: 'var(--sm-fin)', at: 3 },
  { key: 'proc', lines: ['INTERNAL', 'PROCESS'], y: 204, h: 84, fill: 'var(--sm-proc)', at: 2 },
  { key: 'org', lines: ['ORGANIZATION'], y: 300, h: 42, fill: 'var(--sm-org)', at: 1 },
]

const ROWS = computed(() => [
  { at: 1, boxes: ORG },
  { at: 2, boxes: PROCESS },
  { at: 3, boxes: FINANCE },
  { at: 4, boxes: CONSTITUENCY },
])

const focused = computed(() => props.step >= 5)
const shown = (at: number) => props.step >= at

function chev(y: number, h: number) {
  // a narrow upward chevron hugging the left margin; the label sits beside it
  const x1 = 10
  const x2 = 34
  const mid = (x1 + x2) / 2
  return `M ${x1} ${y + h} L ${x1} ${y + 10} L ${mid} ${y - 5} L ${x2} ${y + 10} L ${x2} ${y + h} Z`
}
</script>

<template>
  <div class="sm">
    <svg viewBox="0 0 1000 410" class="map" role="img"
      aria-label="Province of Bataan 2030 Strategy Map with the objectives this Office answers to highlighted">
      <defs>
        <filter id="sm-lift" x="-30%" y="-30%" width="160%" height="160%">
          <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="var(--oppo-gold)" flood-opacity="0.45" />
        </filter>
      </defs>

      <!-- vision banner -->
      <g class="vision" :class="{ on: shown(0) }">
        <rect x="10" y="2" width="616" height="50" rx="5" fill="var(--oppo-bg-2)"
          stroke="var(--h-20)" stroke-width="1" />
        <text x="24" y="19" class="vis-k">VISION</text>
        <text x="24" y="33" class="vis-t">
          By 2030, Bataan is a highly livable Province and home to diverse economic
        </text>
        <text x="24" y="45" class="vis-t">investments resulting in resilient families</text>
        <rect x="640" y="2" width="346" height="50" rx="5" fill="var(--oppo-panel-2)"
          stroke="var(--g-35)" stroke-width="1" />
        <text x="813" y="24" text-anchor="middle" class="map-t">PROVINCE OF BATAAN</text>
        <text x="813" y="42" text-anchor="middle" class="map-s">2030 STRATEGY MAP</text>
      </g>

      <!-- perspective chevrons -->
      <g v-for="b in BANDS" :key="b.key" class="band" :class="{ on: shown(b.at) }"
        :style="{ transitionDelay: (b.at * 60) + 'ms' }">
        <path :d="chev(b.y, b.h)" :fill="b.fill" opacity="0.22"
          :stroke="b.fill" stroke-width="1.1" />
        <text :x="44" :y="b.y + b.h / 2 - (b.lines.length - 1) * 5 + 3" class="band-l">
          <tspan v-for="(ln, li) in b.lines" :key="li" x="44" :dy="li === 0 ? 0 : 10">{{ ln }}</tspan>
        </text>
      </g>

      <!-- objective boxes -->
      <g v-for="r in ROWS" :key="r.at">
        <g v-for="(b, i) in r.boxes" :key="i" class="box"
          :class="{ on: shown(r.at), mine: focused && b.mine, muted: focused && !b.mine }"
          :style="{ transitionDelay: (r.at * 60 + i * 55) + 'ms' }">
          <rect :x="b.x" :y="b.y" :width="b.w" :height="b.h" rx="8"
            :fill="b.fill" fill-opacity="0.82" stroke="var(--sm-edge)" stroke-width="1" />
          <rect class="halo" :x="b.x - 2" :y="b.y - 2" :width="b.w + 4" :height="b.h + 4" rx="10"
            fill="none" stroke="var(--oppo-gold)" stroke-width="1.8" />
          <text :x="b.x + b.w / 2" :y="b.y + b.h / 2 - (wrap(b.t, b.max).length - 1) * 5.45 + 3"
            text-anchor="middle" class="box-t">
            <tspan v-for="(ln, li) in wrap(b.t, b.max)" :key="li"
              :x="b.x + b.w / 2" :dy="li === 0 ? 0 : 10.9">{{ ln }}</tspan>
          </text>
          <g v-if="b.mine" class="chip" :transform="'translate(' + (b.x + b.w - 26) + ' ' + (b.y + 11) + ')'">
            <circle r="7" fill="var(--oppo-gold)" />
            <circle r="7" fill="none" stroke="var(--oppo-gold)" stroke-width="1.2" class="chip-ping" />
          </g>
        </g>
      </g>

      <!-- mission / core values -->
      <g class="foot" :class="{ on: shown(1) }">
        <rect x="10" y="354" width="482" height="50" rx="5" fill="var(--oppo-bg-2)"
          stroke="var(--h-16)" stroke-width="1" />
        <text x="24" y="371" class="vis-k">MISSION</text>
        <text x="24" y="386" class="vis-t">
          Excellent public service that upholds the general welfare
        </text>
        <text x="24" y="398" class="vis-t">through participatory and proactive governance.</text>
        <rect x="504" y="354" width="482" height="50" rx="5" fill="var(--oppo-bg-2)"
          stroke="var(--h-16)" stroke-width="1" />
        <text x="518" y="371" class="vis-k">CORE VALUES</text>
        <text x="518" y="392" class="vis-t">
          Integrity &#183; Commitment &#183; Humility &#183; Innovation &#183; Unity &#183; Patriotism
        </text>
      </g>
    </svg>

    <div class="focus-note" :class="{ on: focused }">
      <span class="oppo-tag">Where our PPAs land</span>
      <span><strong>Constituency</strong> &#8212; easier access to rights-based and needs-based services.
        <strong>Internal Process</strong> &#8212; harmonise national and local programmes, and engage
        stakeholders as partners in implementation.</span>
    </div>
  </div>
</template>

<style scoped>
.sm { width: 100%; display: flex; flex-direction: column; gap: 0.55rem; }
.map { width: 100%; height: auto; }

.vision, .foot { opacity: 0; transition: opacity 600ms ease; }
.vision.on, .foot.on { opacity: 1; }

.vis-k { font-size: 9.5px; font-weight: 750; letter-spacing: 0.2em; fill: var(--oppo-gold); }
.vis-t { font-size: 11.5px; fill: var(--oppo-ink-1); }
.map-t { font-size: 16px; font-weight: 800; letter-spacing: 0.06em; fill: var(--oppo-ink); }
.map-s { font-size: 12px; font-weight: 650; letter-spacing: 0.18em; fill: var(--oppo-gold); }

.band {
  opacity: 0; transform: translateY(26px);
  transition: opacity 560ms ease, transform 640ms cubic-bezier(.22,1,.36,1);
}
.band.on { opacity: 1; transform: translateY(0); }
/* tracking is tight here because "CONSTITUENCY" has to clear the first box
   of its own band at this size */
.band-l { font-size: 9.5px; font-weight: 750; letter-spacing: 0.035em; fill: var(--oppo-ink-1); }

.box {
  opacity: 0; transform: translateY(26px);
  transition: opacity 540ms ease, transform 660ms cubic-bezier(.22,1,.36,1), filter 500ms ease;
}
.box.on { opacity: 1; transform: translateY(0); }
.box.muted > rect:first-of-type { fill-opacity: 0.2; stroke-opacity: 0.12; }
.box.muted .box-t { fill: var(--oppo-on-color-muted); }
.box.mine { filter: url(#sm-lift); }

.halo { opacity: 0; transition: opacity 420ms ease 160ms; }
.box.mine .halo { opacity: 1; }

.box-t { font-size: 10.6px; font-weight: 600; fill: var(--oppo-on-color); letter-spacing: 0.002em;
  transition: fill 500ms ease; }

.chip { opacity: 0; transition: opacity 400ms ease 260ms; }
.box.mine .chip { opacity: 1; }
.chip-ping { animation: chip-ping 2.4s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes chip-ping {
  0%   { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(2.1); opacity: 0; }
}

.focus-note {
  display: flex; align-items: center; gap: 0.8rem;
  font-size: 0.95rem; color: var(--oppo-ink-2); line-height: 1.4;
  opacity: 0; transform: translateY(8px);
  transition: opacity 500ms ease 200ms, transform 500ms ease 200ms;
}
.focus-note.on { opacity: 1; transform: translateY(0); }
.focus-note strong { color: var(--oppo-gold); }
.focus-note .oppo-tag { flex: none; }
</style>
