import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import WeatherCard from '../src/components/WeatherCard.vue'

const sample = {
  city: 'Lisbon',
  temperature: 21.3,
  description: 'clear sky',
  icon: 'https://cdn.weather/icon.png',
  timestamp: new Date('2023-09-21T10:00:00Z').toISOString(),
  language: 'en'
}

describe('WeatherCard', () => {
  it('renders primary fields', () => {
    const wrapper = mount(WeatherCard, {
      props: { weather: sample }
    })

    expect(wrapper.text()).toContain('Lisbon')
    expect(wrapper.text()).toContain('21.3')
    expect(wrapper.find('img').attributes('src')).toBe(sample.icon)
  })
})
