<script setup lang="ts">
/**
 * The conclusion. Each line swaps an abstraction for the human being behind it,
 * and the icon does the same swap at the same moment.
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const shown = (at: number) => props.step >= at

const LINES = [
  { from: 'number', to: 'a person', icon: 'person' },
  { from: 'registration', to: 'a family', icon: 'family' },
  { from: 'dataset', to: 'a community', icon: 'community' },
  { from: 'program', to: 'the hope of improving someone’s life', icon: 'hope' },
]
</script>

<template>
  <div class="cl">
    <div v-for="(l, i) in LINES" :key="i" class="line" :class="{ on: shown(i + 1) }"
      :style="{ transitionDelay: (i * 60) + 'ms' }">
      <svg class="ico" viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="24" cy="24" r="22" fill="var(--oppo-panel-2)" stroke="var(--g-35)" stroke-width="1.2" />
        <circle v-if="shown(i + 1)" cx="24" cy="24" r="22" fill="none" stroke="var(--oppo-gold)"
          stroke-width="1" class="ping" :style="{ animationDelay: (i * 0.5) + 's' }" />

        <!-- the abstraction, fading out -->
        <g class="was" :class="{ gone: shown(i + 1) }">
          <text v-if="l.icon === 'person'" x="24" y="30" text-anchor="middle" class="num">7</text>
          <g v-else-if="l.icon === 'family'" stroke="var(--oppo-ink-3)" stroke-width="1.6" fill="none">
            <rect x="14" y="13" width="20" height="24" rx="2" />
            <line x1="18" y1="20" x2="30" y2="20" /><line x1="18" y1="25" x2="30" y2="25" />
            <line x1="18" y1="30" x2="26" y2="30" />
          </g>
          <g v-else-if="l.icon === 'community'" fill="var(--oppo-ink-3)">
            <rect v-for="k in 9" :key="k" :x="14 + ((k - 1) % 3) * 8" :y="14 + Math.floor((k - 1) / 3) * 8"
              width="5" height="5" rx="1" />
          </g>
          <g v-else stroke="var(--oppo-ink-3)" stroke-width="1.6" fill="none">
            <circle cx="24" cy="24" r="7" />
            <path d="M 24 12 V 17 M 24 31 V 36 M 12 24 H 17 M 31 24 H 36" />
          </g>
        </g>

        <!-- the person, fading in -->
        <g class="now" :class="{ here: shown(i + 1) }" fill="var(--oppo-gold-fig)">
          <g v-if="l.icon === 'person'">
            <circle cx="24" cy="18" r="5" />
            <path d="M 15 35 C 15 25, 19.5 22, 24 22 C 28.5 22, 33 25, 33 35 Z" />
          </g>
          <g v-else-if="l.icon === 'family'">
            <circle cx="17" cy="19" r="4" />
            <path d="M 10 33 C 10 25, 13.5 22.5, 17 22.5 C 20.5 22.5, 24 25, 24 33 Z" />
            <circle cx="30" cy="20" r="3.5" />
            <path d="M 24 33 C 24 26, 27 24, 30 24 C 33 24, 36 26, 36 33 Z" />
            <circle cx="24" cy="27" r="2.6" />
            <path d="M 20 35 C 20 30.5, 22 29.5, 24 29.5 C 26 29.5, 28 30.5, 28 35 Z" />
          </g>
          <g v-else-if="l.icon === 'community'">
            <g v-for="(p, k) in [[14, 19], [24, 15], [34, 19], [17, 31], [31, 31]]" :key="k">
              <circle :cx="p[0]" :cy="p[1]" r="3.2" />
              <path :d="'M ' + (p[0] - 5) + ' ' + (p[1] + 10) + ' C ' + (p[0] - 5) + ' ' + (p[1] + 4) + ', ' + (p[0] - 2.6) + ' ' + (p[1] + 2.6) + ', ' + p[0] + ' ' + (p[1] + 2.6) + ' C ' + (p[0] + 2.6) + ' ' + (p[1] + 2.6) + ', ' + (p[0] + 5) + ' ' + (p[1] + 4) + ', ' + (p[0] + 5) + ' ' + (p[1] + 10) + ' Z'" />
            </g>
          </g>
          <g v-else class="beat">
            <path d="M 24 36 C 9 25, 10.5 13, 18.5 13 C 22 13, 24 16, 24 18.5 C 24 16, 26 13, 29.5 13 C 37.5 13, 39 25, 24 36 Z" />
          </g>
        </g>
      </svg>

      <p>
        Behind every <span class="was-w">{{ l.from }}</span>
        is <span class="now-w">{{ l.to }}</span>.
      </p>
    </div>
  </div>
</template>

<style scoped>
.cl { display: flex; flex-direction: column; gap: 1.9rem; }

.line {
  display: flex; align-items: center; gap: 1.4rem;
  opacity: 0; transform: translateX(-18px);
  transition: opacity 620ms cubic-bezier(.22, 1, .36, 1), transform 680ms cubic-bezier(.22, 1, .36, 1);
}
.line.on { opacity: 1; transform: translateX(0); }

.ico { width: 88px; height: 88px; flex: none; }
.ping { animation: oppo-pulse-ring 2.8s ease-out infinite; }

.was { opacity: 1; transition: opacity 620ms ease 240ms; }
.was.gone { opacity: 0; }
.now { opacity: 0; transition: opacity 620ms ease 420ms; }
.now.here { opacity: 1; }
.num { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 22px; font-weight: 600; fill: var(--oppo-ink-3); }
.beat { animation: oppo-heartbeat 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }

.line p { font-size: 2rem; font-weight: 400; color: var(--oppo-ink-2); letter-spacing: -0.01em; }
.was-w { color: var(--oppo-ink-3); }
.now-w { color: var(--oppo-gold); font-weight: 650; }
</style>
