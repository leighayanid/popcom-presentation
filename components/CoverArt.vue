<script setup lang="ts">
/**
 * The cover's flat artwork, drawn as vectors over the photographic plate.
 *
 * The ribbons and the crowd pyramid are the two things that could not survive
 * being enlarged from a 672px source — hard edges go stair-stepped, and the
 * pyramid's five-pixel people go to mush. Both are lifted out of the plate by
 * scripts/make-cover-plate.py and drawn again here instead, so they stay sharp
 * at any projector size.
 *
 *   components/cover-art.json    scripts/trace-cover-art.py   ribbons, traced
 *   components/cover-crowd.json  scripts/make-crowd.py        pyramid, rebuilt
 *
 * Both files are in the same 0..1 frame space, and the SVG is stretched over
 * the slide, so nothing here needs to know the canvas size.
 */
import art from './cover-art.json'
import crowd from './cover-crowd.json'

/**
 * The traced outlines sit a pixel or so inside the ribbons they replace, since
 * the outermost pixels of those are antialiased into the background and never
 * classified. Stroking each shape in its own fill grows it back by half a
 * stroke and covers the soft edge left underneath.
 */
const BLEED = 0.0009
</script>

<template>
  <svg class="cover-art" viewBox="0 0 1 1" preserveAspectRatio="none" aria-hidden="true">
    <path
      v-for="(g, i) in crowd.groups" :key="`c${i}`"
      :d="g.d" :fill="g.f" :opacity="g.o"
    />
    <path
      v-for="(s, i) in art.shapes" :key="`r${i}`"
      :d="s.d" :fill="s.fill" :stroke="s.fill" :stroke-width="BLEED"
      stroke-linejoin="round"
    />
  </svg>
</template>

<style scoped>
.cover-art {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  pointer-events: none;
}
</style>
