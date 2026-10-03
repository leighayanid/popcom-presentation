# From Human Numbers to Human Lives

Flag-ceremony department report for the **Office of the Provincial Population Officer,
Province of Bataan**, built with [Slidev](https://sli.dev/).

## Running it

```bash
npm install
npm run dev       # http://localhost:3030
```

Press **→ / Space** to advance. Most figure slides are staged across several clicks —
the diagram builds as you speak. Press **P** for presenter mode: the full script for
each slide (taken from `popcom_files/10.5. BPC Complete Concept.docx`) is in the
speaker notes, with the click cues marked.

### Settings

Press **,** or use the gear in the top-right corner to open the settings page.
It holds two independent choices, and paints itself in whatever you pick, so you
are looking at the thing you are choosing.

**Colour theme**

| | |
|---|---|
| **OPPO Gold** | Deep navy stage, single amber accent. The Office's own theme, and the default. |
| **Bataeño Pass** | The Pass card's palette — Bataan navy, wordmark green, circuit cyan. For when the deck is shown alongside Pass collateral. |

**Appearance** — dark or light. Dark is what a projector wants; light is what a
printed hand-out wants. The quick toggle beside the gear does the same thing, as
does **D**.

Both choices are saved per browser, so they survive a reload and carry into the
presenter window. The deck opens **dark** the first time a browser sees it,
whatever the machine prefers; `setup/main.ts` seeds that once, and after that the
viewer's own choice wins.

The settings page also carries the Bataeño Pass brand reference the second theme
was built from — the marks, the card, the palette with its hex values, and the
usage rules — so a team reviewing the switch can check the deck against the card
rather than against a memory of it.

### Exporting

```bash
npm run export             # PDF, OPPO Gold, dark
npm run export:light       # PDF, OPPO Gold, light
npm run export:pass        # PDF, Bataeño Pass, dark
npm run export:pass:light  # PDF, Bataeño Pass, light
npm run export:png         # one PNG per slide
npm run build              # static site in dist/
```

Exports always go per-slide: a whole-deck export comes out blank for this deck.

`slidev export` opens a fresh browser, so neither saved choice is there to find.
Dark/light travels as slidev's own `--dark` flag, and the palette travels as
`VITE_DECK_THEME`. Setting an env var inside an npm script is not portable across
`cmd.exe` and `sh`, so `scripts/export.mjs` sets it and names the output file.
For any other combination:

```bash
node scripts/export.mjs [oppo|pass] [dark|light] [pdf|png]
```

The same override works on a URL — `?theme=pass` — if you want to hand someone a
link that opens in one particular theme. Neither control appears in an export.

## Structure

| File | What it holds |
|---|---|
| `slides.md` | The deck: slide order, copy and speaker notes |
| `styles/index.css` | **All four colour-token sets**, the brand constants, ambient keyframes, click transitions |
| `global-top.vue` / `global-bottom.vue` | The gear, the quick theme switch and the settings page; the progress rail and footer |
| `composables/deck-theme.ts` | Which brand palette is on, and how it is resolved |
| `composables/exporting.ts` | Detects an export/print render |
| `setup/main.ts` | Seeds dark as the first-run default |
| `scripts/export.mjs` | Export in a chosen theme; names the output file |
| `layouts/` | `cover`, `section`, `figure`, `statement` |
| `components/` | One component per animated diagram, plus the brand and settings components |
| `public/` | The marks and the card, served at the deck's root |
| `popcom_files/` | Source material — the script, the EO, the reference PDFs, the original artwork |

Every diagram takes a `:step="$clicks"` prop and stages itself from that; the slide's
`clicks:` frontmatter sets how many steps it has. Ambient motion (flowing data, pulses,
heartbeats) runs continuously once a stage is revealed.

| Component | Slide |
|---|---|
| `NumbersToLives` | Digits rippling into people — the guiding principle |
| `MandatePillars` | The Local Government Code mandate as a classical order |
| `PopdevShift` | Population management → population and development |
| `EoFlow` | EO 26, s. 2026 and the transfer of the Bataeño Pass |
| `StrategyMap` | The 2030 Bataan Strategy Map, staged bottom-up |
| `HdiComposite` | The four HDI++ dimensions feeding one index |
| `LifeExpectancyFlow` | LCR death entries → AWDS → Life Expectancy Index |
| `EducationFlow` | Student registration, tapping, and the AHD layer |
| `LivingStreams` | Four programmes building one household |
| `StatBars` | Accomplishments as of August 2026 |
| `PassHub` | The Pass as data registry and service rails |
| `AiGauges` | AI across three operational areas |
| `PartnerNetwork` | The collaboration map |
| `ClosingLines` | Behind every number is a person |
| `PassCard` | The card face itself, read in three hotspots |

And three that are not diagrams:

| Component | What it does |
|---|---|
| `SettingsPanel` | The settings page: theme, appearance, and the Pass brand reference |
| `ThemeToggle` | The quick dark/light switch beside the gear |
| `BrandLockup` | The two marks, side by side or stacked — cover, closing slide, footer |

## Theming

Every colour in the deck is a token defined in `styles/index.css`. No component names
a colour directly — tokens are referenced even inside SVG presentation attributes
(`fill="var(--oppo-gold)"`), so a diagram re-themes without being touched.

There are two independent axes, which compose into four token sets:

| | dark | light |
|---|---|---|
| **OPPO Gold** | `:root` | `html.light` |
| **Bataeño Pass** | `html[data-deck-theme='pass']:not(.light)` | `html[data-deck-theme='pass'].light` |

`composables/deck-theme.ts` writes `data-deck-theme`; Slidev writes `dark`/`light`.
The two Pass selectors are both specificity (0,2,1) and mutually exclusive, so the
cascade does not depend on source order. Anything a Pass block leaves undeclared
falls through to the OPPO value — which is how the strategy-map pastels (`--sm-*`)
stay put: they reproduce an official document and are not ours to re-brand.

Three pairs are worth knowing about:

- `--oppo-gold` is the accent's ink role (text, thin strokes) and `--oppo-gold-fig`
  the large decorative fill role. They are identical in dark; in light they split,
  because a colour bright enough to make a good fill cannot carry text at 4.5:1.
- `--oppo-on-accent` is the ink for text sitting **on** an accent fill. It flips with
  the accent — dark on the bright amber and cyan, light on their paper counterparts.
  It is not `--oppo-on-color`, which belongs to the bright figure colours.
- `--chart-bar` is the bar chart's single series, stepped darker on paper than the
  `--s1` used for diagram accents.

The categorical series `--s1`–`--s6` are validated per surface (lightness band,
chroma, colour-vision separation, contrast). Both Pass sets separate at least as
well as the OPPO sets under a deuteranope simulation. If you change them, re-run the
check before shipping.

### Brand constants

The marks' own colours — `--bp-navy`, `--bp-green`, `--bp-sky`, `--bp-aqua`,
`--bp-blue` — sit deliberately **outside** the themed sets, at the foot of
`styles/index.css`. A logo does not re-colour with the deck: the wordmark green is
the wordmark green on a projector and on paper alike. Only the chrome around a mark
follows the tokens.

### A naming trap

Scoped component styles still lose to UnoCSS's unscoped utilities, which Slidev
ships. A class called `b` picks up `border-width: 1px`, and `ring` picks up a ring
shadow. Avoid single-word class names that UnoCSS already owns.

## The marks

`public/` holds the three pieces of artwork the deck uses, prepared from the
originals in `popcom_files/`:

| File | From | Prepared how |
|---|---|---|
| `oppo-seal.png` | `popcomlogo.jpg` | Cropped to the ring and masked to a transparent disc, so it sits on any stage instead of carrying a white square |
| `bataeno-pass-logo.png` | `bataeno-pass-logo.webp` | Trimmed to its alpha bounds |
| `bataeno-pass-card.jpg` | `bataeno-pass-base.jpg` | Re-encoded |

They appear on the cover, on the EO 26 and IV.D slide titles, on the card slide, in
the footer, on the closing slide, and in the settings page's brand reference.

## A note on the numbers

Figures come from the script's "Accomplishments as of August 2026" section. The HDI++
emblems are deliberately iconic rather than gauges: no index values have been published,
so none are drawn. The AI percentages are shown as the ranges the script states.

Source material lives in `popcom_files/`.
