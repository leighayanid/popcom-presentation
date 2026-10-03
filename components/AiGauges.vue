<script setup lang="ts">
/**
 * Where AI sits in the operation. The three arcs are the only numbers the
 * office has published for this, so they carry explicit ranges and the arc
 * is drawn at the midpoint of the stated range, labelled with the range itself.
 *
 * step 1 - software development and system maintenance
 * step 2 - fieldwork, data governance and administrative work
 * step 3 - public advocacy and communication
 */
import { computed } from 'vue'
import Ticker from './Ticker.vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const shown = (at: number) => props.step >= at

const GAUGES = [
  { label: 'Routine setup', lo: 75, hi: 80, mid: 77.5, text: '75–80%' },
  { label: 'Automated security testing', lo: 60, hi: 60, mid: 60, text: '60%' },
  { label: 'Bug fixes', lo: 50, hi: 50, mid: 50, text: '50%' },
]

const R = 34
const C = 2 * Math.PI * R

const FIELD = [
  'Analyse demographic trends',
  'Generate smart heatmaps',
  'Optimise field-worker visits',
  'Accelerate report generation and data cleaning',
  'Surface trends, inconsistencies and errors',
]

const ADVOCACY = [
  'Translate demographic metrics into plain language',
  'Presentations and infographics',
  'Localised scripts for community symposia',
]
</script>

<template>
  <div class="ag">
    <!-- 1. software development -->
    <section class="panel" :class="{ on: shown(1) }">
      <div class="p-head">
        <span class="oppo-tag">01</span>
        <div>
          <h3>Software development &amp; system maintenance</h3>
          <p class="p-sub">Bataeño Pass &#183; code generation, refactoring, automated testing</p>
        </div>
      </div>

      <div class="gauges">
        <div v-for="(g, i) in GAUGES" :key="g.label" class="gauge">
          <svg viewBox="0 0 88 88">
            <circle cx="44" cy="44" :r="R" fill="none" stroke="var(--h-14)" stroke-width="7" />
            <circle
              cx="44" cy="44" :r="R" fill="none" stroke="var(--chart-bar)" stroke-width="7"
              stroke-linecap="round" transform="rotate(-90 44 44)"
              :stroke-dasharray="C"
              :stroke-dashoffset="shown(1) ? C * (1 - g.mid / 100) : C"
              :style="{ transition: 'stroke-dashoffset 1100ms cubic-bezier(.22,1,.36,1) ' + (i * 160) + 'ms' }"
            />
          </svg>
          <div class="g-val">
            <span v-if="g.lo !== g.hi" class="tnum">
              <Ticker :to="g.lo" :active="shown(1)" :dur="900" />&#8211;<Ticker :to="g.hi" :active="shown(1)" :dur="1100" />%
            </span>
            <span v-else class="tnum"><Ticker :to="g.mid" :active="shown(1)" :dur="1000" />%</span>
          </div>
          <div class="g-label">{{ g.label }}</div>
          <div class="g-note">faster</div>
        </div>
      </div>
      <p class="p-foot">Supporting continuous system development and maintenance.</p>
    </section>

    <!-- 2. fieldwork, data governance, admin -->
    <section class="panel" :class="{ on: shown(2) }">
      <div class="p-head">
        <span class="oppo-tag">02</span>
        <div>
          <h3>Fieldwork, data governance &amp; administrative work</h3>
          <p class="p-sub">Where the data meets the ground</p>
        </div>
      </div>
      <div class="scanbox">
        <div class="scanline" v-if="shown(2)" />
        <ul>
          <li v-for="(f, i) in FIELD" :key="f" :class="{ on: shown(2) }"
            :style="{ transitionDelay: (i * 100) + 'ms' }">
            <span class="dot" />{{ f }}
          </li>
        </ul>
      </div>
    </section>

    <!-- 3. advocacy -->
    <section class="panel" :class="{ on: shown(3) }">
      <div class="p-head">
        <span class="oppo-tag">03</span>
        <div>
          <h3>Public advocacy &amp; communication</h3>
          <p class="p-sub">Complex metrics, made legible</p>
        </div>
      </div>
      <div class="scanbox">
        <div class="scanline" v-if="shown(3)" style="animation-delay: .4s" />
        <ul>
          <li v-for="(a, i) in ADVOCACY" :key="a" :class="{ on: shown(3) }"
            :style="{ transitionDelay: (i * 100) + 'ms' }">
            <span class="dot" />{{ a }}
          </li>
        </ul>
      </div>
      <div class="caution" :class="{ on: shown(3) }">
        Without increasing administrative bloat.
      </div>
    </section>
  </div>
</template>

<style scoped>
.ag { width: 100%; display: grid; grid-template-columns: 1.25fr 1fr 1fr; gap: 1.1rem; align-items: start; }

.panel {
  opacity: 0; transform: translateY(16px);
  transition: opacity 560ms ease, transform 620ms cubic-bezier(.22, 1, .36, 1);
  border-top: 2px solid var(--g-35);
  padding-top: 1rem;
}
.panel.on { opacity: 1; transform: translateY(0); }

.p-head { display: flex; gap: 0.6rem; align-items: flex-start; margin-bottom: 0.7rem; }
/* The three headings run to one or two lines. A two-line box on all of
   them keeps the subtitles on one baseline across the row. */
.p-head h3 { font-size: 1.3rem; font-weight: 700; color: var(--oppo-ink); line-height: 1.2; min-height: 2.4em; }
.p-sub { font-size: 0.96rem; color: var(--oppo-ink-2); margin-top: 0.12rem; }
.p-foot { font-size: 0.86rem; color: var(--oppo-ink-2); margin-top: 0.6rem; font-style: italic; }

.gauges { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.7rem; margin-top: 0.4rem; }
.gauge { text-align: center; }
.gauge svg { width: 100%; max-width: 190px; height: auto; }
.g-val { font-size: 1.5rem; font-weight: 800; color: var(--oppo-gold); margin-top: -0.1rem; }
/* one- and two-line labels sit in the same box so the FASTER notes below
   them stay on a shared baseline across the three gauges */
.g-label { font-size: 1rem; color: var(--oppo-ink-1); line-height: 1.25; margin-top: 0.15rem; min-height: 2.5em; }
.g-note { font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--oppo-ink-2); }

.scanbox { position: relative; overflow: hidden; }
.scanline {
  position: absolute; left: 0; right: 0; height: 2px;
  background: linear-gradient(to right, transparent, var(--g-50), transparent);
  animation: scanv 2.4s ease-in-out 1 forwards;
}
@keyframes scanv {
  0%   { top: 0; opacity: 0; }
  15%  { opacity: 1; }
  85%  { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
.scanbox ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.62rem; }
.scanbox li {
  display: flex; gap: 0.5rem; align-items: flex-start;
  font-size: 1.15rem; line-height: 1.35; color: var(--oppo-ink-1);
  opacity: 0; transform: translateX(-10px);
  transition: opacity 460ms ease, transform 500ms ease;
}
.scanbox li.on { opacity: 1; transform: translateX(0); }
.dot { width: 5px; height: 5px; border-radius: 50%; background: var(--oppo-gold); margin-top: 0.42rem; flex: none; }

.caution {
  margin-top: 0.9rem; font-size: 1rem; font-weight: 650; color: var(--oppo-gold);
  border-left: 2px solid var(--g-50); padding-left: 0.55rem;
  opacity: 0; transition: opacity 520ms ease 400ms;
}
.caution.on { opacity: 1; }
</style>
