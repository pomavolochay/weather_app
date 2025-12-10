export type WeatherStatus = 'idle' | 'loading' | 'success' | 'error'

export interface WeatherData {
  city: string
  temperature: number
  description: string
  icon: string
  timestamp: string
  language: string
}

export const useWeather = () => {
  const config = useRuntimeConfig()
  const { t, locale } = useWeatherI18n()
  const city = ref('San Francisco')
  const status = ref<WeatherStatus>('idle')
  const errorMessage = ref<string | null>(null)
  const weather = ref<WeatherData | null>(null)

  const fetchWeather = async (overrideCity?: string) => {
    const targetCity = (overrideCity || city.value).trim()
    if (!targetCity) {
      errorMessage.value = t('emptyCity')
      status.value = 'error'
      return
    }

    status.value = 'loading'
    errorMessage.value = null
    city.value = targetCity

    try {
      const response = await $fetch<{ data: WeatherData }>(`${config.public.apiBase}/api/weather`, {
        query: { city: targetCity, lang: locale.value }
      })
      weather.value = response.data
      status.value = 'success'
    } catch (error: any) {
      const fallback = t('errorBanner')
      errorMessage.value = error?.data?.error?.message || fallback
      status.value = 'error'
    }
  }

  watch(locale, () => {
    if (status.value === 'success' && city.value) {
      fetchWeather(city.value)
    }
  })

  return {
    city,
    status,
    errorMessage,
    weather,
    fetchWeather,
    locale
  }
}
