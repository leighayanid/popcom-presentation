<script setup lang="ts">
/**
 * The Bataeno Pass as infrastructure, drawn as one thing: a plinth carrying
 * two others.
 *
 *   above it    SERVICE - the identified use cases it is tapped for
 *   the plinth  the Pass itself: one card, one citizen registry
 *   below it    DATA - the registry it standardises, and what that may support
 *
 * Each use case carries its own pictogram, drawn in one stroke weight on one
 * 24-unit grid so the eight read as a set rather than eight borrowed marks. The
 * pictograms name the programme, nothing more - they do not assert outcomes
 * this Office does not own. The contactless glyph that every tile used to carry
 * stays on, demoted to a faint corner mark: the differing thing (the programme)
 * leads, the identical thing (the tap, verified against one registry) repeats.
 *
 * The HDI++ capstone is dashed, not solid. No human-development analysis runs
 * on this registry yet, and the figure should not imply that it does.
 *
 * step 1 - the use cases it carries, and the taps running up to them
 * step 2 - the registry it builds, and where that may lead
 * step 3 - who remains responsible for delivery
 */
import { computed } from 'vue'
import Ticker from './Ticker.vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const REGISTRANTS = 241984

/* One stroke weight, one 24-unit grid, paths only - so scoped CSS reaches
   them and the set stays recolourable with the figure's accent. */
const USES = [
  {
    t: 'School Implementation',
    // a schoolhouse: pennant, roof, body, door
    d: [
      'M12 6.6V3.1',
      'M12 3.1h2.7l-.7.95.7.95H12z',
      'M3 11.8 12 6.6l9 5.2',
      'M5.2 12.7V20h13.6v-7.3',
      'M10 20v-4.6h4V20',
    ],
  },
  {
    t: 'Libreng Sakay',
    // a bus: body, window band, wheels
    d: [
      'M4.3 15.7V7.2a2 2 0 0 1 2-2h11.4a2 2 0 0 1 2 2v8.5',
      'M4.3 15.7h15.4',
      'M4.3 10.6h15.4',
      'M12 5.2v5.4',
      'M6.3 15.7a1.5 1.5 0 0 0 3 0',
      'M14.7 15.7a1.5 1.5 0 0 0 3 0',
    ],
  },
  {
    t: 'Social Services',
    // a heart held in a cupped hand
    d: [
      'M12 12.8 7.9 8.7a2.9 2.9 0 0 1 4.1-4.1 2.9 2.9 0 0 1 4.1 4.1z',
      'M4.4 15.5c2.3 3.2 4.8 4.8 7.6 4.8s5.3-1.6 7.6-4.8',
    ],
  },
  {
    t: 'READI',
    // a shield carrying a readiness pulse
    d: [
      'M12 3.7 19 6.1v5.5c0 4-2.9 6.9-7 8.4-4.1-1.5-7-4.4-7-8.4V6.1z',
      'M8.3 11.8h2l1.2-2.4 1.5 4.1 1-1.7h1.7',
    ],
  },
  {
    t: 'Bataan Jobs',
    // a briefcase: case, handle, latch line
    d: [
      'M5.2 8.7h13.6a1.6 1.6 0 0 1 1.6 1.6v6.5a1.6 1.6 0 0 1-1.6 1.6H5.2a1.6 1.6 0 0 1-1.6-1.6v-6.5a1.6 1.6 0 0 1 1.6-1.6z',
      'M9.3 8.7V7a1.6 1.6 0 0 1 1.6-1.6h2.2a1.6 1.6 0 0 1 1.6 1.6v1.7',
      'M3.6 12.8h16.8',
    ],
  },
  {
    t: 'Iskolar ng Bataan',
    // a mortarboard with its tassel
    d: [
      'M2.8 9.3 12 5.3l9.2 4-9.2 4z',
      'M6.5 11v4.2c0 1.5 2.5 2.7 5.5 2.7s5.5-1.2 5.5-2.7V11',
      'M20.3 10v4.4',
    ],
  },
  {
    t: 'BHSS',
    // a verified seal - neutral until the programme's own mark is settled
    d: [
      'M12 4.6a7.4 7.4 0 1 1 0 14.8 7.4 7.4 0 0 1 0-14.8z',
      'M8.7 12.1l2.3 2.3 4.3-4.6',
    ],
  },
  {
    t: 'EduChild',
    // an adult and a child standing together
    d: [
      'M9.1 7.3a2 2 0 1 1 0 4 2 2 0 1 1 0-4z',
      'M12 19.6v-4.6a2.9 2.9 0 0 0-2.9-2.9 2.9 2.9 0 0 0-2.9 2.9v4.6',
      'M16.6 10.3a1.55 1.55 0 1 1 0 3.1 1.55 1.55 0 1 1 0-3.1z',
      'M18.8 19.6v-3.3a2.2 2.2 0 0 0-2.2-2.2 2.2 2.2 0 0 0-2.2 2.2v3.3',
    ],
  },
]

const STRATA = [
  { k: 'Registry', t: 'A standardised citizen registry', s: 'One record format across all twelve LGUs' },
  { k: 'System', t: 'A system that captures and organises it', s: 'Maintained as registration continues' },
  { k: 'Information', t: 'Verified, disaggregated information', s: 'Down to the barangay level' },
]

const service = computed(() => props.step >= 1)
const data = computed(() => props.step >= 2)
const owned = computed(() => props.step >= 3)
</script>

<template>
  <div class="ph">
    <!-- ===================================================== SERVICE, above -->
    <header class="band-head" :class="{ on: service }">
      <span class="oppo-kicker">Service &#183; identified use cases</span>
      <span class="oppo-fig-note">Tapped and verified against one registry</span>
    </header>

    <ul class="uses" :class="{ on: service }">
      <li v-for="(u, i) in USES" :key="u.t" class="use" :style="{ transitionDelay: (i * 55) + 'ms' }">
        <svg class="ico" viewBox="0 0 24 24" aria-hidden="true">
          <path v-for="d in u.d" :key="d" :d="d" />
        </svg>
        <span class="lbl">{{ u.t }}</span>
        <svg class="tap" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5.1 9.3a4.3 4.3 0 0 1 0 5.4" />
          <path d="M9.2 6.4a8.6 8.6 0 0 1 0 11.2" />
          <path d="M13.3 3.5a12.9 12.9 0 0 1 0 17" />
        </svg>
      </li>
    </ul>

    <!-- the taps rising from the plinth into the four columns of use cases -->
    <div class="stems up" :class="{ on: service }">
      <span v-for="n in 4" :key="n" class="cell">
        <span class="stem" />
        <span v-if="service" class="pip" :style="{ animationDelay: ((n - 1) * 0.42) + 's' }" />
      </span>
    </div>

    <!-- ==================================================== THE PASS, plinth -->
    <div class="plinth">
      <div class="bus" />
      <figure class="card">
        <img src="/bataeno-pass-card.jpg" alt="A Bataeño Pass card" />
        <span class="sheen" />
      </figure>
      <div class="plinth-copy">
        <div class="plinth-k">The Bataeño Pass</div>
        <div class="plinth-t">
          One card and one citizen registry, under this Office since July 2026
        </div>
      </div>
      <div class="plinth-num">
        <div class="pn-v"><Ticker :to="REGISTRANTS" :active="true" :dur="1800" /></div>
        <div class="pn-l">citizens registered<br>as of August 2026</div>
      </div>
    </div>

    <!-- the registry filling from the plinth -->
    <div class="stems down" :class="{ on: data }">
      <span v-for="n in 3" :key="n" class="cell">
        <span class="stem" />
        <span v-if="data" class="pip" :style="{ animationDelay: ((n - 1) * 0.5) + 's' }" />
      </span>
      <span class="cell" />
    </div>

    <!-- ======================================================== DATA, below -->
    <header class="band-head" :class="{ on: data }">
      <span class="oppo-kicker">Data &#183; what the registry builds</span>
    </header>

    <div class="strata" :class="{ on: data }">
      <article v-for="(s, i) in STRATA" :key="s.k" class="plate"
        :style="{ transitionDelay: (i * 90) + 'ms' }">
        <div class="p-k">{{ s.k }}</div>
        <div class="p-t">{{ s.t }}</div>
        <div class="p-s">{{ s.s }}</div>
      </article>

      <article class="cap" style="transition-delay:320ms">
        <svg class="chev" viewBox="0 0 12 24" aria-hidden="true">
          <path d="M2 4l7 8-7 8" />
        </svg>
        <div class="cap-k">HDI++</div>
        <div class="cap-t">May support future human-development analysis</div>
      </article>
    </div>

    <p class="own" :class="{ on: owned }">
      Delivery and implementation remain with the respective provincial offices.
      The Bataeño Pass provides the system and the citizen registry behind each use case.
    </p>
  </div>
</template>

<style scoped>
.ph {
  --data-cols: repeat(3, 1fr) 272px;
  --col-gap: 0.7rem;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.band-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.45rem;
  opacity: 0;
  transition: opacity 460ms ease;
}
.band-head.on { opacity: 1; }

/* ------------------------------------------------------------- use cases */
.uses {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.6rem var(--col-gap);
  list-style: none;
  margin: 0;
  padding: 0;
}
.use {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  min-height: 54px;
  padding: 0.55rem 1.35rem 0.55rem 0.8rem;
  border: 1px solid var(--g-20);
  border-radius: 11px;
  background: linear-gradient(170deg, var(--g-13), transparent 70%), var(--oppo-bg-2);
  opacity: 0;
  transform: translateY(12px) scale(0.97);
  transition: opacity 420ms ease, transform 520ms cubic-bezier(.22, 1, .36, 1);
}
.uses.on .use { opacity: 1; transform: none; }

/* the programme's own mark - the one thing that differs tile to tile */
.ico {
  flex: none;
  width: 23px;
  height: 23px;
  fill: none;
  stroke: var(--oppo-gold);
  stroke-width: 1.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* the shared tap, demoted to a corner mark: identical on all eight */
.tap {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 13px;
  height: 13px;
  fill: none;
  stroke: var(--oppo-gold);
  stroke-width: 2;
  stroke-linecap: round;
  opacity: 0.3;
}
.uses.on .tap { animation: tap-fade 2.8s ease-in-out infinite; }
@keyframes tap-fade {
  0%, 100% { opacity: 0.22; }
  50%      { opacity: 0.6; }
}
.lbl {
  flex: 1;
  min-width: 0;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.15;
  text-wrap: pretty;
  color: var(--oppo-ink-1);
}

/* the caveat holds its space from the start, so step 3 does not shift the figure */
.own {
  min-height: 2.3rem;
  margin: 0.8rem 0 0;
  padding-left: 0.8rem;
  border-left: 2px solid var(--g-40);
  font-size: 0.92rem;
  line-height: 1.45;
  max-width: 48rem;
  text-wrap: pretty;
  color: var(--oppo-ink-2);
  opacity: 0;
  transform: translateY(6px);
  transition: opacity 520ms ease, transform 520ms ease;
}
.own.on { opacity: 1; transform: none; }

/* ----------------------------------------------------------------- stems */
.stems {
  display: grid;
  height: 30px;
  opacity: 0;
  transition: opacity 460ms ease;
}
.stems.on { opacity: 1; }
.stems.up { grid-template-columns: repeat(4, 1fr); }
.stems.down { grid-template-columns: var(--data-cols); gap: 0 var(--col-gap); }
.cell { position: relative; }
.stem {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 1px;
  background: linear-gradient(to bottom, var(--g-16), var(--g-50));
}
.stems.down .stem { background: linear-gradient(to bottom, var(--g-50), var(--g-16)); }

.pip {
  position: absolute;
  left: 50%;
  width: 4px;
  height: 4px;
  margin-left: -2px;
  border-radius: 50%;
  background: var(--oppo-gold);
  animation: pip-up 2.1s linear infinite;
}
.stems.down .pip { animation-name: pip-down; }
@keyframes pip-up {
  0%   { top: 100%; opacity: 0; }
  20%  { opacity: 1; }
  80%  { opacity: 1; }
  100% { top: -2px; opacity: 0; }
}
@keyframes pip-down {
  0%   { top: -2px; opacity: 0; }
  20%  { opacity: 1; }
  80%  { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}

/* --------------------------------------------------------------- the Pass */
.plinth {
  position: relative;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  padding: 0.9rem 1.2rem;
  border-top: 1px solid var(--g-45);
  border-bottom: 1px solid var(--g-16);
  background:
    linear-gradient(to right, transparent, var(--g-07) 18%, var(--g-07) 82%, transparent),
    linear-gradient(160deg, var(--grad-a), var(--grad-b));
}

/* a slow pulse travelling along the top edge — registration is continuous */
.bus {
  position: absolute;
  top: -1px;
  left: 0;
  width: 26%;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--oppo-gold), transparent);
  animation: bus 7s cubic-bezier(.5, 0, .5, 1) infinite;
}
@keyframes bus {
  0%   { transform: translateX(-30%); opacity: 0; }
  12%  { opacity: 1; }
  88%  { opacity: 1; }
  100% { transform: translateX(400%); opacity: 0; }
}

.card {
  position: relative;
  flex: none;
  width: 150px;
  height: 95px;
  margin: 0;
  border-radius: 9px;
  overflow: hidden;
  border: 1px solid var(--g-40);
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.3);
  animation: oppo-bob 6s ease-in-out infinite;
}
.card img { width: 100%; height: 100%; object-fit: cover; display: block; }
.sheen {
  position: absolute;
  inset: 0 auto 0 0;
  width: 34%;
  background: linear-gradient(to right, transparent, var(--g-50), transparent);
  animation: oppo-sheen 5.2s ease-in-out infinite;
}

.plinth-copy { flex: 1; min-width: 0; }
.plinth-k {
  font-size: 0.86rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--oppo-gold);
}
.plinth-t {
  margin-top: 0.2rem;
  font-size: 1.08rem;
  line-height: 1.3;
  color: var(--oppo-ink);
  font-weight: 600;
}

.plinth-num { flex: none; text-align: right; }
.pn-v {
  font-size: 1.85rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1;
  color: var(--oppo-ink);
}
.pn-l {
  margin-top: 0.2rem;
  font-size: 0.84rem;
  line-height: 1.3;
  color: var(--oppo-ink-2);
}

/* ---------------------------------------------------------- the registry */
.strata {
  display: grid;
  grid-template-columns: var(--data-cols);
  gap: 0 var(--col-gap);
  align-items: stretch;
}
.plate, .cap {
  opacity: 0;
  transform: translateY(-10px);
  transition: opacity 440ms ease, transform 520ms cubic-bezier(.22, 1, .36, 1);
}
.strata.on .plate, .strata.on .cap { opacity: 1; transform: none; }

.plate {
  display: flex;
  flex-direction: column;
  padding: 0.65rem 0.85rem 0.7rem;
  border: 1px solid var(--h-14);
  border-top: 2px solid var(--g-50);
  border-radius: 0 0 11px 11px;
  background: var(--oppo-bg-2);
}
.p-k {
  font-size: 0.78rem;
  font-weight: 750;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--oppo-gold);
}
.p-t {
  margin-top: 0.22rem;
  text-wrap: balance;
  font-size: 1.02rem;
  font-weight: 650;
  line-height: 1.25;
  color: var(--oppo-ink);
}
.p-s {
  margin-top: auto;
  padding-top: 0.25rem;
  font-size: 0.88rem;
  line-height: 1.35;
  color: var(--oppo-ink-2);
}

.cap {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 1.5rem;
  padding: 0.65rem 0.95rem 0.7rem;
  border: 1px dashed var(--g-45);
  border-radius: 11px;
  background: var(--g-07);
}
.chev {
  position: absolute;
  left: -1.35rem;
  top: 50%;
  width: 12px;
  height: 24px;
  margin-top: -12px;
  fill: none;
  stroke: var(--g-65);
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.cap-k {
  font-size: 1.18rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: var(--oppo-gold);
}
.cap-t {
  margin-top: 0.15rem;
  text-wrap: balance;
  font-size: 0.9rem;
  line-height: 1.35;
  color: var(--oppo-ink-2);
}
</style>
