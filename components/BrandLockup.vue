<script setup lang="ts">
/**
 * The marks, side by side, with a hairline between them.
 *
 * Both are reproduced as artwork: the OPPO seal keeps its white disc and the
 * Pass roundel keeps its own green→aqua→blue gradient, whatever theme the
 * deck is wearing. Only the rule and the caption follow the tokens.
 *
 *   <BrandLockup />                  both marks
 *   <BrandLockup only="pass" />      one of them
 *   <BrandLockup size="sm" />        footer scale
 *   <BrandLockup vertical />         stacked, for the cover rail
 */
withDefaults(defineProps<{
  only?: 'oppo' | 'pass' | 'both'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  caption?: string
  vertical?: boolean
}>(), { only: 'both', size: 'md' })
</script>

<template>
  <div class="lockup" :class="[`is-${size}`, { vertical }]">
    <div class="row">
      <img
        v-if="only !== 'pass'"
        class="brand-mark brand-seal oppo"
        src="/oppo-seal.png"
        alt="Office of the Provincial Population Officer, Bataan, Philippines"
      >
      <span v-if="only === 'both'" class="divider" />
      <img
        v-if="only !== 'oppo'"
        class="brand-mark pass"
        src="/bataeno-pass-logo.png"
        alt="Bataeño Pass"
      >
    </div>
    <div v-if="caption" class="cap">{{ caption }}</div>
  </div>
</template>

<style scoped>
.lockup { display: inline-flex; flex-direction: column; align-items: center; gap: 0.55rem; }
.row { display: flex; align-items: center; gap: 1rem; }
.vertical { max-width: 190px; }
.vertical .row { flex-direction: column; gap: 0.95rem; }
.vertical .divider { width: auto; height: 1px; align-self: stretch; }
.vertical .cap { text-align: center; line-height: 1.6; }

.oppo, .pass { width: auto; }
.is-sm .oppo, .is-sm .pass { height: 26px; }
.is-md .oppo, .is-md .pass { height: 56px; }
.is-lg .oppo, .is-lg .pass { height: 92px; }
.is-xl .oppo, .is-xl .pass { height: 112px; }

/* the Pass roundel is open line-work, so it reads a touch small next to the
   seal's solid disc at the same pixel height */
.pass { transform: scale(1.1); }

/* on the cover the two marks are stacked and read against each other
   directly, so they are matched outright rather than optically */
.is-xl .pass { transform: none; }

.divider { width: 1px; align-self: stretch; background: var(--h-22); }

.cap {
  font-size: 0.6rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--oppo-ink-4);
  font-weight: 600;
}
</style>
