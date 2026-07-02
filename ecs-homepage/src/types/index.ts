/* ============================================
   ECS Homepage — Type Definitions
   ============================================ */

import type { translations } from '@/data/translations'
import type { platforms } from '@/data/platforms'

export type Language = keyof typeof translations
export type Translation = (typeof translations)[Language]
export type PlatformId = (typeof platforms)[number]['id']
export type CopyState = 'idle' | 'copied' | 'selected' | 'error'
