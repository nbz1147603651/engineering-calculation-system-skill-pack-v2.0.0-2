/* ============================================
   ECS Homepage — Install Section Component
   ============================================ */

import { motion } from 'framer-motion'
import { Section } from '@/components/layout/Section'
import { GUI_INSTALLER_DOWNLOAD_PATH } from '@/data/constants'
import type { Translation } from '@/types'

export default function Install({ t }: { t: Translation }) {
  const highlights = 'highlights' in t.install ? t.install.highlights : []
  const steps = 'steps' in t.install ? t.install.steps : []

  return (
    <Section id="install" className="bg-gradient-to-b from-[#F8FBFF] to-white">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="max-w-3xl mx-auto text-center"
      >
        <div className="section-divider mx-auto mb-6" />
        <h2 className="text-3xl md:text-4xl font-bold mb-4">{t.install.title}</h2>
        <p className="text-text2 mb-10">
          {t.install.subtitle}
        </p>

        {/* Customer-facing download CTA */}
        <div className="relative group mb-8 text-left">
          <div className="install-terminal bg-white border border-border rounded-lg p-6 md:p-8 overflow-hidden">
            <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
              <div className="min-w-0">
                <p className="text-primary text-sm font-bold mb-2">{t.install.downloadLabel}</p>
                <h3 className="text-2xl font-bold mb-3">{t.install.downloadTitle}</h3>
                <p className="text-text2 leading-relaxed mb-5">{t.install.downloadDesc}</p>
                <div className="flex flex-wrap gap-2">
                  {highlights.map((highlight) => (
                    <span key={highlight} className="text-xs font-semibold text-text2 bg-accent-pale border border-border px-3 py-1.5 rounded-full">
                      {highlight}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex flex-col sm:flex-row md:flex-col gap-2 md:min-w-40">
                <a
                  href={GUI_INSTALLER_DOWNLOAD_PATH}
                  download
                  className="btn-primary justify-center text-sm !py-3 !rounded-lg"
                >
                  {t.install.downloadCta}
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Customer onboarding */}
        <div className="grid md:grid-cols-3 gap-4">
          {steps.map((step) => (
            <div key={step.title} className="glass-card install-method p-6 text-left">
              <h3 className="font-bold mb-2 flex items-center gap-2">
                <span className="text-lg">{step.icon}</span> {step.title}
              </h3>
              <p className="text-sm text-text2 mb-4">{step.desc}</p>
              <span className="text-xs font-semibold text-primary bg-accent-pale px-2.5 py-1 rounded-full">
                {step.meta}
              </span>
            </div>
          ))}
        </div>
      </motion.div>
    </Section>
  )
}
