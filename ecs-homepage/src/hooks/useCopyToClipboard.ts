/* ============================================
   ECS Homepage — Copy to Clipboard Hook
   ============================================ */

import { useState, useCallback } from 'react'
import { copyToClipboard } from '@/utils/clipboard'
import type { CopyState } from '@/types'

export function useCopyToClipboard(text: string) {
  const [copyState, setCopyState] = useState<CopyState>('idle')

  const handleCopy = useCallback(async (element?: HTMLElement | null) => {
    try {
      const result = await copyToClipboard(text, element)
      setCopyState(result)
    } catch {
      setCopyState('error')
    } finally {
      window.setTimeout(() => setCopyState('idle'), 2000)
    }
  }, [text])

  return { copyState, handleCopy }
}
