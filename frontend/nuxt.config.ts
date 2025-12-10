import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  devtools: { enabled: false },
  srcDir: 'src/',
  typescript: {
    strict: true,
    typeCheck: true
  },
  css: ['~/assets/main.css'],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    }
  },
  app: {
    head: {
      title: 'Weather Insight',
      meta: [
        { name: 'description', content: 'Production-grade weather dashboard powered by FastAPI.' }
      ]
    }
  }
})
