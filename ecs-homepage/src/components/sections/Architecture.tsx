/* ============================================
   ECS Homepage — Architecture Section Component
   ============================================ */

import { motion } from 'framer-motion'
import { Section } from '@/components/layout/Section'
import { fadeUp, stagger } from '@/data/constants'
import type { Translation } from '@/types'

export default function Architecture({ t }: { t: Translation }) {
  return (
    <Section id="architecture" className="architecture-section overflow-hidden">
      <div className="absolute inset-0 blueprint-bg opacity-80" />
      <div className="relative z-10">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
          className="text-center mb-16"
        >
          <motion.div variants={fadeUp} className="section-divider mx-auto mb-6" />
          <motion.h2 variants={fadeUp} className="text-3xl md:text-4xl font-bold mb-4">
            {t.architecture.title}
          </motion.h2>
          <motion.p variants={fadeUp} className="text-text2 max-w-2xl mx-auto">
            {t.architecture.subtitle}
          </motion.p>
        </motion.div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-4"
        >
          {t.phases.map((p, i) => (
            <motion.div
              key={p.num}
              variants={fadeUp}
              custom={i}
              whileHover={{ y: -6 }}
              className="phase-card relative p-6 rounded-lg border border-primary/15 bg-white/85 shadow-sm backdrop-blur-sm transition-all duration-300 hover:-translate-y-1 hover:border-primary/30 hover:shadow-xl group"
            >
              <div className="font-mono text-xs text-primary mb-2">{p.num}</div>
              <h3 className="font-bold text-lg mb-2 text-text group-hover:text-primary transition-colors">
                {p.name}
              </h3>
              <p className="text-sm text-text2">{p.desc}</p>
              {/* Connection line */}
              {i < t.phases.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-2 w-4 h-px bg-gradient-to-r from-primary/40 to-transparent" />
              )}
            </motion.div>
          ))}
        </motion.div>

        {/* Gates visualization */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5, duration: 0.6 }}
          className="mt-16 p-8 rounded-lg border border-primary/15 bg-white/80 shadow-sm backdrop-blur-sm"
        >
          <h3 className="font-bold text-lg mb-6 text-center text-text">{t.architecture.gatesTitle}</h3>
          <div className="flex flex-wrap justify-center gap-3">
            {t.architecture.gates.map((gate, i) => (
              <motion.div
                key={gate}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: 0.6 + i * 0.08 }}
                className="px-4 py-2 rounded-full border border-primary/25 bg-accent-pale text-sm font-medium text-primary"
              >
                {gate}
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </Section>
  )
}
