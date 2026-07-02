/* ============================================
   ECS Homepage — Language Hook
   ============================================ */

import { useEffect, useState } from 'react'
import { translations } from '@/data/translations'
import { LANGUAGE_STORAGE_KEY } from '@/data/constants'
import type { Language } from '@/types'

function getInitialLanguage(): Language {
  const saved = window.localStorage.getItem(LANGUAGE_STORAGE_KEY)
  return saved === 'en' ? 'en' : 'zh'
}

export function useLanguage() {
  const [language, setLanguage] = useState<Language>(getInitialLanguage)
  const t = translations[language]

  useEffect(() => {
    window.localStorage.setItem(LANGUAGE_STORAGE_KEY, language)
    document.documentElement.lang = t.htmlLang
    document.title = t.documentTitle

    const metaDescription = document.querySelector<HTMLMetaElement>('meta[name="description"]')
    metaDescription?.setAttribute('content', t.metaDescription)
  }, [language, t])

  return { language, setLanguage, t }
}
