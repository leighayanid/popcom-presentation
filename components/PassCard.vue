<script setup lang="ts">
/**
 * The Bataeño Pass itself — the half of the programme a citizen can hold.
 *
 * The card is the artwork, reproduced; the hotspots and the reading beside it
 * are the deck's. Each step lights one hotspot and its line, so the card is
 * read in the order it is spoken about.
 *
 * step 1 — who issues it
 * step 2 — what it names
 * step 3 — where it is from
 * step 4 — and what sits behind it (the hand-off to PassHub)
 *
 * A note on class names: scoped styles still lose to UnoCSS's unscoped
 * utilities, so single-word names it already owns (`b`, `ring`, `border`) are
 * avoided here — `.b` would otherwise pick up a 1px border.
 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })
const shown = (at: number) => props.step >= at

/** Positions are fractions of the card face, so the tilt carries them along. */
const SPOTS = [
  {
    n: 1,
    x: 21.5, y: 17.5,
    title: 'Issued by the Province',
    body: 'The provincial seal and this Office’s mark sit together on the face. Under EO 26, s. 2026, the Pass is carried by OPPO.',
  },
  {
    n: 2,
    x: 76.5, y: 15.5,
    title: 'One name, province-wide',
    body: 'A single citizen identity across the use cases — school implementation, Libreng Sakay, social services, READI, Bataan Jobs, Iskolar ng Bataan, BHSS, EduChild.',
  },
  {
    n: 3,
    x: 86, y: 62,
    title: 'Dambana ng Kagitingan',
    body: 'The shrine, the sea turtle, the contour of the province. The card says where its holder is from before it says anything else.',
  },
]

const visibleSpots = computed(() => SPOTS.filter(s => shown(s.n)))
</script>

<template>
  <div class="pc">
    <!-- -------------------------------------------------- the card -->
    <figure class="card-wrap">
      <div class="card" :class="{ lit: shown(1) }">
        <img src="/bataeno-pass-card.jpg" alt="The Bataeño Pass card" >
        <span class="sheen" />
        <span
          v-for="s in SPOTS" :key="s.n"
          class="spot"
          :class="{ on: shown(s.n) }"
          :style="{ left: `${s.x}%`, top: `${s.y}%` }"
          aria-hidden="true"
        >
          <span class="ping" />
          <span class="dot">{{ s.n }}</span>
        </span>
      </div>
      <figcaption>
        Bataeño Pass &#183; card face
        <span class="sep">&#183;</span>
        registration ongoing province-wide
      </figcaption>
    </figure>

    <!-- -------------------------------------------------- the reading -->
    <div class="read">
      <ol class="notes">
        <li v-for="s in SPOTS" :key="s.n" :class="{ on: shown(s.n) }">
          <span class="num">{{ s.n }}</span>
          <div>
            <div class="note-t">{{ s.title }}</div>
            <p class="note-b">{{ s.body }}</p>
          </div>
        </li>
      </ol>

      <div class="behind" :class="{ on: shown(4) }">
        <span class="rule" />
        <p>
          The card is the visible half. The registry and the digital system behind it
          are the other &#8212; and that is what the provincial offices build their
          use cases on.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pc {
  display: grid;
  grid-template-columns: 1.14fr 1fr;
  gap: 2.4rem;
  align-items: center;
  width: 100%;
}

/* ---------- card ---------- */
.card-wrap { margin: 0; perspective: 1400px; }
.card {
  position: relative;
  border-radius: 14px;
  overflow: hidden;
  transform: rotateY(-9deg) rotateX(3deg) rotateZ(-1deg);
  transform-style: preserve-3d;
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.16),
    0 2px 0 var(--h-11),
    0 26px 60px rgba(0, 0, 0, 0.42);
  transition: transform 700ms cubic-bezier(.22, 1, .36, 1), box-shadow 500ms ease;
}
.card.lit { transform: rotateY(-4deg) rotateX(1.5deg); }
.card img { display: block; width: 100%; height: auto; }

/* a slow pass of light across the laminate */
.sheen {
  position: absolute;
  inset: 0 auto 0 0;
  width: 26%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.17), transparent);
  animation: oppo-sheen 6.5s ease-in-out infinite;
  pointer-events: none;
}

/* ---------- hotspots ---------- */
.spot {
  position: absolute;
  width: 0; height: 0;
  opacity: 0;
  transform: scale(0.6);
  transition: opacity 420ms ease, transform 520ms cubic-bezier(.22, 1, .36, 1);
}
.spot.on { opacity: 1; transform: scale(1); }
.dot {
  position: absolute;
  left: -11px; top: -11px;
  width: 22px; height: 22px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--bp-green);
  color: #06290a;
  font-size: 0.62rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.85), 0 3px 10px rgba(0, 0, 0, 0.4);
}
.ping {
  position: absolute;
  left: -11px; top: -11px;
  width: 22px; height: 22px;
  border-radius: 50%;
  border: 2px solid var(--bp-aqua);
  animation: pc-ping 2.4s ease-out infinite;
}
@keyframes pc-ping {
  0%   { transform: scale(1);   opacity: 0.85; }
  70%  { transform: scale(2.5); opacity: 0; }
  100% { transform: scale(2.5); opacity: 0; }
}

figcaption {
  margin-top: 0.7rem;
  font-size: 0.6rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--oppo-ink-4);
  font-weight: 600;
}
.sep { opacity: 0.5; margin: 0 0.3rem; }

/* ---------- reading ---------- */
.notes { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.05rem; }
.notes li {
  display: flex;
  gap: 0.75rem;
  opacity: 0;
  transform: translateY(8px);
  filter: blur(2px);
  transition:
    opacity 420ms cubic-bezier(.22, 1, .36, 1),
    transform 520ms cubic-bezier(.22, 1, .36, 1),
    filter 420ms ease;
}
.notes li.on { opacity: 1; transform: none; filter: none; }

.num {
  flex: none;
  width: 21px; height: 21px;
  margin-top: 1px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--g-16);
  border: 1px solid var(--g-45);
  color: var(--oppo-gold);
  font-size: 0.6rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}
.note-t { font-size: 0.98rem; font-weight: 650; color: var(--oppo-ink); letter-spacing: -0.012em; }
.note-b { margin: 0.22rem 0 0; font-size: 0.8rem; line-height: 1.52; color: var(--oppo-ink-2); }

.behind {
  margin-top: 1.25rem;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 460ms ease, transform 520ms cubic-bezier(.22, 1, .36, 1);
}
.behind.on { opacity: 1; transform: none; }
.rule { display: block; width: 46px; height: 2px; background: var(--oppo-gold); margin-bottom: 0.65rem; }
.behind p {
  margin: 0;
  font-family: Fraunces, serif;
  font-size: 0.96rem;
  line-height: 1.5;
  color: var(--oppo-ink-1);
}
</style>
