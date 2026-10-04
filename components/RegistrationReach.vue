<script setup lang="ts">
/**
 * Bataeno Pass citizen registration, by LGU.
 *
 * Two readings of the same twelve rows, side by side. The left plot ranks raw
 * registrants; the right plot gives each LGU's registrants as a share of its
 * own population. They disagree, and the disagreement is the point - the three
 * largest registries are also the three largest towns, so volume alone says
 * nothing about reach.
 *
 * One series, one validated hue (var(--chart-bar)); the residual "Others"
 * bucket sits in var(--oppo-neutral) because it is not an LGU and has no
 * denominator. On the coverage track the only encoded distinction is
 * above/below the province-wide rate - a binary, not twelve hues.
 *
 * Rows stay ranked by registrant count: the coverage dots then visibly refuse
 * to follow that order, which is what the slide is for.
 */
import { computed } from 'vue'
import Ticker from './Ticker.vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const TOTAL = 241984
const TARGET = 887772          // household population target, province-wide
const REACH = TOTAL / TARGET * 100

// registrants as reported by the Bataeno Pass registry dashboard;
// pop = 2024 POPCEN count for the same city / municipality
const LGUS = [
  { label: 'Mariveles', v: 51006, pop: 156200 },
  { label: 'Dinalupihan', v: 28911, pop: 124188 },
  { label: 'City of Balanga', v: 26251, pop: 109931 },
  { label: 'Limay', v: 20051, pop: 81960 },
  { label: 'Orion', v: 19701, pop: 63044 },
  { label: 'Hermosa', v: 19167, pop: 80557 },
  { label: 'Orani', v: 17668, pop: 72941 },
  { label: 'Abucay', v: 14101, pop: 44846 },
  { label: 'Pilar', v: 12384, pop: 47107 },
  { label: 'Bagac', v: 11255, pop: 32799 },
  { label: 'Morong', v: 11067, pop: 37024 },
  { label: 'Samal', v: 9975, pop: 40843 },
].sort((a, b) => b.v - a.v)

const OTHERS = { label: 'Others', v: 417, pop: 0, residual: true }

const ROWS = [...LGUS, OTHERS].map(r => ({
  ...r,
  cov: r.pop ? r.v / r.pop * 100 : null,
}))

const MAX = 51006
const TICKS = [0, 10000, 20000, 30000, 40000, 50000]

const COV_MAX = 40                      // the coverage track runs 0-40%
const COV_TICKS = [0, 10, 20, 30, 40]
const covX = (p: number) => p / COV_MAX * 100

const pc1 = (n: number) => n.toFixed(1) + '%'

const bars = computed(() => props.step >= 1)
const total = computed(() => props.step >= 2)
const cover = computed(() => props.step >= 3)
</script>

<template>
  <div class="rr">
    <!-- ---------------------------------------------------- the ranked plot -->
    <section class="chart">
      <div class="chart-head">
        <span class="oppo-kicker">Registrants by city / municipality</span>
        <span class="oppo-fig-note">12 LGUs &#183; as of August 2026</span>
      </div>

      <div class="plot" :class="{ shift: cover }">
        <!-- column captions, so the two readings are never confused -->
        <div class="caps">
          <span class="cap cap-bar">Registrants</span>
          <span class="cap cap-cov" :class="{ on: cover }">Coverage rate</span>
        </div>

        <div class="overlay">
          <div v-for="t in TICKS" :key="t" class="gl" :class="{ zero: t === 0 }"
            :style="{ left: (t / MAX * 100) + '%' }" />
          <div v-if="bars" class="scan" />
        </div>

        <!-- the province-wide rate, drawn once through the coverage column -->
        <div class="cov-overlay" :class="{ on: cover }">
          <div v-for="t in COV_TICKS" :key="t" class="gl" :class="{ zero: t === 0 }"
            :style="{ left: covX(t) + '%' }" />
          <div class="benchmark" :style="{ left: covX(REACH) + '%' }">
            <span class="benchmark-tag">Province {{ REACH.toFixed(2) }}%</span>
          </div>
        </div>

        <div v-for="(r, i) in ROWS" :key="r.label" class="row"
          :class="{ residual: r.residual }">
          <div class="r-name">{{ r.label }}</div>

          <div class="bar-area">
            <div class="bar" :style="{
              width: bars ? 'max(5px, ' + (r.v / MAX * 100) + '%)' : '0%',
              transitionDelay: (i * 70) + 'ms',
            }" />
          </div>

          <div class="val" :class="{ on: bars }" :style="{ transitionDelay: (i * 70 + 220) + 'ms' }">
            <Ticker :to="r.v" :active="bars" :dur="1100 + i * 60" />
          </div>

          <!-- coverage: a lollipop on a shared 0-40% scale -->
          <div class="cov-area">
            <template v-if="r.cov !== null">
              <div class="lolli" :class="{ on: cover, over: r.cov >= REACH }" :style="{
                width: cover ? covX(r.cov) + '%' : '0%',
                transitionDelay: (i * 55) + 'ms',
              }" />
              <div class="dot" :class="{ on: cover, over: r.cov >= REACH }" :style="{
                left: covX(r.cov) + '%',
                transitionDelay: (i * 55 + 160) + 'ms',
              }" />
            </template>
          </div>

          <div class="cov-val" :class="{ on: cover, over: r.cov !== null && r.cov >= REACH }"
            :style="{ transitionDelay: (i * 55 + 220) + 'ms' }">
            <span v-if="r.cov === null">&#8212;</span>
            <span v-else>{{ pc1(r.cov) }}</span>
          </div>
        </div>

        <!-- axes sit under their own columns -->
        <div class="axis">
          <div class="axis-rail bar-rail">
            <span v-for="t in TICKS" :key="t" class="at" :style="{ left: (t / MAX * 100) + '%' }">
              {{ t === 0 ? '0' : (t / 1000) + 'k' }}
            </span>
          </div>
          <div class="axis-rail cov-rail" :class="{ on: cover }">
            <span v-for="t in COV_TICKS" :key="t" class="at" :style="{ left: covX(t) + '%' }">
              {{ t }}%
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
          <span class="oppo-kicker">Current population reach</span>
        </div>

        <div class="hero-num">
          <Ticker :to="REACH" :active="total" :dur="1600" :decimals="2" suffix="%" />
        </div>

        <div class="meter">
          <div class="meter-fill" :style="{ width: total ? REACH + '%' : '0%' }" />
        </div>

        <dl class="hero-grid">
          <div>
            <dt>Registered individuals</dt>
            <dd>{{ TOTAL.toLocaleString('en-US') }}</dd>
          </div>
          <div>
            <dt>Household population target</dt>
            <dd>{{ TARGET.toLocaleString('en-US') }}</dd>
          </div>
        </dl>
      </div>

      <p class="foot" :class="{ on: total }">
        &#8220;Others&#8221; holds registrants recorded outside the twelve LGUs and so has
        no denominator. LGU rates are measured against 2024 POPCEN population.
        Registration is continuing; figures move weekly.
      </p>
    </aside>
  </div>
</template>

<style scoped>
.rr {
  --c-name: 126px;
  --c-val: 74px;
  --c-cov: 300px;
  --c-covval: 54px;
  --c-gap: 0.7rem;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 254px;
  gap: 1.6rem;
  align-items: center;
}

.chart-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.3rem;
}

.plot { position: relative; }

/* ------------------------------------------------------- column captions */
.caps {
  display: grid;
  grid-template-columns: var(--c-name) 1fr var(--c-val) var(--c-cov) var(--c-covval);
  gap: 0 var(--c-gap);
  margin-bottom: 0.3rem;
  height: 1.05rem;
}
.cap {
  font-size: 0.74rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--oppo-ink-3);
  white-space: nowrap;
}
.cap-bar { grid-column: 2; }
.cap-cov {
  grid-column: 4 / span 2;
  opacity: 0;
  transition: opacity 420ms ease;
}
.cap-cov.on { opacity: 1; color: var(--oppo-gold); font-weight: 650; }

/* recessive grid, clipped to each plot column */
.overlay, .cov-overlay {
  position: absolute;
  top: 1.35rem;
  bottom: 1.25rem;
  pointer-events: none;
}
.overlay {
  left: calc(var(--c-name) + var(--c-gap));
  right: calc(var(--c-val) + var(--c-cov) + var(--c-covval) + var(--c-gap) * 3);
}
.cov-overlay {
  left: calc(100% - var(--c-cov) - var(--c-covval) - var(--c-gap));
  right: calc(var(--c-covval) + var(--c-gap));
  opacity: 0;
  transition: opacity 480ms ease;
}
.cov-overlay.on { opacity: 1; }

.gl { position: absolute; top: 0; bottom: 0; width: 1px; background: var(--h-16); }
.gl.zero { background: var(--h-30); }

/* the one annotation on this slide: the province-wide rate */
.benchmark {
  position: absolute;
  top: -0.2rem;
  bottom: -0.1rem;
  width: 0;
  border-left: 2px dashed var(--g-65);
}
.benchmark-tag {
  position: absolute;
  bottom: 100%;
  left: 0;
  transform: translateX(-50%);
  margin-bottom: 0.18rem;
  white-space: nowrap;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--oppo-gold);
  font-variant-numeric: tabular-nums;
}

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
  grid-template-columns: var(--c-name) 1fr var(--c-val) var(--c-cov) var(--c-covval);
  gap: 0 var(--c-gap);
  align-items: center;
  height: 34px;
}

.r-name {
  font-size: 1.02rem;
  line-height: 1.1;
  color: var(--oppo-ink-1);
  text-align: right;
  white-space: nowrap;
  transition: color 320ms ease;
}

.bar-area { position: relative; height: 18px; }
.bar {
  height: 18px;
  background: var(--chart-bar);
  border-radius: 0 4px 4px 0;
  transition: width 880ms cubic-bezier(.22, 1, .36, 1), opacity 420ms ease;
}

.val {
  text-align: right;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--oppo-ink);
  font-variant-numeric: tabular-nums;
  opacity: 0;
  transition: opacity 400ms ease, color 420ms ease;
}
.val.on { opacity: 1; }

/* --------------------------------------------------------- coverage track */
.cov-area { position: relative; height: 18px; }
.lolli {
  position: absolute;
  top: 8px;
  left: 0;
  height: 2px;
  background: var(--h-25);
  transition: width 760ms cubic-bezier(.22, 1, .36, 1);
}
.lolli.over { background: var(--g-35); }

.dot {
  position: absolute;
  top: 3px;
  width: 12px;
  height: 12px;
  margin-left: -6px;
  border-radius: 50%;
  background: var(--oppo-bg-2);
  border: 2px solid var(--oppo-neutral);
  opacity: 0;
  transform: scale(.4);
  transition: opacity 320ms ease, transform 420ms cubic-bezier(.22, 1.4, .4, 1);
}
.dot.on { opacity: 1; transform: scale(1); }
.dot.over { background: var(--oppo-gold-fig); border-color: var(--oppo-gold-fig); }

.cov-val {
  text-align: right;
  font-size: 1.02rem;
  font-weight: 650;
  color: var(--oppo-ink-2);
  font-variant-numeric: tabular-nums;
  opacity: 0;
  transition: opacity 400ms ease;
}
.cov-val.on { opacity: 1; }
.cov-val.over { color: var(--oppo-gold); font-weight: 750; }

/* once coverage is on stage, the volume bars step back */
.plot.shift .bar { opacity: 0.42; }
.plot.shift .val { color: var(--oppo-ink-2); font-weight: 600; }

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
.row.residual .val { color: var(--oppo-ink-2); font-weight: 600; }
.row.residual .cov-val { color: var(--oppo-ink-4); font-weight: 500; }

/* ------------------------------------------------------------------ axes */
.axis { position: relative; height: 1.25rem; }
.axis-rail { position: absolute; top: 0.3rem; }
.bar-rail {
  left: calc(var(--c-name) + var(--c-gap));
  right: calc(var(--c-val) + var(--c-cov) + var(--c-covval) + var(--c-gap) * 3);
}
.cov-rail {
  left: calc(100% - var(--c-cov) - var(--c-covval) - var(--c-gap));
  right: calc(var(--c-covval) + var(--c-gap));
  opacity: 0;
  transition: opacity 480ms ease;
}
.cov-rail.on { opacity: 1; }
.at {
  position: absolute;
  transform: translateX(-50%);
  font-size: 0.76rem;
  color: var(--oppo-ink-2);
  font-variant-numeric: tabular-nums;
}

/* ------------------------------------------------------------------ rail */
.rail { display: flex; flex-direction: column; gap: 0.8rem; }

.hero, .foot {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 520ms ease, transform 520ms cubic-bezier(.22, 1, .36, 1);
}
.hero.on, .foot.on { opacity: 1; transform: translateY(0); }

.hero { border-color: var(--g-28); background: linear-gradient(160deg, var(--grad-a), var(--grad-b)); }
.hero-top { display: flex; align-items: center; gap: 0.5rem; }
.hero-ico { width: 20px; height: 20px; fill: var(--oppo-gold-fig); flex: none; }
.hero-num {
  font-size: 3.1rem;
  font-weight: 800;
  letter-spacing: -0.035em;
  line-height: 1.02;
  color: var(--oppo-gold);
  margin-top: 0.3rem;
  font-variant-numeric: tabular-nums;
}

.meter {
  height: 7px;
  border-radius: 4px;
  background: var(--h-14);
  overflow: hidden;
  margin: 0.55rem 0 0.75rem;
}
.meter-fill {
  height: 100%;
  border-radius: 4px;
  background: var(--oppo-gold-fig);
  transition: width 1400ms cubic-bezier(.22, 1, .36, 1) 260ms;
}

.hero-grid { display: flex; flex-direction: column; gap: 0.5rem; }
.hero-grid dt {
  font-size: 0.74rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--oppo-ink-3);
}
.hero-grid dd {
  font-size: 1.22rem;
  font-weight: 750;
  color: var(--oppo-ink);
  font-variant-numeric: tabular-nums;
  line-height: 1.15;
}

.foot {
  font-size: 0.82rem;
  line-height: 1.4;
  color: var(--oppo-ink-2);
  transition-delay: 240ms;
  margin-top: auto;
}
</style>
