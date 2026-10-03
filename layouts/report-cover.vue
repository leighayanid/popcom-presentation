<script setup lang="ts">
/**
 * The printed department-report cover, rebuilt as live type over its own
 * artwork.
 *
 * The slide is three layers. `public/cover-plate.jpg` carries only the
 * photography — the Capitol on the left, the family at sunset on the right,
 * and the sky behind them. CoverArt draws the tricolour ribbons and the crowd
 * pyramid as vectors on top of it. The type is set here, last.
 *
 * Splitting it that way is what keeps the cover sharp: the source artwork is
 * a 672px flat image, and enlarging its hard edges is what made an all-in-one
 * plate look soft. Only the two photographs are still bound by that source.
 *
 * Positions come from measuring the original: each line is placed by the
 * centre of its capitals, as a share of the 1280x720 canvas, so it lands
 * exactly where the printed one did. Sizes and tracking were solved against
 * the artwork's own glyph metrics, which is why they are not round numbers.
 *
 * The plate is a fixed photographic light artwork, so this one slide does not
 * follow the deck's dark/light toggle.
 */
</script>

<template>
  <div class="slidev-layout report-cover">
    <img class="rc-plate" src="/cover-plate.jpg" alt="" aria-hidden="true">
    <CoverArt />
    <div class="rc-type">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.report-cover {
  padding: 0;
  background: #fff;
  overflow: hidden;
  position: relative;
}
/* the deck's survey grid belongs on the data slides, not over a photograph */
.report-cover::before { display: none; }

.rc-plate {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}
.rc-type { position: absolute; inset: 0; z-index: 2; }
.report-cover :deep(.cover-art) { z-index: 1; }

/* ---------- the lines, placed by the centre of their capitals ---------- */
.report-cover :deep(.rc-eyebrow),
.report-cover :deep(.rc-title-1),
.report-cover :deep(.rc-title-2),
.report-cover :deep(.rc-kicker),
.report-cover :deep(.rc-date),
.report-cover :deep(.rc-venue),
.report-cover :deep(.rc-rule-1),
.report-cover :deep(.rc-rule-2) {
  position: absolute;
  left: 50.22%;
  white-space: nowrap;
  /* with line-height 1 the cap centre sits 0.0137em above the box middle */
  transform: translate(-50%, calc(-50% + 0.0137em));
  line-height: 1;
  margin: 0;
}

/* letter-spacing trails the last glyph, so a matching lead keeps the ink
   centred rather than the box */
.report-cover :deep(.rc-eyebrow),
.report-cover :deep(.rc-title-1),
.report-cover :deep(.rc-title-2),
.report-cover :deep(.rc-kicker),
.report-cover :deep(.rc-date),
.report-cover :deep(.rc-venue) {
  padding-left: var(--rc-track);
  font-family: Roboto, Inter, ui-sans-serif, system-ui, sans-serif;
  letter-spacing: var(--rc-track);
  color: #041d62;
}

.report-cover :deep(.rc-eyebrow) {
  top: 19.32%;
  font-size: 26.8px;
  font-weight: 700;
  --rc-track: 0.155em;
}

.report-cover :deep(.rc-rule-1) { top: 23.68%; transform: translate(-50%, -50%); }
.report-cover :deep(.rc-rule-2) { top: 54.10%; transform: translate(-50%, -50%); }

.report-cover :deep(.rc-title-1),
.report-cover :deep(.rc-title-2) {
  font-family: 'Roboto Condensed', Roboto, Inter, ui-sans-serif, sans-serif;
  font-weight: 800;
}
.report-cover :deep(.rc-title-1) { top: 37.30%; font-size: 61.6px; --rc-track: 0.033em; }
.report-cover :deep(.rc-title-2) { top: 46.43%; font-size: 68.3px; --rc-track: 0.0173em; }

.report-cover :deep(.rc-kicker) {
  top: 59.39%;
  font-size: 37.5px;
  font-weight: 500;
  --rc-track: 0.240em;
}

.report-cover :deep(.rc-date) {
  top: 69.58%;
  font-size: 24.1px;
  font-weight: 700;
  --rc-track: 0.050em;
}

.report-cover :deep(.rc-venue) {
  top: 73.74%;
  font-size: 23.8px;
  font-weight: 400;
  color: #4d5374;
  --rc-track: 0.029em;
}
</style>
