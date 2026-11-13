/* ============================================
   ECS Homepage — Hero Section Component
   ============================================ */

import { motion, useReducedMotion, useScroll, useTransform } from 'framer-motion'
import type { Translation } from '@/types'

export default function Hero({ t }: { t: Translation }) {
  const { scrollY } = useScroll()
  const shouldReduceMotion = useReducedMotion()
  const y = useTransform(scrollY, [0, 500], [0, 80])
  const motionStyle = shouldReduceMotion ? undefined : { y }
  const terminalLines = [
    t.terminal.reference,
    t.terminal.blueprint,
    t.terminal.deployed,
    t.terminal.verifying,
  ]

  return (
    <section id="top" className="hero-section relative min-h-[800px] flex items-center overflow-hidden">
      {/* Background layers */}
      <div className="hero-gradient absolute inset-0" />
      <div className="absolute inset-0 blueprint-bg blueprint-bg-animated" />
      <div className="hero-measure-line hero-measure-line-top" />
      <div className="hero-measure-line hero-measure-line-bottom" />
      <div className="absolute inset-x-0 bottom-0 h-28 bg-gradient-to-b from-transparent to-bg2/80" />

      <motion.div style={motionStyle} className="relative z-10 max-w-7xl mx-auto px-6 py-32 grid md:grid-cols-2 gap-16 items-center w-full">
        {/* Left: Content */}
        <div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent-pale border border-primary/20 text-sm text-primary font-medium mb-8"
          >
            <span className="w-2 h-2 rounded-full bg-primary animate-blink" />
            {t.hero.eyebrow}
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6"
          >
            <span className="gradient-text">{t.hero.titlePrimary}</span>
            <br />
            <span className="text-text">{t.hero.titleSecondary}</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg text-text2 leading-relaxed mb-10 max-w-lg"
          >
            {t.hero.body}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-wrap gap-4"
          >
            <a href="#install" className="btn-primary flex items-center gap-2">
              <svg aria-hidden="true" focusable="false" className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {t.hero.primaryCta}
            </a>
            <a href="#features" className="px-8 py-3.5 rounded-lg border border-border hover:border-primary/30 text-text2 hover:text-primary transition-all duration-300 font-medium">
              {t.hero.secondaryCta}
            </a>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="flex flex-wrap gap-3 mt-10"
          >
            {t.hero.tags.map((tag) => (
              <span key={tag} className="hero-tag px-3 py-1 text-xs font-medium rounded-full bg-bg2 text-text3 border border-border">
                {tag}
              </span>
            ))}
          </motion.div>
        </div>

        {/* Right: Product Window Mockup */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="hidden md:block hero-visual"
        >
          <div className="product-window animate-float">
            <div className="window-titlebar">
              <div className="window-dot bg-[#FF5F56]" />
              <div className="window-dot bg-[#FFBD2E]" />
              <div className="window-dot bg-[#27C93F]" />
              <span className="text-white/60 text-xs ml-3 font-mono">{t.terminal.title}</span>
            </div>
            <div className="relative bg-[#0F172A] p-6 dark-blueprint-bg overflow-hidden">
              <div className="terminal-scanline" aria-hidden="true" />
              {/* Simulated terminal output */}
              <div className="space-y-3 font-mono text-sm">
                <div className="flex items-center gap-2">
                  <span className="text-primary-light">$</span>
                  <span className="text-white/80">{t.terminal.command}</span>
                </div>
                {terminalLines.map((line, i) => (
                  <motion.div
                    key={line}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.7 + i * 0.18, duration: 0.35 }}
                    className={`terminal-output-line text-xs ${i === terminalLines.length - 1 ? 'text-primary-light' : 'text-success'}`}
                  >
                    {line}
                  </motion.div>
                ))}
                <div className="flex items-center gap-2 mt-4">
                  <div className="h-1.5 flex-1 bg-white/10 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-primary to-primary-light rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: '100%' }}
                      transition={{ duration: 2, delay: 0.8 }}
                    />
                  </div>
                  <span className="text-white/40 text-xs">100%</span>
                </div>
                <div className="flex items-center gap-2 text-success text-xs mt-2">
                  <span className="w-2 h-2 rounded-full bg-success animate-pulse-glow" />
                  {t.terminal.complete}
                </div>
              </div>
            </div>
          </div>
          <div className="hero-status-grid">
            {t.stats.slice(0, 3).map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9 + i * 0.12, duration: 0.4 }}
                className="hero-status-card"
              >
                <span className="font-mono text-lg font-bold text-primary">{stat.value}{stat.suffix}</span>
                <span>{stat.label}</span>
              </motion.div>
            ))}
          </div>
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.12, duration: 0.45 }}
            className="hero-release-strip"
          >
            {t.phases.slice(0, 4).map((phase) => (
              <span key={phase.num}>
                <strong>{phase.num}</strong>
                {phase.name}
              </span>
            ))}
          </motion.div>
        </motion.div>
      </motion.div>
    </section>
  )
}
