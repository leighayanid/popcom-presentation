<script setup lang="ts">
/**
 * Bataeno Pass citizen registration, by LGU.
 *
 * Thirteen rows, so identity is carried by the name column and position - never
 * by thirteen hues. One series, one validated hue (var(--chart-bar)); the
 * residual "Others" bucket sits in var(--oppo-neutral) because it is not an LGU.
 * The single gold bar at step 3 is an annotation, not a category: it arrives
 * together with the sentence that explains it.
 *
 * Rows are ranked by magnitude rather than held alphabetical - the question this
 * slide answers is "where is the reach", not "look up my town".
 */
import { computed } from 'vue'
import Ticker from './Ticker.vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const TOTAL = 241984

// as reported by the Bataeno Pass registry dashboard
const LGUS = [
  { label: 'Mariveles', v: 51006 },
  { label: 'Dinalupihan', v: 28911 },
  { label: 'City of Balanga', v: 26251 },
  { label: 'Orion', v: 19701 },
  { label: 'Limay', v: 20051 },
  { label: 'Hermosa', v: 19167 },
  { label: 'Orani', v: 17668 },
  { label: 'Abucay', v: 14101 },
  { label: 'Pilar', v: 12384 },
  { label: 'Bagac', v: 11255 },
  { label: 'Morong', v: 11067 },
  { label: 'Samal', v: 9975 },
].sort((a, b) => b.v - a.v)

const OTHERS = { label: 'Others', v: 417, residual: true }
const ROWS = [...LGUS, OTHERS]

const MAX = 51006
const TICKS = [0, 10000, 20000, 30000, 40000, 50000]

const TOP3 = LGUS.slice(0, 3).reduce((s, r) => s + r.v, 0)

const pct = (v: number) => (v / TOTAL * 100).toFixed(1) + '%'

const bars = computed(() => props.step >= 1)
const total = computed(() => props.step >= 2)
const lead = computed(() => props.step >= 3)
</script>

<template>
  <div class="rr">
    <!-- ---------------------------------------------------- the ranked plot -->
    <section class="chart">
      <div class="chart-head">
        <span class="oppo-kicker">Registrants by city / municipality</span>
        <span class="oppo-fig-note">12 LGUs &#183; as of August 2026</span>
      </div>

      <div class="plot" :class="{ focus: lead }">
        <div class="overlay">
          <div v-for="t in TICKS" :key="t" class="gl" :class="{ zero: t === 0 }"
            :style="{ left: (t / MAX * 100) + '%' }" />
          <div v-if="bars" class="scan" />
        </div>

        <div v-for="(r, i) in ROWS" :key="r.label" class="row"
          :class="{ residual: r.residual, lead: lead && i === 0 }">
          <div class="r-name">{{ r.label }}</div>

          <div class="bar-area">
            <div class="bar" :style="{
              width: bars ? 'max(5px, ' + (r.v / MAX * 100) + '%)' : '0%',
              transitionDelay: (i * 70) + 'ms',
            }" />
          </div>

          <div class="val" :class="{ on: bars }" :style="{ transitionDelay: (i * 70 + 220) + 'ms' }">
            <span class="v"><Ticker :to="r.v" :active="bars" :dur="1100 + i * 60" /></span>
            <span class="pc">{{ pct(r.v) }}</span>
          </div>
        </div>

        <!-- axis sits under the bar column only -->
        <div class="axis">
          <div class="axis-rail">
            <span v-for="t in TICKS" :key="t" class="at" :style="{ left: (t / MAX * 100) + '%' }">
              {{ t === 0 ? '0' : (t / 1000) + 'k' }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- --------------------------------------------------------- the rail -->
    <aside class="rail">
      <div class="hero oppo-card" :class="{ on: total }">
        <div class="hero-top">
          <svg class="hero-ico" viewBox="0 0 32 32" aria-hidden="true">
            <circle cx="11" cy="10" r="4.4" />
            <circle cx="22" cy="11.5" r="3.4" />
            <path d="M3 25c0-4.4 3.6-7 8-7s8 2.6 8 7z" />
            <path d="M19.5 25c0-3.2 1.6-5.6 4.4-5.6S28 21.8 28 25z" />
          </svg>
          <span class="oppo-kicker">Total citizens</span>
        </div>
        <div class="hero-num"><Ticker :to="TOTAL" :active="total" :dur="1600" /></div>
        <div class="hero-sub">registrants province-wide</div>
      </div>

      <div class="note" :class="{ on: lead }">
        <div class="note-key"><span class="swatch" /> {{ pct(MAX) }}</div>
        <p>
          <strong>Mariveles</strong> alone carries one registrant in five. The three
          largest LGUs together account for
          <strong>{{ TOP3.toLocaleString('en-US') }}</strong> &#8212;
          {{ pct(TOP3) }} of the registry.
        </p>
      </div>

      <p class="foot" :class="{ on: total }">
        &#8220;Others&#8221; holds registrants recorded outside the twelve LGUs.
        Registration is continuing; figures move weekly.
      </p>
    </aside>
  </div>
</template>

<style scoped>
.rr {
  --c-name: 138px;
  --c-val: 104px;
  --c-gap: 0.75rem;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 268px;
  gap: 2rem;
  align-items: center;
}

.chart-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.45rem;
}

.plot { position: relative; }

/* recessive grid, clipped to the bar column */
.overlay {
  position: absolute;
  top: 0;
  bottom: 1.25rem;
  left: calc(var(--c-name) + var(--c-gap));
  right: calc(var(--c-val) + var(--c-gap));
  pointer-events: none;
}
.gl { position: absolute; top: 0; bottom: 0; width: 1px; background: var(--h-16); }
.gl.zero { background: var(--h-30); }

.scan {
  position: absolute; top: 0; bottom: 0; width: 2px;
  background: linear-gradient(to bottom, transparent, var(--g-60), transparent);
  left: 0;
  animation: scan 1.8s cubic-bezier(.3, .8, .4, 1) 1 forwards;
}
@keyframes scan {
  0%   { left: 0; opacity: 0; }
  12%  { opacity: 1; }
  88%  { opacity: 1; }
  100% { left: 100%; opacity: 0; }
}

.row {
  position: relative;
  display: grid;
  grid-template-columns: var(--c-name) 1fr var(--c-val);
  gap: 0 var(--c-gap);
  align-items: center;
  height: 36px;
}

.r-name {
  font-size: 1.05rem;
  line-height: 1.1;
  color: var(--oppo-ink-1);
  text-align: right;
  white-space: nowrap;
  transition: color 320ms ease;
}

.bar-area { position: relative; height: 19px; }
.bar {
  height: 19px;
  background: var(--chart-bar);
  border-radius: 0 4px 4px 0;
  transition: width 880ms cubic-bezier(.22, 1, .36, 1), background-color 420ms ease;
}

.val {
  position: relative;
  height: 1.2rem;
  opacity: 0;
  transition: opacity 400ms ease;
}
.val.on { opacity: 1; }
.v, .pc {
  position: absolute; inset: 0;
  text-align: right;
  font-variant-numeric: tabular-nums;
  transition: opacity 180ms ease;
}
.v { font-size: 1.2rem; font-weight: 700; color: var(--oppo-ink); }
.pc { font-size: 1.02rem; font-weight: 600; color: var(--oppo-gold); opacity: 0; }
.row:hover .v { opacity: 0; }
.row:hover .pc { opacity: 1; }

/* the residual bucket is not an LGU, and does not read like one */
.row.residual { margin-top: 0.3rem; }
.row.residual::before {
  content: "";
  position: absolute;
  top: -0.15rem;
  left: calc(var(--c-name) + var(--c-gap));
  right: 0;
  height: 1px;
  background: var(--h-11);
}
.row.residual .r-name { color: var(--oppo-ink-3); font-style: italic; }
.row.residual .bar { background: var(--oppo-neutral); }
.row.residual .v { color: var(--oppo-ink-2); font-weight: 600; }

/* step 3 — one annotated mark, arriving with its sentence.
   The hue shift alone is too small a step in light mode, so the focus is
   carried by contrast against a receded field, which holds in both themes. */
.plot.focus .bar { opacity: 0.4; }
.plot.focus .row.lead .bar { opacity: 1; background: var(--oppo-gold-fig); }
.plot.focus .r-name { color: var(--oppo-ink-3); }
.plot.focus .row.lead .r-name { color: var(--oppo-ink); font-weight: 700; }
.bar, .r-name { transition-property: width, background-color, opacity, color; }

.axis { position: relative; height: 1.25rem; }
.axis-rail {
  position: absolute;
  top: 0.3rem;
  left: calc(var(--c-name) + var(--c-gap));
  right: calc(var(--c-val) + var(--c-gap));
}
.at {
  position: absolute;
  transform: translateX(-50%);
  font-size: 0.8rem;
  color: var(--oppo-ink-2);
  font-variant-numeric: tabular-nums;
}

/* ------------------------------------------------------------------ rail */
.rail { display: flex; flex-direction: column; gap: 0.85rem; }

.hero, .note, .foot {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 520ms ease, transform 520ms cubic-bezier(.22, 1, .36, 1);
}
.hero.on, .note.on, .foot.on { opacity: 1; transform: translateY(0); }

.hero { border-color: var(--g-28); background: linear-gradient(160deg, var(--grad-a), var(--grad-b)); }
.hero-top { display: flex; align-items: center; gap: 0.5rem; }
.hero-ico { width: 20px; height: 20px; fill: var(--oppo-gold-fig); flex: none; }
.hero-num {
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.05;
  color: var(--oppo-gold);
  margin-top: 0.35rem;
}
.hero-sub { font-size: 0.92rem; color: var(--oppo-ink-2); margin-top: 0.15rem; }

.note { transition-delay: 120ms; }
.note-key {
  display: flex; align-items: center; gap: 0.45rem;
  font-size: 1.22rem; font-weight: 750; color: var(--oppo-ink);
  font-variant-numeric: tabular-nums;
}
.swatch {
  width: 11px; height: 11px; border-radius: 3px;
  background: var(--oppo-gold-fig); flex: none;
}
.note p { font-size: 0.92rem; line-height: 1.45; color: var(--oppo-ink-2); margin-top: 0.3rem; }

.foot {
  font-size: 0.86rem;
  line-height: 1.4;
  color: var(--oppo-ink-2);
  transition-delay: 240ms;
  margin-top: auto;
}
</style>
