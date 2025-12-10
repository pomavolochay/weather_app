<template>
  <div class="card" aria-live="polite">
    <div class="meta">
      <div>
        <p class="label">Current city</p>
        <p class="city">{{ weather.city }}</p>
      </div>
      <span class="timestamp">{{ formattedTimestamp }}</span>
    </div>
    <div class="body">
      <div class="temperature">
        <span class="value">{{ weather.temperature.toFixed(1) }}</span>
        <span class="unit">&deg;C</span>
      </div>
      <div class="condition">
        <img v-if="weather.icon" :src="weather.icon" :alt="weather.description" />
        <p>{{ weather.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { WeatherData } from '~/composables/useWeather'

const props = defineProps<{ weather: WeatherData }>()

const formattedTimestamp = computed(() =>
  new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(props.weather.timestamp))
)
</script>

<style scoped>
.card {
  background: var(--card-bg);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 24px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  backdrop-filter: blur(20px);
  box-shadow: 0 10px 30px rgba(2, 6, 23, 0.4);
}

.meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.label {
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  color: #94a3b8;
  margin: 0 0 0.2rem;
}

.city {
  font-size: 1.4rem;
  font-weight: 600;
}

.timestamp {
  color: #94a3b8;
  font-size: 0.85rem;
}

.body {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.temperature .value {
  font-size: 4rem;
  font-weight: 600;
  line-height: 1;
}

.temperature .unit {
  font-size: 1.5rem;
  color: #94a3b8;
}

.condition {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
  text-transform: capitalize;
}

.condition img {
  width: 52px;
  height: 52px;
}

@media (max-width: 640px) {
  .temperature .value {
    font-size: 3rem;
  }

  .card {
    padding: 1.25rem;
  }
}
</style>
