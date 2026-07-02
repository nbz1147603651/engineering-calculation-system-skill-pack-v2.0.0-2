/* ============================================
   ECS Homepage — Navbar Component
   ============================================ */

import { useEffect, useRef, useState } from 'react'
import BrandLogo from '@/components/ui/BrandLogo'
import LanguageToggle from '@/components/ui/LanguageToggle'
import { useScrollPosition } from '@/hooks/useScrollPosition'
import type { Language, Translation } from '@/types'

export default function Navbar({
  language,
  t,
  onLanguageChange,
}: {
  language: Language
  t: Translation
  onLanguageChange: (language: Language) => void
}) {
  const scrolled = useScrollPosition()
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!menuOpen) return

    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    window.setTimeout(() => {
      menuRef.current?.querySelector<HTMLAnchorElement>('[data-mobile-menu-link]')?.focus()
    }, 0)

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setMenuOpen(false)
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => {
      document.body.style.overflow = previousOverflow
      window.removeEventListener('keydown', onKeyDown)
    }
  }, [menuOpen])

  const closeMenu = () => setMenuOpen(false)

  return (
    <nav aria-label={t.navAria} className={`fixed top-0 left-0 right-0 z-50 nav-glass transition-all duration-300 ${scrolled ? 'scrolled' : ''}`}>
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <a href="#top" aria-label={t.homeAria} className="flex items-center gap-3">
          <BrandLogo />
        </a>
        <div className="hidden md:flex items-center gap-8">
          {t.navItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="text-sm text-text2 hover:text-primary transition-colors relative group"
            >
              {item.label}
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary transition-all duration-300 group-hover:w-full" />
            </a>
          ))}
        </div>
        <div className="flex items-center gap-3">
          <LanguageToggle language={language} labels={t.language} onChange={onLanguageChange} />
          <a
            href="#install"
            className="hidden sm:inline-flex btn-primary !py-2 !px-4 sm:!px-5 !text-sm !rounded-lg whitespace-nowrap"
          >
            {t.install.title}
          </a>
          <button
            type="button"
            aria-label={menuOpen ? t.mobileMenu.close : t.mobileMenu.open}
            aria-controls="mobile-nav-menu"
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((open) => !open)}
            className={`mobile-menu-button md:hidden ${menuOpen ? 'mobile-menu-button-open' : ''}`}
          >
            <span />
            <span />
            <span />
          </button>
        </div>
      </div>
      <div
        id="mobile-nav-menu"
        ref={menuRef}
        hidden={!menuOpen}
        className="mobile-menu-panel md:hidden"
      >
        <div className="flex flex-col gap-2">
          {t.navItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              data-mobile-menu-link
              onClick={closeMenu}
              className="mobile-menu-link"
            >
              {item.label}
            </a>
          ))}
          <a href="#install" data-mobile-menu-link onClick={closeMenu} className="btn-primary mt-2 justify-center !py-3 !rounded-lg">
            {t.install.title}
          </a>
        </div>
      </div>
    </nav>
  )
}
