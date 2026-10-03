<script setup lang="ts">
/**
 * How a death entry at a Local Civil Registrar becomes an input to the
 * Life Expectancy Index - drawn as a live pipeline, because that is what it is:
 * collection runs continuously, not in batches.
 *
 * step 1 - the real-time collection
 * step 2 - the disaggregation this Office maintains
 * step 3 - the Age-Weighted Death Score
 * step 4 - the index it feeds
 * step 5 - the PPD-POA strategies working the other end of the same outcome
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const MID = 150
const HUB = { x: 290, r: 42 }
const AWDS = { x: 740 }
const LEI = 910

const LCRS = Array.from({ length: 6 }, (_, i) => ({ i, y: 86 + i * 26 }))

const FACETS = [
  'Barangay of usual residence',
  'Place of incidence',
  'Age at death',
  'Cause of death',
  'Month and day',
].map((t, i) => ({ t, i, y: 86 + i * 32 }))

const inPaths = computed(() => LCRS.map(n =>
  `M 152 ${n.y + 9} C 200 ${n.y + 9}, 210 ${MID}, ${HUB.x - HUB.r - 4} ${MID}`))

const fanPaths = computed(() => FACETS.map(f =>
  `M ${HUB.x + HUB.r + 4} ${MID} C 362 ${MID}, 372 ${f.y + 11}, 400 ${f.y + 11}`))

const joinPaths = computed(() => FACETS.map(f =>
  `M 620 ${f.y + 11} C 652 ${f.y + 11}, 666 ${MID}, 698 ${MID}`))

const shown = (at: number) => props.step >= at
const live = computed(() => props.step >= 1)
const branch = computed(() => props.step >= 5)
</script>

<template>
  <div class="lef">
    <svg viewBox="0 0 1000 380" class="stage" role="img"
      aria-label="Pipeline from Local Civil Registrar death entries to the Life Expectancy Index">
      <defs>
        <path v-for="(d, i) in inPaths" :key="'ip' + i" :id="'lef-in-' + i" :d="d" />
        <path v-for="(d, i) in fanPaths" :key="'fp' + i" :id="'lef-fan-' + i" :d="d" />
        <path v-for="(d, i) in joinPaths" :key="'jp' + i" :id="'lef-join-' + i" :d="d" />
        <path id="lef-out" :d="'M 782 ' + MID + ' H 840'" />
        <path id="lef-branch" d="M 836 332 C 894 332, 910 312, 910 212" />
        <filter id="lef-glow" x="-70%" y="-70%" width="240%" height="240%">
          <feGaussianBlur stdDeviation="4" result="b" />
          <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>

      <!-- ========== 1. Local Civil Registrars ========== -->
      <g class="stg on">
        <text x="96" y="66" text-anchor="middle" class="stg-k">SOURCE</text>
        <rect v-for="n in LCRS" :key="n.i" x="42" :y="n.y" width="110" height="18" rx="4"
          fill="var(--oppo-bg-2)" stroke="var(--h-25)" stroke-width="0.9" class="lcr"
          :style="{ animationDelay: (n.i * 0.42) + 's' }" />
        <text v-for="n in LCRS" :key="'t' + n.i" x="97" :y="n.y + 12.5" text-anchor="middle"
          class="lcr-t">LCR</text>
        <text x="96" y="266" text-anchor="middle" class="stg-n">LOCAL CIVIL</text>
        <text x="96" y="279" text-anchor="middle" class="stg-n">REGISTRARS</text>
        <text x="96" y="296" text-anchor="middle" class="stg-s">across Bataan</text>
      </g>

      <!-- flow: LCR -> databank -->
      <g class="flow" :class="{ on: shown(1) }">
        <use v-for="(d, i) in inPaths" :key="'iu' + i" :href="'#lef-in-' + i"
          fill="none" stroke="var(--s3-40)" stroke-width="1.1" />
        <template v-if="shown(1)">
          <circle v-for="(d, i) in inPaths" :key="'ic' + i" r="2.6" fill="var(--s3)" opacity="0">
            <animateMotion dur="2s" repeatCount="indefinite" :begin="(i * 0.26) + 's'">
              <mpath :href="'#lef-in-' + i" />
            </animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="2s"
              repeatCount="indefinite" :begin="(i * 0.26) + 's'" />
          </circle>
        </template>
      </g>

      <!-- ========== 2. the databank ========== -->
      <g class="stg" :class="{ on: shown(1) }" :transform="'translate(' + HUB.x + ' ' + MID + ')'">
        <circle :r="HUB.r" fill="var(--oppo-panel-2)" stroke="var(--s3)" stroke-width="1.6" />
        <circle v-if="shown(1)" :r="HUB.r" fill="none" stroke="var(--s3)" stroke-width="1" class="ping" />
        <!-- databank cylinder -->
        <g stroke="var(--s3)" stroke-width="1.5" fill="none">
          <ellipse cx="0" cy="-12" rx="17" ry="6" />
          <path d="M -17 -12 V 10 A 17 6 0 0 0 17 10 V -12" />
          <path d="M -17 -1 A 17 6 0 0 0 17 -1" opacity="0.6" />
        </g>
        <!-- sits clear below the r=42 ring: inside it, the wider setting at this
             size crosses the arc where it curves back in -->
        <text y="57" text-anchor="middle" class="hub-l">REAL-TIME</text>
      </g>
      <text :x="HUB.x" y="266" text-anchor="middle" class="stg-n">OPPO POPULATION</text>
      <text :x="HUB.x" y="279" text-anchor="middle" class="stg-n">DATABANK</text>
      <text :x="HUB.x" y="296" text-anchor="middle" class="stg-s">continuous death-entry collection</text>

      <!-- flow: databank -> facets -->
      <g class="flow" :class="{ on: shown(2) }">
        <use v-for="(d, i) in fanPaths" :key="'fu' + i" :href="'#lef-fan-' + i"
          fill="none" stroke="var(--g-30)" stroke-width="1.1" />
        <template v-if="shown(2)">
          <circle v-for="(d, i) in fanPaths" :key="'fc' + i" r="2.4" fill="var(--oppo-gold)" opacity="0">
            <animateMotion dur="1.8s" repeatCount="indefinite" :begin="(i * 0.3) + 's'">
              <mpath :href="'#lef-fan-' + i" />
            </animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="1.8s"
              repeatCount="indefinite" :begin="(i * 0.3) + 's'" />
          </circle>
        </template>
      </g>

      <!-- ========== 3. disaggregation ========== -->
      <g class="stg" :class="{ on: shown(2) }">
        <text x="510" y="66" text-anchor="middle" class="stg-k">DISAGGREGATED BY</text>
        <g v-for="f in FACETS" :key="f.i" class="facet" :style="{ transitionDelay: (f.i * 80) + 'ms' }">
          <rect x="400" :y="f.y" width="220" height="22" rx="11" fill="var(--oppo-bg-2)"
            stroke="var(--g-35)" stroke-width="0.9" />
          <text x="510" :y="f.y + 15" text-anchor="middle" class="facet-t">{{ f.t }}</text>
        </g>
        <text x="510" y="279" text-anchor="middle" class="stg-n">DOWN TO BARANGAY LEVEL</text>
        <text x="510" y="296" text-anchor="middle" class="stg-s">comparable barangay &#8594; municipality &#8594; province</text>
      </g>

      <!-- flow: facets -> AWDS -->
      <g class="flow" :class="{ on: shown(3) }">
        <use v-for="(d, i) in joinPaths" :key="'ju' + i" :href="'#lef-join-' + i"
          fill="none" stroke="var(--g-30)" stroke-width="1.1" />
        <template v-if="shown(3)">
          <circle v-for="(d, i) in joinPaths" :key="'jc' + i" r="2.4" fill="var(--oppo-gold)" opacity="0">
            <animateMotion dur="1.6s" repeatCount="indefinite" :begin="(i * 0.24) + 's'">
              <mpath :href="'#lef-join-' + i" />
            </animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="1.6s"
              repeatCount="indefinite" :begin="(i * 0.24) + 's'" />
          </circle>
        </template>
      </g>

      <!-- ========== 4. AWDS ========== -->
      <g class="stg" :class="{ on: shown(3) }" :transform="'translate(' + AWDS.x + ' ' + MID + ')'">
        <path d="M 0 -42 L 36 -21 L 36 21 L 0 42 L -36 21 L -36 -21 Z"
          fill="var(--oppo-panel-2)" stroke="var(--oppo-gold)" stroke-width="1.5" />
        <text y="-4" text-anchor="middle" class="awds-t">AWDS</text>
        <text y="11" text-anchor="middle" class="awds-s">age-weighted</text>
        <text y="21" text-anchor="middle" class="awds-s">death score</text>
      </g>
      <text :x="AWDS.x" y="266" text-anchor="middle" class="stg-n">PROXY</text>
      <text :x="AWDS.x" y="279" text-anchor="middle" class="stg-n">INDICATOR</text>

      <!-- flow: AWDS -> index -->
      <g class="flow" :class="{ on: shown(4) }">
        <use href="#lef-out" fill="none" stroke="var(--g-50)" stroke-width="1.4" />
        <template v-if="shown(4)">
          <circle r="2.8" fill="var(--oppo-gold)" opacity="0">
            <animateMotion dur="1.2s" repeatCount="indefinite"><mpath href="#lef-out" /></animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="1.2s" repeatCount="indefinite" />
          </circle>
        </template>
      </g>

      <!-- ========== 5. the index ========== -->
      <g class="stg" :class="{ on: shown(4) }" :transform="'translate(' + LEI + ' ' + MID + ')'"
        filter="url(#lef-glow)">
        <rect x="-66" y="-42" width="132" height="84" rx="10" fill="var(--oppo-panel-2)"
          stroke="var(--oppo-gold)" stroke-width="1.7" />
        <text y="-16" text-anchor="middle" class="lei-k">HDI++</text>
        <text y="4" text-anchor="middle" class="lei-t">LIFE</text>
        <text y="21" text-anchor="middle" class="lei-t">EXPECTANCY</text>
        <text y="35" text-anchor="middle" class="lei-s">INDEX</text>
      </g>

      <!-- ========== branch: the PPD-POA strategies ========== -->
      <g class="branch" :class="{ on: branch }">
        <rect x="42" y="316" width="230" height="32" rx="8" fill="var(--oppo-bg-2)"
          stroke="var(--s2-50)" stroke-width="1" />
        <text x="157" y="331" text-anchor="middle" class="br-k">PPD-POA STRATEGY 1</text>
        <text x="157" y="343" text-anchor="middle" class="br-t">Responsible Parenthood</text>

        <rect x="288" y="316" width="248" height="32" rx="8" fill="var(--oppo-bg-2)"
          stroke="var(--s2-50)" stroke-width="1" />
        <text x="412" y="331" text-anchor="middle" class="br-k">PPD-POA STRATEGY 2</text>
        <text x="412" y="343" text-anchor="middle" class="br-t">Adolescent Health and Development</text>

        <path d="M 540 332 H 566" stroke="var(--s2-60)" stroke-width="1.2" />
        <path d="M 560 328 L 566 332 L 560 336" fill="none" stroke="var(--s2-80)" stroke-width="1.2" />

        <rect x="572" y="316" width="256" height="32" rx="8" fill="var(--oppo-bg-2)"
          stroke="var(--s2-50)" stroke-width="1" />
        <text x="700" y="331" text-anchor="middle" class="br-k">DESIRED OUTCOME</text>
        <text x="700" y="343" text-anchor="middle" class="br-t">Prevent high-risk births &amp; adolescent pregnancy</text>

        <use href="#lef-branch" fill="none" stroke="var(--s2-45)"
          stroke-width="1.2" stroke-dasharray="4 5" class="br-arc" />
        <template v-if="branch">
          <circle r="2.6" fill="var(--s2)" opacity="0">
            <animateMotion dur="2.2s" repeatCount="indefinite"><mpath href="#lef-branch" /></animateMotion>
            <animate attributeName="opacity" values="0;1;1;0" dur="2.2s" repeatCount="indefinite" />
          </circle>
        </template>
        <text x="700" y="368" text-anchor="middle" class="br-s">
          may contribute to improved maternal and infant health outcomes
        </text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.lef { width: 100%; }
.stage { width: 100%; height: auto; }

.stg { opacity: 0; transition: opacity 600ms ease, transform 600ms ease; }
.stg.on { opacity: 1; }

.stg-k { font-size: 10px; font-weight: 750; letter-spacing: 0.22em; fill: var(--oppo-ink-2); }
.stg-n { font-size: 12px; font-weight: 750; letter-spacing: 0.12em; fill: var(--oppo-ink); }
.stg-s { font-size: 10.5px; fill: var(--oppo-ink-2); }

.lcr { animation: lcr-blink 3.4s ease-in-out infinite; }
@keyframes lcr-blink {
  0%, 100% { stroke: var(--h-25); }
  50%      { stroke: var(--s3-90); }
}
.lcr-t { font-size: 9.5px; font-weight: 700; letter-spacing: 0.16em; fill: var(--oppo-ink-2); }

.ping { animation: oppo-pulse-ring 2.8s ease-out infinite; }
.hub-l { font-size: 9px; font-weight: 750; letter-spacing: 0.18em; fill: var(--s3); }

.flow { opacity: 0; transition: opacity 600ms ease; }
.flow.on { opacity: 1; }

.facet { opacity: 0; transform: translateX(-14px); transform-box: view-box;
  transition: opacity 460ms ease, transform 520ms cubic-bezier(.22,1,.36,1); }
.stg.on .facet { opacity: 1; transform: translateX(0); }
.facet-t { font-size: 11.5px; font-weight: 600; fill: var(--oppo-ink-1); }

.awds-t { font-size: 15px; font-weight: 800; letter-spacing: 0.08em; fill: var(--oppo-gold); }
.awds-s { font-size: 9px; letter-spacing: 0.08em; fill: var(--oppo-ink-2); }

.lei-k { font-size: 9.5px; font-weight: 800; letter-spacing: 0.2em; fill: var(--oppo-gold); }
.lei-t { font-size: 15px; font-weight: 750; letter-spacing: 0.04em; fill: var(--oppo-ink); }
.lei-s { font-size: 10.5px; font-weight: 650; letter-spacing: 0.2em; fill: var(--oppo-ink-2); }

.branch { opacity: 0; transform: translateY(12px); transform-box: view-box;
  transition: opacity 600ms ease, transform 600ms ease; }
.branch.on { opacity: 1; transform: translateY(0); }
.br-k { font-size: 9px; font-weight: 750; letter-spacing: 0.18em; fill: var(--s2); }
.br-t { font-size: 11px; font-weight: 600; fill: var(--oppo-ink-1); }
.br-s { font-size: 10.5px; fill: var(--oppo-ink-2); font-style: italic; }
.br-arc { animation: oppo-dash 20s linear infinite; }
</style>
