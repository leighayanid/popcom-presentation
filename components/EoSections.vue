<script setup lang="ts">
/**
 * Executive Order No. 26, s. 2026 - what the order actually says.
 * step 0 - the instrument itself: seal, issuing office, operative title
 * step 1 - Section 1, the structure and where it sits
 * step 2 - Section 2, who chairs it and under whose approval
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const sec1 = computed(() => props.step >= 1)
const sec2 = computed(() => props.step >= 2)
</script>

<template>
  <div class="eos">
    <!-- ── the issuing instrument ───────────────────────────────── -->
    <div class="masthead">
      <div class="seal">
        <svg viewBox="0 0 92 92" class="seal-svg" role="img" aria-label="Seal of Executive Order No. 26">
          <circle cx="46" cy="46" r="43" fill="none" stroke="var(--g-30)" stroke-width="1"
            stroke-dasharray="3 5" class="seal-ring" />
          <circle cx="46" cy="46" r="35" fill="var(--oppo-panel-2)" stroke="var(--g-60)" stroke-width="1.4" />
          <circle cx="46" cy="46" r="30" fill="none" stroke="var(--g-30)" stroke-width="0.8" />
          <!-- the eight rays of the provincial sun -->
          <g stroke="var(--g-45)" stroke-width="1.1" stroke-linecap="round">
            <line v-for="n in 8" :key="n" x1="46" y1="13" x2="46" y2="18"
              :transform="`rotate(${(n - 1) * 45} 46 46)`" />
          </g>
          <text x="46" y="38" text-anchor="middle" class="seal-k">EXECUTIVE ORDER</text>
          <text x="46" y="57" text-anchor="middle" class="seal-n">26</text>
          <text x="46" y="68" text-anchor="middle" class="seal-s">S. 2026</text>
          <circle cx="46" cy="46" r="35" fill="none"
            stroke="var(--oppo-gold)" stroke-width="1.2" class="seal-shock" />
        </svg>
      </div>

      <div class="instrument">
        <div class="issuer">
          <span>Republic of the Philippines</span>
          <i />
          <span>Province of Bataan</span>
          <i />
          <span class="issuer-strong">Office of the Provincial Governor</span>
        </div>

        <div class="order">
          <p>
            An order <strong>transferring the implementation and operationalization</strong> of
            <em>Provincial Ordinance No. 23, s. 2022</em> &#8212; the
            <em>Provincial Personal Data Card (PPDC) Ordinance</em> &#8212; under the
            <strong>Office of the Provincial Population Officer</strong>, and establishing the
            <strong>Bataeño Pass Program Management Structure</strong>.
          </p>
        </div>
      </div>
    </div>

    <!-- ── the two operative sections ───────────────────────────── -->
    <div class="sections">
      <article class="sec oppo-card" :class="{ on: sec1 }">
        <header class="sec-head">
          <div class="glyph">
            <svg viewBox="0 0 64 64" role="img" aria-label="Program management structure">
              <!-- the structure: one coordinating node carrying three below -->
              <path d="M32 26 V34 M14 42 V34 H50 V42" fill="none" stroke="var(--g-50)"
                stroke-width="1.6" stroke-linecap="round" class="limbs" />
              <rect x="18" y="8" width="28" height="18" rx="5" fill="var(--g-16)"
                stroke="var(--oppo-gold)" stroke-width="1.6" />
              <circle cx="32" cy="17" r="3.4" fill="var(--oppo-gold-fig)" class="core" />
              <g fill="var(--oppo-bg-3)" stroke="var(--g-50)" stroke-width="1.4">
                <rect x="6" y="42" width="16" height="14" rx="4" />
                <rect x="24" y="42" width="16" height="14" rx="4" />
                <rect x="42" y="42" width="16" height="14" rx="4" />
              </g>
              <g fill="var(--g-65)">
                <circle cx="14" cy="49" r="2.2" />
                <circle cx="32" cy="49" r="2.2" />
                <circle cx="50" cy="49" r="2.2" />
              </g>
            </svg>
          </div>
          <div class="sec-id">
            <span class="sec-no">Section 1</span>
            <h3>Establishment of the Program Management Structure</h3>
          </div>
        </header>

        <p class="sec-body">
          Implementation and operationalization of the <strong>Bataeño Pass Program</strong> are hereby
          transferred to and placed under the <strong>direct supervision and control</strong> of the
          Office of the Provincial Population Officer.
        </p>

        <div class="sec-take">
          <svg viewBox="0 0 18 18" class="tick" aria-hidden="true">
            <circle cx="9" cy="9" r="8" fill="none" stroke="var(--g-45)" stroke-width="1.3" />
            <path d="M5.4 9.2 L7.9 11.7 L12.8 6.2" fill="none" stroke="var(--oppo-gold)"
              stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <span>OPPO is the <strong>central coordinating office</strong> for the Program</span>
        </div>
      </article>

      <article class="sec oppo-card" :class="{ on: sec2 }">
        <header class="sec-head">
          <div class="glyph">
            <svg viewBox="0 0 64 64" role="img" aria-label="Supervision and policy direction">
              <!-- a compass: policy direction held under a higher approval -->
              <circle cx="32" cy="34" r="20" fill="var(--g-13)" stroke="var(--oppo-gold)" stroke-width="1.6" />
              <circle cx="32" cy="34" r="14" fill="none" stroke="var(--g-30)" stroke-width="0.9"
                stroke-dasharray="2 4" class="dial" />
              <path d="M32 21 L37 34 L32 47 L27 34 Z" fill="var(--g-65)" stroke="var(--oppo-gold)"
                stroke-width="1.2" stroke-linejoin="round" class="needle" />
              <circle cx="32" cy="34" r="2.6" fill="var(--oppo-bg-2)" stroke="var(--oppo-gold)" stroke-width="1.3" />
              <!-- the governor's approval sitting above it -->
              <path d="M24 10 L32 6 L40 10 L40 14 L24 14 Z" fill="var(--g-28)"
                stroke="var(--g-60)" stroke-width="1.3" stroke-linejoin="round" />
            </svg>
          </div>
          <div class="sec-id">
            <span class="sec-no">Section 2</span>
            <h3>Supervision and Policy Direction</h3>
          </div>
        </header>

        <p class="sec-body">
          The <strong>Acting Provincial Population Officer</strong> shall serve as
          <strong>Chairperson</strong> of the Bataeño Pass Program and shall exercise overall
          supervision, policy direction, and executive oversight.
        </p>

        <div class="sec-take">
          <svg viewBox="0 0 18 18" class="tick" aria-hidden="true">
            <circle cx="9" cy="9" r="8" fill="none" stroke="var(--g-45)" stroke-width="1.3" />
            <path d="M5.4 9.2 L7.9 11.7 L12.8 6.2" fill="none" stroke="var(--oppo-gold)"
              stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <span>Subject to the approval of the <strong>Provincial Governor</strong></span>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.eos { width: 100%; height: 100%; display: flex; flex-direction: column; gap: 1.25rem; }

/* ---------- masthead ---------- */
.masthead {
  display: flex;
  align-items: center;
  gap: 1.35rem;
}

.seal { flex: none; }
.seal-svg { width: 140px; height: 140px; display: block; }
.seal-ring { transform-box: fill-box; transform-origin: center; animation: oppo-spin 46s linear infinite; }
.seal-k { font-size: 6.4px; font-weight: 750; letter-spacing: 0.1em; fill: var(--oppo-ink-3); }
.seal-n { font-size: 22px; font-weight: 800; fill: var(--oppo-gold); font-variant-numeric: tabular-nums; }
.seal-s { font-size: 7px; font-weight: 700; letter-spacing: 0.18em; fill: var(--oppo-ink-2); }
.seal-shock { animation: eos-shock 3.6s ease-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes eos-shock {
  0%   { transform: scale(1); opacity: 0.55; }
  55%  { transform: scale(1.5); opacity: 0; }
  100% { transform: scale(1.5); opacity: 0; }
}

.instrument { flex: 1; min-width: 0; }

.issuer {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  font-size: 0.86rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--oppo-ink-2);
  font-weight: 600;
}
.issuer-strong { color: var(--oppo-ink-2); }
.issuer i { width: 3px; height: 3px; border-radius: 50%; background: var(--g-45); flex: none; }

.order {
  margin-top: 0.6rem;
  padding: 0.95rem 0 0.95rem 1.15rem;
  border-left: 3px solid var(--oppo-gold);
  background: linear-gradient(to right, var(--g-07), transparent 72%);
  border-radius: 0 10px 10px 0;
}
.order p {
  margin: 0;
  font-family: Fraunces, serif;
  font-size: 1.26rem;
  line-height: 1.55;
  color: var(--oppo-ink-1);
}
.order strong { color: var(--oppo-ink); font-weight: 600; }
.order em { color: var(--oppo-gold); font-style: normal; font-weight: 600; }

/* ---------- the sections ---------- */
.sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.1rem;
  flex: 1;
  min-height: 0;
}

.sec {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  padding: 1.25rem 1.35rem;
  border-radius: 16px;
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 540ms ease, transform 540ms cubic-bezier(.22,1,.36,1);
}
.sec.on { opacity: 1; transform: translateY(0); }

.sec-head { display: flex; align-items: center; gap: 0.95rem; }

.glyph { flex: none; width: 78px; height: 78px; }
.glyph svg { width: 100%; height: 100%; display: block; }
.sec.on .limbs { animation: oppo-breathe 4.2s ease-in-out infinite; }
.sec.on .core { animation: oppo-pulse-ring 2.8s ease-out infinite; transform-box: fill-box; transform-origin: center; }
.sec.on .dial { transform-box: fill-box; transform-origin: center; animation: oppo-spin 30s linear infinite; }
.sec.on .needle { transform-box: fill-box; transform-origin: center; animation: eos-sweep 6s ease-in-out infinite; }
@keyframes eos-sweep {
  0%, 100% { transform: rotate(-7deg); }
  50%      { transform: rotate(7deg); }
}

.sec-id { min-width: 0; }
.sec-no {
  display: inline-block;
  font-size: 0.82rem;
  font-weight: 750;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--oppo-gold);
  margin-bottom: 0.2rem;
}
.sec-id h3 {
  margin: 0;
  font-size: 1.3rem;
  line-height: 1.25;
  font-weight: 650;
  color: var(--oppo-ink);
}

.sec-body {
  margin: 0;
  font-size: 1.05rem;
  line-height: 1.6;
  color: var(--oppo-ink-2);
}
.sec-body strong { color: var(--oppo-ink); font-weight: 650; }

.sec-take {
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--h-11);
  font-size: 0.96rem;
  color: var(--oppo-ink-2);
}
.sec-take strong { color: var(--oppo-gold); font-weight: 650; }
.tick { width: 20px; height: 20px; flex: none; }
</style>
