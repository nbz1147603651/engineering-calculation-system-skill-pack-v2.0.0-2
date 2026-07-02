/* ============================================
   ECS Homepage — Language Toggle Component
   ============================================ */

import type { Language, Translation } from '@/types'

export default function LanguageToggle({
  language,
  labels,
  onChange,
}: {
  language: Language
  labels: Translation['language']
  onChange: (language: Language) => void
}) {
  const options: { value: Language; shortLabel: string; ariaLabel: string }[] = [
    { value: 'zh', shortLabel: labels.zh, ariaLabel: labels.zhLabel },
    { value: 'en', shortLabel: labels.en, ariaLabel: labels.enLabel },
  ]

  return (
    <div
      role="group"
      aria-label={labels.aria}
      className="inline-flex h-9 shrink-0 items-center rounded-lg border border-border bg-white/75 p-0.5 shadow-sm"
    >
      {options.map((option) => {
        const active = language === option.value
        return (
          <button
            key={option.value}
            type="button"
            aria-label={option.ariaLabel}
            aria-pressed={active}
            onClick={() => onChange(option.value)}
            className={`h-8 w-10 rounded-md text-xs font-semibold transition-colors ${
              active
                ? 'bg-primary text-white shadow-sm'
                : 'text-text3 hover:bg-accent-pale hover:text-primary'
            }`}
          >
            {option.shortLabel}
          </button>
        )
      })}
    </div>
  )
}
