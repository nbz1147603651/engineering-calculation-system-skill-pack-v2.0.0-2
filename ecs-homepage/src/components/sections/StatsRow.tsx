/* ============================================
   ECS Homepage — Stats Row Component
   ============================================ */

import { motion } from 'framer-motion'
import Counter from '@/components/ui/Counter'
import { fadeUp } from '@/data/constants'
import type { Translation } from '@/types'

export default function StatsRow({ stats }: { stats: Translation['stats'] }) {
  return (
    <section className="stat-strip relative py-16 bg-bg2 border-y border-border">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              custom={i}
              variants={fadeUp}
              className="stat-item text-center"
            >
              <Counter value={s.value} suffix={s.suffix} />
              <div className="mt-2 text-sm text-text3 font-medium">{s.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
