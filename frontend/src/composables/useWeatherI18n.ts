import { messages } from '~/i18n/messages'

export type Locale = keyof typeof messages
export type MessageKey = keyof (typeof messages)['en']

export const useWeatherI18n = () => {
  const locale = useState<Locale>('weather-locale', () => 'en')

  const setLocale = (value: Locale) => {
    locale.value = value
  }

  const t = (key: MessageKey, vars: Record<string, string> = {}) => {
    let result: string = messages[locale.value][key]
    for (const [variable, value] of Object.entries(vars)) {
      result = result.replaceAll(`{${variable}}`, value)
    }
    return result
  }

  return {
    locale,
    setLocale,
    t
  }
}
