/* ============================================
   ECS Homepage — Clipboard Utilities
   ============================================ */

export function selectElementText(element: HTMLElement) {
  const selection = window.getSelection()
  const range = document.createRange()
  range.selectNodeContents(element)
  selection?.removeAllRanges()
  selection?.addRange(range)
}

export async function copyToClipboard(
  text: string,
  fallbackElement?: HTMLElement | null
): Promise<'copied' | 'selected'> {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text)
      return 'copied'
    } catch {
      // Fall back to selection when the browser denies clipboard writes.
    }
  }

  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'fixed'
  textarea.style.top = '0'
  textarea.style.left = '0'
  textarea.style.opacity = '0'
  document.body.appendChild(textarea)
  textarea.focus()
  textarea.select()
  textarea.setSelectionRange(0, text.length)
  const copied = document.execCommand('copy')
  textarea.remove()

  if (copied) {
    return 'copied'
  }

  if (fallbackElement) {
    selectElementText(fallbackElement)
    return 'selected'
  }

  throw new Error('Clipboard copy failed')
}
