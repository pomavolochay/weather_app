<template>
  <div class="switcher" role="group" :aria-label="t('languageLabel')">
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      :class="['chip', { active: locale === option.value }]"
      @click="setLocale(option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Locale } from '~/composables/useWeatherI18n'
const { locale, setLocale, t } = useWeatherI18n()
const options = computed(() => [
  { value: 'en' as Locale, label: t('languageEnglish') },
  { value: 'ru' as Locale, label: t('languageRussian') }
])
</script>

<style scoped>
.switcher {
  display: inline-flex;
  gap: 0.5rem;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 999px;
  padding: 0.3rem;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.chip {
  border: none;
  border-radius: 999px;
  padding: 0.35rem 0.9rem;
  background: transparent;
  color: #e2e8f0;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chip.active {
  background: linear-gradient(135deg, var(--accent), var(--accent-strong));
  color: #0f172a;
  box-shadow: 0 0 12px rgba(14, 165, 233, 0.35);
}
</style>
