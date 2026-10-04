<script setup lang="ts">
// Title rail on the left edge, figure gets the rest of the stage.
</script>

<template>
  <div class="slidev-layout oppo-figure">
    <slot />
  </div>
</template>

<style scoped>
.oppo-figure {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1.5rem 2.4rem 1.2rem;
}
.oppo-figure :deep(h1) { font-size: 2.05rem; margin: 0; }
.oppo-figure :deep(.fig) { flex: 1; min-height: 0; display: flex; align-items: center; }
.oppo-figure :deep(.fig) > * { width: 100%; }

/* A banner strip riding between the title and the figure: the marks the
   slide's content answers to. Capped well short of the stage width, since
   whatever it takes comes straight out of the figure's height. */
.oppo-figure :deep(.fig-banner) { display: flex; justify-content: center; }
.oppo-figure :deep(.fig-banner) > * { width: 100%; max-width: 560px; }

/* The same strip riding above the head rather than under it: the marks the
   slide answers to come first, then its own title. The title wants a little
   more air above it, so it reads as the slide’s own rather than a caption
   hanging off the plate. An eyebrow standing alone above the strip centres
   like the head’s own and drops its tail, which would otherwise read as a
   rule running out of a centred line. */
.oppo-figure :deep(.fig-banner + .fig-head) { margin-top: 0.4rem; }
.oppo-figure :deep(.oppo-eyebrow.is-center) { justify-content: center; }
.oppo-figure :deep(.oppo-eyebrow.is-center)::after { display: none; }

/* A figure sized off its own width grows taller than the stage once a
   banner is above it, and overflows up under the banner rather than
   shrinking. Only where a banner is actually present, give the figure a
   definite height so its SVG scales down into what is left instead. */
.oppo-figure :deep(.fig-banner ~ .fig) { align-items: stretch; }
.oppo-figure :deep(.fig-banner ~ .fig) > * { height: 100%; min-height: 0; }
.oppo-figure :deep(.fig-banner ~ .fig svg) { flex: 1 1 0; min-height: 0; height: auto; }

/* A head block that owns the top of the stage rather than sitting in the
   title rail: the framework name carried at statement scale, with the
   section marker demoted to the eyebrow above it. The eyebrow's trailing
   hairline reads as an off-centre tail once the text is centred, so it goes. */
.oppo-figure :deep(.fig-head.is-center) { text-align: center; }
.oppo-figure :deep(.fig-head.is-center) h1 {
  font-size: 2.9rem;
  line-height: 1.08;
  letter-spacing: -0.01em;
  margin-top: 0.35rem;
}
.oppo-figure :deep(.fig-head.is-center) .oppo-eyebrow { justify-content: center; }
.oppo-figure :deep(.fig-head.is-center) .oppo-eyebrow::after { display: none; }
</style>
