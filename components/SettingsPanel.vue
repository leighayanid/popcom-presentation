<script setup lang="ts">
/**
 * Deck settings — the page where the deck's look is chosen.
 *
 * Two independent axes:
 *   Colour theme  OPPO Gold | Bataeño Pass   (composables/deck-theme.ts)
 *   Appearance    Dark | Light               (Slidev's own useDarkMode)
 *
 * Both persist per browser, so a choice survives a reload and carries into
 * the presenter window. The panel is painted in the deck's own tokens, so
 * switching a theme re-paints the panel underneath the cursor — which is the
 * point: you are looking at the thing you are choosing.
 *
 * The Bataeño Pass section below the choices is the brand reference the
 * palette was built from, so a team reviewing the switch can check the deck
 * against the card rather than against a memory of it.
 */
import { computed, nextTick, ref, watch } from 'vue'
import { useDarkMode } from '@slidev/client'
import { THEMES, deckTheme, type DeckTheme } from '../composables/deck-theme'

const open = defineModel<boolean>('open', { default: false })

const { isDark, toggleDark } = useDarkMode()
const panel = ref<HTMLElement>()

const current = computed(() => THEMES.find(t => t.id === deckTheme.value)!)
const swatches = (t: typeof THEMES[number]) => (isDark.value ? t.swatches.dark : t.swatches.light)

function choose(id: DeckTheme) {
  deckTheme.value = id
}

function setMode(dark: boolean) {
  if (isDark.value !== dark) toggleDark()
}

/**
 * Keys are stopped at the dialog rather than left to bubble: Slidev binds its
 * own shortcuts on window, so an arrow key typed in here would otherwise
 * advance the deck behind the page. Escape and ',' still close it.
 */
function onKey(e: KeyboardEvent) {
  if (e.key === 'Escape' || e.key === ',') open.value = false
}

// Move focus in when the page opens so Escape and Tab land here, not on the
// deck behind it.
watch(open, async (v) => {
  if (!v) return
  await nextTick()
  panel.value?.focus()
})

/** The Pass palette, as the settings page documents it. */
const PASS_PALETTE = [
  { name: 'Bataan Navy', hex: '#003476', role: 'The card field. The deck\'s stage in dark mode.', on: '#ffffff' },
  { name: 'Wordmark Green', hex: '#83cb05', role: '"Bataeño". First figure colour — never body text.', on: '#04203f' },
  { name: 'Pass Sky', hex: '#32b9f0', role: '"PASS". Decorative fills and large strokes.', on: '#04203f' },
  { name: 'Circuit Aqua', hex: '#3affff', role: 'The mark\'s gradient midpoint. Highlights only.', on: '#04203f' },
  { name: 'Circuit Blue', hex: '#249efb', role: 'The mark\'s gradient, blue end.', on: '#04203f' },
]

const PASS_RULES = [
  ['Field first', 'The Pass reads on navy. Put the mark on #003476 or on white — not on the wordmark green, and not on a photograph.'],
  ['Never recolour the mark', 'The circuit roundel carries its own green→aqua→blue gradient. It is reproduced as artwork, so it does not follow the deck\'s dark/light switch.'],
  ['Green is a figure colour', 'At #83cb05 the wordmark green is 1.9:1 on paper. It fills shapes and draws thick strokes; the deep cyan #06647f carries text instead.'],
  ['Clear space', 'Keep a margin of one roundel-radius around the mark. The deck\'s lockups already reserve it.'],
  ['One accent at a time', 'The Pass theme maps cyan to the single accent role the gold held. Adding a second accent is what makes a government deck look busy.'],
]
</script>

<template>
  <Teleport to="body">
    <Transition name="settings">
      <div v-if="open" class="settings-scrim" @click.self="open = false">
        <section
          ref="panel"
          class="settings"
          tabindex="-1"
          role="dialog"
          aria-modal="true"
          aria-label="Deck settings"
          @keydown.stop="onKey"
        >
          <header class="head">
            <div>
              <div class="oppo-eyebrow head-eyebrow">Deck settings</div>
              <h2>Theme &amp; appearance</h2>
            </div>
            <button class="close" type="button" aria-label="Close settings" @click="open = false">
              <svg viewBox="0 0 24 24" width="18" height="18">
                <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
              </svg>
            </button>
          </header>

          <div class="scroll">
            <!-- ---------------------------------------------- theme -->
            <h3 class="sec">Colour theme</h3>
            <p class="sec-note">
              Applies to every slide and every diagram at once — no component names a
              colour of its own.
            </p>

            <div class="themes">
              <button
                v-for="t in THEMES" :key="t.id"
                class="theme-card"
                type="button"
                :class="{ on: deckTheme === t.id }"
                :aria-pressed="deckTheme === t.id"
                @click="choose(t.id)"
              >
                <div class="tc-head">
                  <span class="tick" :class="{ on: deckTheme === t.id }">
                    <svg v-if="deckTheme === t.id" viewBox="0 0 24 24" width="11" height="11">
                      <path d="M5 12.5l4.5 4.5L19 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <div>
                    <div class="tc-name">{{ t.name }}</div>
                    <div class="tc-owner">{{ t.owner }}</div>
                  </div>
                </div>
                <div class="tc-swatches">
                  <span v-for="c in swatches(t)" :key="c" class="sw" :style="{ background: c }" />
                </div>
                <p class="tc-blurb">{{ t.blurb }}</p>
              </button>
            </div>

            <!-- ---------------------------------------- appearance -->
            <h3 class="sec">Appearance</h3>
            <p class="sec-note">
              Dark is what a projector wants; light is what a printed hand-out wants.
              Exports take whichever is set here.
            </p>
            <div class="seg" role="group" aria-label="Appearance">
              <button type="button" :class="{ on: isDark }" :aria-pressed="isDark" @click="setMode(true)">Dark</button>
              <button type="button" :class="{ on: !isDark }" :aria-pressed="!isDark" @click="setMode(false)">Light</button>
            </div>

            <!-- ------------------------------------------- preview -->
            <h3 class="sec">Preview</h3>
            <div class="preview">
              <div class="pv-eyebrow">IV.D &#183; Bataeño Pass</div>
              <div class="pv-h1">System support for HDI++</div>
              <div class="pv-sub">Behind every registration is a family.</div>
              <div class="pv-bars">
                <span
                  v-for="(h, i) in [96, 71, 58, 44, 80, 34]" :key="i"
                  class="pv-bar"
                  :style="{ background: `var(--s${i + 1})`, height: `${h}%` }"
                />
              </div>
              <div class="pv-row">
                <span class="oppo-tag">{{ current.name }}</span>
                <span class="pv-rule" />
              </div>
            </div>

            <!-- ------------------------------ brand guidelines -->
            <h3 class="sec">
              Bataeño Pass brand guidelines
              <span v-if="deckTheme === 'pass'" class="live">in use</span>
            </h3>
            <p class="sec-note">
              What the Pass theme is derived from. The marks below are reproduced as
              artwork and do not re-colour with the deck.
            </p>

            <div class="marks">
              <div class="mark-cell">
                <div class="mark-plate pass"><img src="/bataeno-pass-logo.png" alt="Bataeño Pass mark" ></div>
                <div class="mark-cap">Pass mark &#183; on navy</div>
              </div>
              <div class="mark-cell">
                <div class="mark-plate white"><img src="/bataeno-pass-logo.png" alt="Bataeño Pass mark on white" ></div>
                <div class="mark-cap">Pass mark &#183; on white</div>
              </div>
              <div class="mark-cell">
                <div class="mark-plate white"><img src="/oppo-seal.png" alt="Office of the Provincial Population Officer seal" ></div>
                <div class="mark-cap">OPPO seal</div>
              </div>
            </div>

            <div class="card-ref">
              <img src="/bataeno-pass-card.jpg" alt="The Bataeño Pass card artwork" >
              <div class="card-cap">
                The card the palette is sampled from — provincial seal and OPPO mark at
                the left, wordmark at the right, Dambana ng Kagitingan behind.
              </div>
            </div>

            <table class="palette">
              <thead>
                <tr><th>Colour</th><th>Hex</th><th>Role in the deck</th></tr>
              </thead>
              <tbody>
                <tr v-for="c in PASS_PALETTE" :key="c.hex">
                  <td>
                    <span class="chip" :style="{ background: c.hex, color: c.on }">{{ c.name }}</span>
                  </td>
                  <td class="tnum mono">{{ c.hex.toUpperCase() }}</td>
                  <td class="role">{{ c.role }}</td>
                </tr>
              </tbody>
            </table>

            <dl class="rules">
              <div v-for="[term, def] in PASS_RULES" :key="term">
                <dt>{{ term }}</dt>
                <dd>{{ def }}</dd>
              </div>
            </dl>

            <p class="foot-note">
              Both choices are saved in this browser only — switching here does not
              change the deck for anyone else.
            </p>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.settings-scrim {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: grid;
  place-items: center;
  padding: 2.5vh 2vw;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(6px);
}

.settings {
  width: min(960px, 100%);
  max-height: 95vh;
  display: flex;
  flex-direction: column;
  background: var(--oppo-bg-1);
  color: var(--oppo-ink);
  border: 1px solid var(--h-18);
  border-radius: 18px;
  box-shadow: 0 30px 90px rgba(0, 0, 0, 0.5);
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  outline: none;
  transition: background-color 320ms ease, color 320ms ease, border-color 320ms ease;
}

/* ---------- head ---------- */
.head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 1.6rem 1rem;
  border-bottom: 1px solid var(--h-14);
}
.head-eyebrow { font-size: 0.62rem; margin-bottom: 0.45rem; }
.head-eyebrow::after { max-width: 120px; }
.head h2 { font-size: 1.3rem; font-weight: 700; letter-spacing: -0.02em; margin: 0; color: var(--oppo-ink); }
.close {
  flex: none;
  display: grid;
  place-items: center;
  width: 30px; height: 30px;
  border-radius: 8px;
  border: 1px solid var(--h-16);
  background: var(--oppo-bg-2);
  color: var(--oppo-ink-2);
  cursor: pointer;
  transition: color 200ms ease, border-color 200ms ease;
}
.close:hover { color: var(--oppo-gold); border-color: var(--g-40); }

/* ---------- body ---------- */
.scroll { overflow-y: auto; padding: 1.3rem 1.6rem 1.8rem; }
.scroll::-webkit-scrollbar { width: 9px; }
.scroll::-webkit-scrollbar-thumb { background: var(--h-18); border-radius: 9px; }

.sec {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--oppo-gold);
  margin: 1.9rem 0 0.35rem;
}
.sec:first-child { margin-top: 0; }
.live {
  font-size: 0.56rem;
  letter-spacing: 0.1em;
  padding: 0.14rem 0.46rem;
  border-radius: 999px;
  border: 1px solid var(--g-40);
  background: var(--g-13);
}
.sec-note { font-size: 0.8rem; color: var(--oppo-ink-2); line-height: 1.5; margin: 0 0 0.9rem; max-width: 60ch; }

/* ---------- theme cards ---------- */
.themes { display: grid; grid-template-columns: 1fr 1fr; gap: 0.85rem; }
.theme-card {
  text-align: left;
  padding: 0.95rem 1rem 1.05rem;
  border-radius: 14px;
  border: 1px solid var(--h-16);
  background: var(--oppo-bg-2);
  cursor: pointer;
  color: inherit;
  font: inherit;
  transition: border-color 200ms ease, box-shadow 200ms ease, transform 200ms ease;
}
.theme-card:hover { transform: translateY(-1px); border-color: var(--g-40); }
.theme-card.on { border-color: var(--oppo-gold); box-shadow: 0 0 0 1px var(--oppo-gold), 0 10px 28px var(--g-16); }
.theme-card:focus-visible { outline: 2px solid var(--oppo-gold); outline-offset: 3px; }

.tc-head { display: flex; align-items: flex-start; gap: 0.6rem; }
.tick {
  flex: none;
  display: grid;
  place-items: center;
  width: 17px; height: 17px;
  margin-top: 2px;
  border-radius: 50%;
  border: 1.5px solid var(--h-30);
  color: var(--oppo-on-accent);
  transition: background-color 200ms ease, border-color 200ms ease;
}
.tick.on { background: var(--oppo-gold); border-color: var(--oppo-gold); }
.tc-name { font-size: 1rem; font-weight: 650; letter-spacing: -0.01em; color: var(--oppo-ink); }
.tc-owner { font-size: 0.66rem; color: var(--oppo-ink-3); margin-top: 0.12rem; line-height: 1.35; }

.tc-swatches { display: flex; gap: 4px; margin: 0.8rem 0 0.7rem; }
.sw { flex: 1; height: 24px; border-radius: 5px; box-shadow: inset 0 0 0 1px var(--h-14); }

.tc-blurb { font-size: 0.74rem; line-height: 1.5; color: var(--oppo-ink-2); margin: 0; }

/* ---------- segmented ---------- */
.seg {
  display: inline-flex;
  padding: 3px;
  gap: 3px;
  border-radius: 10px;
  border: 1px solid var(--h-16);
  background: var(--oppo-bg-2);
}
.seg button {
  padding: 0.38rem 1.3rem;
  border: none;
  border-radius: 7px;
  background: none;
  color: var(--oppo-ink-2);
  font: inherit;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 200ms ease, color 200ms ease;
}
.seg button.on { background: var(--oppo-gold); color: var(--oppo-on-accent); }
.seg button:focus-visible { outline: 2px solid var(--oppo-gold); outline-offset: 2px; }

/* ---------- preview ---------- */
.preview {
  border-radius: 14px;
  border: 1px solid var(--h-14);
  padding: 1.1rem 1.25rem 1.2rem;
  background:
    radial-gradient(130% 90% at 50% -20%, var(--grad-a) 0%, transparent 60%),
    var(--oppo-bg-1);
  transition: background-color 320ms ease;
}
.pv-eyebrow {
  font-size: 0.6rem; letter-spacing: 0.22em; text-transform: uppercase;
  font-weight: 650; color: var(--oppo-gold);
}
.pv-h1 { font-size: 1.35rem; font-weight: 700; letter-spacing: -0.022em; margin-top: 0.4rem; color: var(--oppo-ink); }
.pv-sub { font-family: Fraunces, serif; font-style: italic; font-size: 0.9rem; color: var(--oppo-ink-2); margin-top: 0.25rem; }
.pv-bars { display: flex; align-items: flex-end; gap: 7px; height: 68px; margin: 0.95rem 0 0.75rem; }
.pv-bar { flex: 1; border-radius: 3px 3px 0 0; }
.pv-row { display: flex; align-items: center; gap: 0.8rem; }
.pv-rule { flex: 1; height: 1px; background: linear-gradient(to right, var(--g-45), transparent); }

/* ---------- marks ---------- */
.marks { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.7rem; }
.mark-plate {
  display: grid;
  place-items: center;
  height: 110px;
  border-radius: 12px;
  border: 1px solid var(--h-14);
}
.mark-plate.pass { background: var(--bp-navy); }
.mark-plate.white { background: #ffffff; }
.mark-plate img { height: 72px; width: auto; }
.mark-cap { font-size: 0.64rem; color: var(--oppo-ink-3); margin-top: 0.4rem; text-align: center; }

.card-ref { margin-top: 1rem; max-width: 420px; }
.card-ref img {
  width: 100%;
  display: block;
  border-radius: 12px;
  border: 1px solid var(--h-14);
}
.card-cap { font-size: 0.68rem; color: var(--oppo-ink-3); margin-top: 0.45rem; line-height: 1.5; }

/* ---------- palette table ---------- */
.palette { width: 100%; border-collapse: collapse; margin-top: 1.2rem; font-size: 0.76rem; }
.palette th {
  text-align: left;
  font-size: 0.6rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--oppo-ink-3);
  font-weight: 650;
  padding-bottom: 0.45rem;
  border-bottom: 1px solid var(--h-16);
}
.palette td { padding: 0.42rem 0.7rem 0.42rem 0; border-bottom: 1px solid var(--h-10); vertical-align: middle; }
.palette td:last-child { padding-right: 0; }
.chip {
  display: inline-block;
  padding: 0.22rem 0.62rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 650;
  white-space: nowrap;
  box-shadow: inset 0 0 0 1px var(--h-14);
}
.mono { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 0.72rem; color: var(--oppo-ink-1); }
.role { color: var(--oppo-ink-2); line-height: 1.45; }

/* ---------- rules ---------- */
.rules { margin: 1.3rem 0 0; display: grid; gap: 0.7rem; }
.rules dt { font-size: 0.78rem; font-weight: 650; color: var(--oppo-ink); }
.rules dd { margin: 0.15rem 0 0; font-size: 0.76rem; line-height: 1.55; color: var(--oppo-ink-2); max-width: 72ch; }

.foot-note { margin: 1.5rem 0 0; font-size: 0.68rem; color: var(--oppo-ink-4); }

/* ---------- transition ---------- */
.settings-enter-active, .settings-leave-active { transition: opacity 220ms ease; }
.settings-enter-active .settings, .settings-leave-active .settings {
  transition: transform 260ms cubic-bezier(.22, 1, .36, 1), opacity 220ms ease;
}
.settings-enter-from, .settings-leave-to { opacity: 0; }
.settings-enter-from .settings, .settings-leave-to .settings { transform: translateY(14px) scale(0.985); }

@media (max-width: 760px) {
  .themes, .marks { grid-template-columns: 1fr; }
}
@media print { .settings-scrim { display: none !important; } }
</style>
