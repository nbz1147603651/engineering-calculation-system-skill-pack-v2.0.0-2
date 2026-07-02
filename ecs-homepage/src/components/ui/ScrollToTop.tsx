/* ============================================
   ECS Homepage - Scroll To Top Button
   ============================================ */

import { useEffect, useState } from 'react'

export default function ScrollToTop({ label }: { label: string }) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 420)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <button
      type="button"
      aria-label={label}
      onClick={scrollToTop}
      className={`scroll-to-top ${visible ? 'scroll-to-top-visible' : ''}`}
    >
      <svg aria-hidden="true" focusable="false" viewBox="0 0 24 24">
        <path d="M12 5l-7 7m7-7l7 7M12 5v14" />
      </svg>
    </button>
  )
}
