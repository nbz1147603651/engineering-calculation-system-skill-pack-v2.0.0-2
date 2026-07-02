/* ============================================
   ECS Homepage — Features Section Component
   ============================================ */

import { motion } from 'framer-motion'
import { Section } from '@/components/layout/Section'
import { fadeUp, stagger, featureToneClassNames } from '@/data/constants'
import type { Translation } from '@/types'

export default function Features({ t }: { t: Translation }) {
  return (
    <Section id="features" className="bg-gradient-to-b from-[#F8FBFF] to-white">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
        className="text-center mb-16"
      >
        <motion.div variants={fadeUp} className="section-divider mx-auto mb-6" />
        <motion.h2 variants={fadeUp} className="text-3xl md:text-4xl font-bold mb-4">
          {t.featuresSection.title}
        </motion.h2>
        <motion.p variants={fadeUp} className="text-text2 max-w-2xl mx-auto">
          {t.featuresSection.subtitle}
        </motion.p>
      </motion.div>

      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
        className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        {t.features.map((f, i) => (
          <motion.div
            key={f.title}
            variants={fadeUp}
            custom={i}
            whileHover={{ y: -8 }}
            className={`glass-card feature-card p-8 ${featureToneClassNames[i % featureToneClassNames.length]}`}
          >
            <div className="feature-icon w-14 h-14 rounded-lg bg-accent-pale flex items-center justify-center text-2xl mb-5">
              {f.icon}
            </div>
            <h3 className="text-lg font-bold mb-3 text-text">{f.title}</h3>
            <p className="text-sm text-text2 leading-relaxed">{f.desc}</p>
          </motion.div>
        ))}
      </motion.div>
    </Section>
  )
}
