<template>
  <div class="page">
    <main>
      <header>
        <div>
          <p class="eyebrow">{{ t('eyebrow') }}</p>
          <h1>{{ t('title') }}</h1>
          <p class="subtitle">{{ t('subtitle') }}</p>
        </div>
        <LanguageSwitcher />
      </header>

      <WeatherForm v-model="city" :disabled="status === 'loading'" @submit="fetchWeather()" />

      <transition name="fade">
        <StateBanner v-if="status === 'loading'" class="mt" variant="info">
          {{ t('loadingBanner', { city: city }) }}
        </StateBanner>
      </transition>

      <transition name="fade">
        <StateBanner v-if="status === 'error' && errorMessage" class="mt" variant="error">
          {{ errorMessage }}
        </StateBanner>
      </transition>

      <section class="mt">
        <WeatherCard v-if="weather" :weather="weather" />
        <p v-else class="placeholder">{{ t('placeholder') }}</p>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
const { city, status, errorMessage, weather, fetchWeather } = useWeather()
const { t } = useWeatherI18n()

onMounted(() => {
  fetchWeather(city.value)
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
}

main {
  width: min(720px, 100%);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.4em;
  font-size: 0.7rem;
  color: #94a3b8;
  margin-bottom: 0.4rem;
}

h1 {
  font-size: clamp(2rem, 4vw, 2.75rem);
  margin: 0 0 0.5rem;
}

.subtitle {
  color: #94a3b8;
  margin: 0;
}

.mt {
  margin-top: 1rem;
}

.placeholder {
  margin: 0;
  padding: 2rem;
  border: 1px dashed rgba(148, 163, 184, 0.3);
  border-radius: 18px;
  text-align: center;
  color: #94a3b8;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .page {
    padding: 2rem 1rem;
  }
}
</style>
