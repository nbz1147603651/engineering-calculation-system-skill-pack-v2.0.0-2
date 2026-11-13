/* ============================================
   ECS Homepage — Footer Component
   ============================================ */

import BrandLogo from '@/components/ui/BrandLogo'
import type { Translation } from '@/types'

export default function Footer({ t, version }: { t: Translation; version: string }) {
  const year = new Date().getFullYear()

  return (
    <footer className="footer-surface px-6 py-12">
      <div className="mx-auto grid max-w-7xl gap-10 md:grid-cols-[1.4fr_1fr_1fr]">
        <div className="space-y-4">
          <BrandLogo fullName />
          <p className="max-w-lg text-sm leading-6 text-text2">{t.footer.description}</p>
        </div>

        <div>
          <h2 className="footer-heading">{t.footer.productTitle}</h2>
          <div className="mt-4 flex flex-col gap-3 text-sm">
            {t.navItems.map((item) => (
              <a key={item.href} href={item.href} className="footer-link">
                {item.label}
              </a>
            ))}
          </div>
        </div>

        <div>
          <h2 className="footer-heading">{t.footer.companyTitle}</h2>
          <div className="mt-4 flex flex-col gap-3 text-sm text-text2">
            <a href="https://www.zjic.site/" target="_blank" rel="noreferrer" className="footer-link">
              {t.footer.website}
            </a>
            <span>{t.footer.versionLabel} v{version}</span>
            <span>© {year} {t.footer.copyrightPrefix}</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
