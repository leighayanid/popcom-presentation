<script setup lang="ts">
/**
 * Accomplishments as of August 2026.
 *
 * One series (people reached), so one hue - var(--s1), validated at >= 3:1 against
 * the deck surface. Every bar is direct-labelled, so identity and value are
 * never carried by colour alone and the chart doubles as its own table.
 * The two figures that are not counts of people (centres, sessions) sit outside
 * the bar scale as tiles rather than being forced onto one axis.
 */
import { computed } from 'vue'
import Ticker from './Ticker.vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const ROWS = [
  { label: 'Persons provided with Responsible Parenthood services', v: 11221 },
  { label: 'Adults and parents reached through AHD activities', v: 1813 },
  { label: 'Service providers reached through AHD activities', v: 1813 },
  { label: 'Adolescents reached through AHD activities', v: 1760 },
  { label: 'Would-be couples given Pre-Marriage Orientation and Counseling', v: 1700 },
  { label: 'New KATROPA participants', v: 119 },
]

const MAX = Math.max(...ROWS.map(r => r.v))
const TICKS = [0, 2500, 5000, 7500, 10000]

const TILES = [
  { v: 103, label: 'Teen Information Centers established', unit: 'centres' },
  { v: 5, label: 'KATROPA sessions conducted', unit: 'sessions' },
]

const bars = computed(() => props.step >= 1)
const tiles = computed(() => props.step >= 2)
</script>

<template>
  <div class="sb">
    <div class="chart" :class="{ live: bars }">
      <div class="chart-head">
        <span class="oppo-kicker">Persons reached &#183; January&#8211;August 2026</span>
      </div>

      <div class="plot">
        <!-- recessive grid + one-shot scan, aligned to the bar area only -->
        <div class="overlay">
          <div v-for="t in TICKS" :key="t" class="gl" :style="{ left: (t / MAX * 100) + '%' }">
            <span class="gt">{{ t.toLocaleString('en-US') }}</span>
          </div>
          <div v-if="bars" class="scan" />
        </div>

        <div v-for="(r, i) in ROWS" :key="i" class="row">
          <div class="r-label">{{ r.label }}</div>
          <div class="track">
            <div class="bar-area">
              <div class="bar" :style="{
                width: bars ? 'max(6px, ' + (r.v / MAX * 100) + '%)' : '0%',
                transitionDelay: (i * 110) + 'ms',
              }" />
            </div>
            <span class="r-val" :style="{ transitionDelay: (i * 110 + 260) + 'ms' }"
              :class="{ on: bars }">
              <Ticker :to="r.v" :active="bars" :dur="1200 + i * 90" />
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="tiles">
      <div v-for="(t, i) in TILES" :key="i" class="tile oppo-card" :class="{ on: tiles }"
        :style="{ transitionDelay: (i * 140) + 'ms' }">
        <div class="t-val"><Ticker :to="t.v" :active="tiles" :dur="900" /></div>
        <div class="t-unit">{{ t.unit }}</div>
        <div class="t-label">{{ t.label }}</div>
      </div>
      <div class="tile note" :class="{ on: tiles }" style="transition-delay: 280ms">
        <p>
          Reported as of <strong>August 2026</strong>. Counts are of persons served,
          except where the tile states otherwise.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sb { width: 100%; display: grid; grid-template-columns: 1fr 300px; gap: 2rem; align-items: center; }

.chart-head { margin-bottom: 0.5rem; }
.plot { position: relative; padding-top: 1.1rem; }

.overlay {
  position: absolute;
  top: 1.1rem; bottom: 0;
  left: calc(50% + 0.45rem);
  right: calc(78px + 0.6rem);
  pointer-events: none;
}
.gl { position: absolute; top: -1.1rem; bottom: 0; width: 1px; background: var(--h-11); }
.gt {
  position: absolute; top: -1.05rem; left: 0; transform: translateX(-50%);
  font-size: 0.64rem; color: var(--oppo-ink-4); font-variant-numeric: tabular-nums;
}

.scan {
  position: absolute; top: 0; bottom: 0; width: 2px;
  background: linear-gradient(to bottom, transparent, var(--g-60), transparent);
  left: 0; animation: scan 1.9s cubic-bezier(.3, .8, .4, 1) 1 forwards;
}
@keyframes scan {
  0%   { left: 0; opacity: 0; }
  12%  { opacity: 1; }
  88%  { opacity: 1; }
  100% { left: 100%; opacity: 0; }
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 0 0.9rem;
  padding: 0.42rem 0;
}
.r-label {
  font-size: 0.92rem;
  line-height: 1.25;
  color: var(--oppo-ink-1);
  text-align: right;
}
.track {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 78px;
  gap: 0.6rem;
  align-items: center;
  height: 28px;
}
.bar-area { position: relative; height: 18px; }
.bar {
  height: 18px;
  background: var(--chart-bar);
  border-radius: 0 4px 4px 0;
  transition: width 900ms cubic-bezier(.22, 1, .36, 1);
  flex: none;
}
.r-val {
  font-size: 1.02rem;
  font-weight: 700;
  color: var(--oppo-ink);
  font-variant-numeric: tabular-nums;
  text-align: right;
  opacity: 0;
  transition: opacity 420ms ease;
}
.r-val.on { opacity: 1; }

.tiles { display: flex; flex-direction: column; gap: 0.6rem; }
.tile {
  opacity: 0; transform: translateY(12px);
  transition: opacity 520ms ease, transform 520ms cubic-bezier(.22, 1, .36, 1);
}
.tile.on { opacity: 1; transform: translateY(0); }
.t-val { font-size: 2.7rem; font-weight: 800; color: var(--oppo-gold); line-height: 1; letter-spacing: -0.02em; }
.t-unit { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--oppo-ink-3); margin-top: 0.1rem; }
.t-label { font-size: 0.8rem; color: var(--oppo-ink-2); line-height: 1.3; margin-top: 0.3rem; }
.tile.note { border: none; background: none; padding: 0.2rem 0 0; }
.tile.note p { font-size: 0.72rem; color: var(--oppo-ink-3); line-height: 1.4; }
</style>
