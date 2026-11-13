/* ============================================
   ECS Homepage — Platforms Section Component
   ============================================ */

import { motion } from 'framer-motion'
import { Section } from '@/components/layout/Section'
import PlatformLogo from '@/components/ui/PlatformLogo'
import { platforms } from '@/data/platforms'
import { fadeUp, stagger } from '@/data/constants'
import type { Translation } from '@/types'

export default function Platforms({ t }: { t: Translation }) {
  return (
    <Section id="platforms" className="platforms-section">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
        className="text-center mb-16"
      >
        <motion.div variants={fadeUp} className="section-divider mx-auto mb-6" />
        <motion.h2 variants={fadeUp} className="text-3xl md:text-4xl font-bold mb-4">
          {t.platformsSection.title}
        </motion.h2>
        <motion.p variants={fadeUp} className="text-text2 max-w-2xl mx-auto">
          {t.platformsSection.subtitle}
        </motion.p>
      </motion.div>

      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
        className="platform-grid"
      >
        {platforms.map((p, i) => (
          <motion.div
            key={p.name}
            variants={fadeUp}
            custom={i}
            aria-label={p.name}
            className="glass-card platform-card min-h-[150px] p-6 text-center group cursor-pointer flex flex-col items-center justify-center gap-4"
            whileHover={{ y: -8, scale: 1.015 }}
            whileTap={{ scale: 0.98 }}
          >
            <PlatformLogo id={p.id} name={p.name} />
            <h3 className="font-bold text-sm text-text">{p.name}</h3>
          </motion.div>
        ))}
      </motion.div>
    </Section>
  )
}
