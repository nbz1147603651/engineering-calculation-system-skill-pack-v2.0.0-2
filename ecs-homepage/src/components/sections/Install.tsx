/* ============================================
   ECS Homepage — Install Section Component
   ============================================ */

import { useRef } from 'react'
import { motion } from 'framer-motion'
import { Section } from '@/components/layout/Section'
import { useCopyToClipboard } from '@/hooks/useCopyToClipboard'
import { INSTALL_COMMAND } from '@/data/constants'
import type { Translation } from '@/types'

export default function Install({ t }: { t: Translation }) {
  const installCommandRef = useRef<HTMLElement>(null)
  const { copyState, handleCopy } = useCopyToClipboard(INSTALL_COMMAND)

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

        {/* CLI Install */}
        <div className="relative group mb-8">
          <div className="install-terminal bg-[#0F172A] rounded-lg p-6 text-left dark-blueprint-bg overflow-hidden">
            <div className="flex items-center gap-2 mb-4">
              <div className="window-dot bg-[#FF5F56]" />
              <div className="window-dot bg-[#FFBD2E]" />
              <div className="window-dot bg-[#27C93F]" />
              <span className="text-white/40 text-xs ml-2 font-mono">terminal</span>
            </div>
            <div className="font-mono text-sm flex items-center gap-3 min-w-0">
              <span className="text-primary-light">$</span>
              <code ref={installCommandRef} className="text-white/90 flex-1 min-w-0 overflow-x-auto whitespace-nowrap">{INSTALL_COMMAND}</code>
              <button
                type="button"
                onClick={() => handleCopy(installCommandRef.current)}
                aria-label={t.install.copyAria}
                aria-live="polite"
                className="text-white/40 hover:text-white transition-colors text-xs px-3 py-1 rounded-md border border-white/10 hover:border-white/30"
              >
                {t.install.copy[copyState]}
              </button>
            </div>
          </div>
        </div>

        {/* Alternative methods */}
        <div className="grid md:grid-cols-2 gap-4">
          {t.install.methods.map((method) => (
            <div key={method.title} className="glass-card install-method p-6 text-left">
              <h3 className="font-bold mb-2 flex items-center gap-2">
                <span className="text-lg">{method.icon}</span> {method.title}
              </h3>
              <p className="text-sm text-text2 mb-4">{method.desc}</p>
              <code className="text-xs font-mono text-primary bg-accent-pale px-2 py-1 rounded">
                {method.command}
              </code>
            </div>
          ))}
        </div>
      </motion.div>
    </Section>
  )
}
