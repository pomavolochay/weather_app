export const messages = {
  en: {
    eyebrow: 'Weather intelligence',
    title: 'Stay ahead of the clouds',
    subtitle: 'Powered by WeatherAPI, delivered via FastAPI and Nuxt 3.',
    formLabel: 'City',
    formPlaceholder: 'Search for any city...',
    formSubmit: 'Check weather',
    formSubmitting: 'Searching...',
    loadingBanner: 'Fetching the most recent data for {city}...',
    errorBanner: 'Unable to reach the weather service. Please retry shortly.',
    emptyCity: 'Please provide a city name.',
    placeholder: 'Search for a city to view its current conditions.',
    languageLabel: 'Language',
    languageEnglish: 'English',
    languageRussian: 'Russian'
  },
  ru: {
    eyebrow: 'Погодная аналитика',
    title: 'Будьте на шаг впереди облаков',
    subtitle: 'WeatherAPI + FastAPI + Nuxt 3 — всё в одном интерфейсе.',
    formLabel: 'Город',
    formPlaceholder: 'Введите название города...',
    formSubmit: 'Показать погоду',
    formSubmitting: 'Поиск...',
    loadingBanner: 'Получаем свежие данные для {city}...',
    errorBanner: 'Не удалось связаться с сервисом погоды. Повторите попытку позже.',
    emptyCity: 'Пожалуйста, укажите город.',
    placeholder: 'Найдите город, чтобы увидеть его актуальную погоду.',
    languageLabel: 'Язык',
    languageEnglish: 'Английский',
    languageRussian: 'Русский'
  }
} as const
