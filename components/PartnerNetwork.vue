<script setup lang="ts">
/**
 * The collaboration map. AI is the force multiplier; this is the part that
 * gives the work purpose, so it is drawn as a living thing - pulses run
 * inward from every partner to the Office, continuously.
 *
 * Laid out as five tiers around the centre rather than one radial burst:
 * the partner names need room to be read, not a starburst.
 *
 * step 1 - strategic leadership and governance partners
 * step 2 - registration and operational support
 * step 3 - programme integration and use-case offices
 * step 4 - the community groundwork
 * step 5 - the internal team
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const shown = (at: number) => props.step >= at

const CX = 500
const CY = 238
const CR = 56

// ---- top centre: strategic leadership & governance
const LEAD = [
  'Local Chief Executives (LCEs)', 'LGUs', 'Sangguniang Panlalawigan (SP)',
  'Provincial Administrator', 'Local Finance Committee (LFC)', 'All PGB Departments',
]

// ---- right column: programme integration & use-case offices
const PROG = [
  'Provincial Governor’s Office', 'DepEd', 'Provincial School Board', 'Legal Office',
  'PIO', 'PITO', 'PSWDO', 'PDRRMO', 'PESO', 'PG-ENRO', 'Iskolar ng Bataan',
].map((label, i) => ({ label, i, x: 714, y: 34 + i * 38, w: 258, h: 26 }))

// ---- left column, upper: registration & operational support
const REG = [
  '1BOSSCO', 'LGUs', 'Barangays', 'Congressional District Staff',
].map((label, i) => ({ label, i, x: 28, y: 74 + i * 38, w: 240, h: 26 }))

// ---- left column, lower: community groundwork
const COMM = [
  'Barangay Population Workers (BPVs)', 'PMOC Counselors', 'Local Community Partners',
].map((label, i) => ({ label, i, x: 28, y: 276 + i * 38, w: 240, h: 26 }))

// ---- bottom centre: the internal team
const TEAM = ['Programmers', 'Administrative Officers', 'Data Analysts', 'Field Workers']

const link = (fromX: number, fromY: number, toX: number) =>
  `M ${fromX} ${fromY} C ${fromX + (toX - fromX) * 0.45} ${fromY}, ${toX - (toX - fromX) * 0.3} ${CY}, ${toX} ${CY}`

const regLinks = computed(() => REG.map(c => link(c.x + c.w, c.y + c.h / 2, CX - CR)))
const commLinks = computed(() => COMM.map(c => link(c.x + c.w, c.y + c.h / 2, CX - CR)))
const progLinks = computed(() => PROG.map(c => link(c.x, c.y + c.h / 2, CX + CR)))
</script>

<template>
  <div class="pn">
    <svg viewBox="0 0 1000 466" class="stage" role="img"
      aria-label="Five tiers of partners connecting to the Office of the Provincial Population Officer">
      <defs>
        <filter id="pn-glow" x="-80%" y="-80%" width="260%" height="260%">
          <feGaussianBlur stdDeviation="5" result="b" />
          <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
        <path v-for="(d, i) in regLinks" :key="'rp' + i" :id="'pn-reg-' + i" :d="d" />
        <path v-for="(d, i) in commLinks" :key="'cp' + i" :id="'pn-comm-' + i" :d="d" />
        <path v-for="(d, i) in progLinks" :key="'pp' + i" :id="'pn-prog-' + i" :d="d" />
        <path id="pn-lead" :d="'M ' + CX + ' 146 V ' + (CY - CR)" />
        <path id="pn-team" :d="'M ' + CX + ' 322 V ' + (CY + CR)" />
      </defs>

      <!-- ===== links ===== -->
      <g class="lk" :class="{ on: shown(2) }">
        <use v-for="(d, i) in regLinks" :key="'ru' + i" :href="'#pn-reg-' + i"
          fill="none" stroke="var(--s3)" stroke-opacity="0.3" stroke-width="1.1" />
      </g>
      <g class="lk" :class="{ on: shown(4) }">
        <use v-for="(d, i) in commLinks" :key="'cu' + i" :href="'#pn-comm-' + i"
          fill="none" stroke="var(--s5)" stroke-opacity="0.3" stroke-width="1.1" />
      </g>
      <g class="lk" :class="{ on: shown(3) }">
        <use v-for="(d, i) in progLinks" :key="'pu' + i" :href="'#pn-prog-' + i"
          fill="none" stroke="var(--s2)" stroke-opacity="0.3" stroke-width="1.1" />
      </g>
      <g class="lk" :class="{ on: shown(1) }">
        <use href="#pn-lead" fill="none" stroke="var(--s4)" stroke-opacity="0.4" stroke-width="1.3" />
      </g>
      <g class="lk" :class="{ on: shown(5) }">
        <use href="#pn-team" fill="none" stroke="var(--s1)" stroke-opacity="0.4" stroke-width="1.3" />
      </g>

      <!-- ===== pulses, always running inward ===== -->
      <template v-if="shown(2)">
        <circle v-for="(d, i) in regLinks" :key="'rc' + i" r="2.6" fill="var(--s3)" opacity="0">
          <animateMotion dur="2.8s" repeatCount="indefinite" :begin="(i * 0.4) + 's'">
            <mpath :href="'#pn-reg-' + i" />
          </animateMotion>
          <animate attributeName="opacity" values="0;1;1;0" dur="2.8s"
            repeatCount="indefinite" :begin="(i * 0.4) + 's'" />
        </circle>
      </template>
      <template v-if="shown(4)">
        <circle v-for="(d, i) in commLinks" :key="'cc' + i" r="2.6" fill="var(--s5)" opacity="0">
          <animateMotion dur="2.8s" repeatCount="indefinite" :begin="(0.2 + i * 0.45) + 's'">
            <mpath :href="'#pn-comm-' + i" />
          </animateMotion>
          <animate attributeName="opacity" values="0;1;1;0" dur="2.8s"
            repeatCount="indefinite" :begin="(0.2 + i * 0.45) + 's'" />
        </circle>
      </template>
      <template v-if="shown(3)">
        <circle v-for="(d, i) in progLinks" :key="'pc' + i" r="2.6" fill="var(--s2)" opacity="0">
          <animateMotion dur="3s" repeatCount="indefinite" :begin="(i * 0.27) + 's'">
            <mpath :href="'#pn-prog-' + i" />
          </animateMotion>
          <animate attributeName="opacity" values="0;1;1;0" dur="3s"
            repeatCount="indefinite" :begin="(i * 0.27) + 's'" />
        </circle>
      </template>
      <template v-if="shown(1)">
        <circle v-for="k in 2" :key="'lc' + k" r="2.8" fill="var(--s4)" opacity="0">
          <animateMotion dur="2.4s" repeatCount="indefinite" :begin="((k - 1) * 1.2) + 's'">
            <mpath href="#pn-lead" />
          </animateMotion>
          <animate attributeName="opacity" values="0;1;1;0" dur="2.4s"
            repeatCount="indefinite" :begin="((k - 1) * 1.2) + 's'" />
        </circle>
      </template>
      <template v-if="shown(5)">
        <circle v-for="k in 2" :key="'tc' + k" r="2.8" fill="var(--s1)" opacity="0">
          <animateMotion dur="2.4s" repeatCount="indefinite" :begin="((k - 1) * 1.2) + 's'">
            <mpath href="#pn-team" />
          </animateMotion>
          <animate attributeName="opacity" values="0;1;1;0" dur="2.4s"
            repeatCount="indefinite" :begin="((k - 1) * 1.2) + 's'" />
        </circle>
      </template>

      <!-- ===== tier: programme integration ===== -->
      <g class="tier" :class="{ on: shown(3) }">
        <!-- by far the longest tier label; `.long` tightens it just enough to
             sit inside its own chip column (714 to 972) at the larger size -->
        <text x="714" y="20" class="tier-k long" style="fill: var(--s2)">
          PROGRAMME INTEGRATION &amp; USE-CASE OFFICES
        </text>
        <g v-for="c in PROG" :key="'p' + c.i" class="chip" :style="{ transitionDelay: (c.i * 55) + 'ms' }">
          <rect :x="c.x" :y="c.y" :width="c.w" :height="c.h" rx="7" fill="var(--oppo-bg-2)"
            stroke="var(--s2)" stroke-opacity="0.45" stroke-width="1" />
          <circle :cx="c.x + 15" :cy="c.y + c.h / 2" r="3" fill="var(--s2)" />
          <text :x="c.x + 28" :y="c.y + c.h / 2 + 3.8" class="chip-t">{{ c.label }}</text>
        </g>
      </g>

      <!-- ===== tier: registration & operational support ===== -->
      <g class="tier" :class="{ on: shown(2) }">
        <text x="28" y="60" class="tier-k" style="fill: var(--s3)">
          REGISTRATION &amp; OPERATIONAL SUPPORT
        </text>
        <g v-for="c in REG" :key="'r' + c.i" class="chip" :style="{ transitionDelay: (c.i * 70) + 'ms' }">
          <rect :x="c.x" :y="c.y" :width="c.w" :height="c.h" rx="7" fill="var(--oppo-bg-2)"
            stroke="var(--s3)" stroke-opacity="0.45" stroke-width="1" />
          <circle :cx="c.x + 15" :cy="c.y + c.h / 2" r="3" fill="var(--s3)" />
          <text :x="c.x + 28" :y="c.y + c.h / 2 + 3.8" class="chip-t">{{ c.label }}</text>
        </g>
      </g>

      <!-- ===== tier: community groundwork ===== -->
      <g class="tier" :class="{ on: shown(4) }">
        <text x="28" y="262" class="tier-k" style="fill: var(--s5)">COMMUNITY GROUNDWORK</text>
        <g v-for="c in COMM" :key="'c' + c.i" class="chip" :style="{ transitionDelay: (c.i * 70) + 'ms' }">
          <rect :x="c.x" :y="c.y" :width="c.w" :height="c.h" rx="7" fill="var(--oppo-bg-2)"
            stroke="var(--s5)" stroke-opacity="0.45" stroke-width="1" />
          <circle :cx="c.x + 15" :cy="c.y + c.h / 2" r="3" fill="var(--s5)" />
          <text :x="c.x + 28" :y="c.y + c.h / 2 + 3.8" class="chip-t">{{ c.label }}</text>
        </g>
        <text x="28" y="404" class="tier-s">Compassionate, face-to-face engagement</text>
      </g>

      <!-- ===== tier: strategic leadership & governance ===== -->
      <g class="tier" :class="{ on: shown(1) }">
        <rect x="318" y="10" width="364" height="136" rx="10" fill="var(--oppo-bg-2)"
          stroke="var(--s4)" stroke-opacity="0.45" stroke-width="1" />
        <text x="500" y="30" text-anchor="middle" class="tier-k" style="fill: var(--s4)">
          STRATEGIC LEADERSHIP &amp; GOVERNANCE PARTNERS
        </text>
        <g v-for="(t, i) in LEAD" :key="t" class="chip" :style="{ transitionDelay: (i * 60) + 'ms' }">
          <circle cx="348" :cy="46 + i * 17" r="2.6" fill="var(--s4)" />
          <text x="360" :y="50 + i * 17" class="chip-t">{{ t }}</text>
        </g>
      </g>

      <!-- ===== tier: internal teamwork ===== -->
      <g class="tier" :class="{ on: shown(5) }">
        <rect x="358" y="322" width="284" height="112" rx="10" fill="var(--oppo-bg-2)"
          stroke="var(--s1)" stroke-opacity="0.45" stroke-width="1" />
        <text x="500" y="342" text-anchor="middle" class="tier-k" style="fill: var(--s1)">
          INTERNAL TEAMWORK
        </text>
        <g v-for="(t, i) in TEAM" :key="t" class="chip" :style="{ transitionDelay: (i * 70) + 'ms' }">
          <circle cx="386" :cy="360 + i * 17" r="2.6" fill="var(--s1)" />
          <text x="398" :y="364 + i * 17" class="chip-t">{{ t }}</text>
        </g>
        <text x="500" y="452" text-anchor="middle" class="tier-s">one unified workforce</text>
      </g>

      <!-- ===== the Office ===== -->
      <g :transform="'translate(' + CX + ' ' + CY + ')'" filter="url(#pn-glow)">
        <circle :r="CR" fill="var(--oppo-panel-2)" stroke="var(--oppo-gold)" stroke-width="1.8" />
        <circle :r="CR" fill="none" stroke="var(--oppo-gold)" stroke-width="1.2" class="core-ping" />
        <g class="core-heart">
          <path d="M 0 13 C -17 2, -15.5 -11, -7 -11 C -2.8 -11, 0 -7.4, 0 -4.6 C 0 -7.4, 2.8 -11, 7 -11 C 15.5 -11, 17 2, 0 13 Z"
            fill="var(--oppo-gold-fig)" />
        </g>
        <text y="36" text-anchor="middle" class="core-t">OPPO</text>
      </g>
      <text x="28" y="432" class="core-s">Human collaboration gives purpose and life</text>
      <text x="28" y="446" class="core-s">to every POPDEV initiative</text>
    </svg>
  </div>
</template>

<style scoped>
.pn { width: 100%; }
.stage { width: 100%; height: auto; }

.tier, .lk { opacity: 0; transition: opacity 560ms ease; }
.tier.on, .lk.on { opacity: 1; }

.chip { opacity: 0; transform: translateY(8px); transform-box: view-box;
  transition: opacity 460ms ease, transform 520ms cubic-bezier(.22,1,.36,1); }
.tier.on .chip { opacity: 1; transform: translateY(0); }

.tier-k { font-size: 10.5px; font-weight: 750; letter-spacing: 0.16em; }
.tier-k.long { font-size: 9.8px; letter-spacing: 0.07em; }
.tier-s { font-size: 10.5px; font-style: italic; fill: var(--oppo-ink-2); }
.chip-t { font-size: 12px; font-weight: 600; fill: var(--oppo-ink-1); }

.core-ping { animation: core-ping 3s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes core-ping {
  0%   { transform: scale(1); opacity: 0.7; }
  100% { transform: scale(1.6); opacity: 0; }
}
.core-heart { animation: oppo-heartbeat 2.6s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
.core-t { font-size: 13.5px; font-weight: 800; letter-spacing: 0.18em; fill: var(--oppo-gold); }
.core-s { font-size: 11px; font-style: italic; fill: var(--oppo-ink-2); }
</style>
