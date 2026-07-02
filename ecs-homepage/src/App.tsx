import { useEffect, useRef, useState } from 'react'
import type { ReactNode } from 'react'
import { motion, useInView, useScroll, useTransform } from 'framer-motion'
import codexLogo from './assets/platform-logos/codex-openai-blossom.svg'
import minimaxCodeLogo from './assets/platform-logos/minimax-code.png'
import opencodeLogo from './assets/platform-logos/opencode.png'
import qoderCnLogo from './assets/platform-logos/qoder-cn.svg'
import qoderLogo from './assets/platform-logos/qoder.svg'
import traeLogo from './assets/platform-logos/trae.png'
import zcodeLogo from './assets/platform-logos/zcode.png'

/* ============================================
   ECS Homepage — Engineering Calculation System
   ============================================ */

const INSTALL_COMMAND = 'pip install engineering-calculation-system'
const LANGUAGE_STORAGE_KEY = 'ecs-homepage-language'

const platforms = [
  { id: 'codex', name: 'Codex' },
  { id: 'qoder', name: 'Qoder' },
  { id: 'qoder-cn', name: 'QoderCN' },
  { id: 'trae', name: 'Trae' },
  { id: 'opencode', name: 'Opencode' },
  { id: 'zcode', name: 'Zcode' },
  { id: 'minimax-code', name: 'MiniMaxCode' },
] as const

const translations = {
  zh: {
    htmlLang: 'zh-CN',
    documentTitle: 'Engineering Calculation System — 工程计算系统',
    metaDescription: 'Engineering Calculation System - AI Agent 工程计算全生命周期交付技能包',
    navAria: '主导航',
    homeAria: '返回首页',
    navItems: [
      { label: '功能', href: '#features' },
      { label: '架构', href: '#architecture' },
      { label: '平台', href: '#platforms' },
      { label: '安装', href: '#install' },
    ],
    language: {
      aria: '切换页面语言',
      zh: '中',
      en: 'EN',
      zhLabel: '中文',
      enLabel: 'English',
    },
    hero: {
      eyebrow: 'v2.6.0 · 全生命周期工程计算技能',
      titlePrimary: '工程计算系统',
      titleSecondary: '全生命周期交付',
      body: '从参考文献采集到可审计的 Web 计算应用，为 AI Agent 赋予完整的工程计算软件全生命周期交付能力。14 步流水线，7 大门控，杜绝跳步。',
      primaryCta: '安装技能包',
      secondaryCta: '了解更多',
      tags: ['Python 3.9+', '7 平台', 'GUI 安装器', '多 Agent 编排'],
    },
    terminal: {
      title: 'ecs-deployment-console',
      command: 'ecs deploy --platform qoder',
      reference: '✓ 参考采集完成（18 个来源）',
      blueprint: '✓ 计算蓝图已生成',
      deployed: '✓ 18 个技能已部署到 Qoder',
      verifying: '▸ 正在运行验证套件...',
      complete: '全部 7 道门控通过 · 部署完成',
    },
    stats: [
      { value: 18, label: '子技能模块', suffix: '' },
      { value: 7, label: '支持平台', suffix: '' },
      { value: 14, label: '生命周期阶段', suffix: '' },
      { value: 7, label: '质量门控', suffix: '' },
    ],
    featuresSection: {
      title: '核心功能',
      subtitle: '覆盖工程计算软件从 0 到 1 的完整交付链路，每个环节都有据可查、可追溯',
    },
    features: [
      {
        icon: '📚',
        title: '参考文献自动采集',
        desc: '主动搜索工程标准、规范、手册，建立本地证据库，来源权威性评级与冲突处理。',
      },
      {
        icon: '📐',
        title: '计算逻辑蓝图',
        desc: '从 PDF/Excel/规范中精准提取公式、查表逻辑、条件分支，生成结构化计算蓝图。',
      },
      {
        icon: '🔒',
        title: '严格质量门控',
        desc: '7 大质量门控贯穿全流程：证据门、分析门、交接门、编码门、报告门、验证门、部署门。',
      },
      {
        icon: '⚡',
        title: '可复用计算模块',
        desc: '解耦的工程计算模块资产库，类型安全的 BookInput/BookResult 模型，跨项目复用。',
      },
      {
        icon: '🖥️',
        title: '生产级 Web UI',
        desc: '左输入/右审查的专业计算书界面，Bootstrap 5 + Jinja2，支持批量导入导出。',
      },
      {
        icon: '🚀',
        title: 'Linux 云端部署',
        desc: 'Docker + systemd + nginx 全套部署方案，一键发布到云服务器。',
      },
    ],
    architecture: {
      title: '14 步生命周期流水线',
      subtitle: '严格门控 + 智能路由，确保工程计算的每一步都有据可查',
      gatesTitle: '7 大质量门控',
      gates: ['证据门', '分析门', '交接门', '编码门', '报告门', '验证门', '部署门'],
    },
    phases: [
      { num: '00', name: '智能路由', desc: '任务分类与路径规划' },
      { num: '01-03', name: '参考采集', desc: '评估 -> 发现 -> 持久化' },
      { num: '04-07', name: '逻辑架构', desc: '摄入 -> 蓝图 -> 提取 -> 交接' },
      { num: '08-11', name: '计算书构建', desc: '架构 -> 模型 -> 模块 -> 运行器' },
      { num: '12', name: '接口层', desc: '报告 / UI / 导入导出' },
      { num: '13', name: '验证追溯', desc: '单元/回归/集成/烟雾测试' },
      { num: '14', name: '云端发布', desc: 'Docker / systemd / nginx' },
    ],
    platformsSection: {
      title: '跨平台一键部署',
      subtitle: '支持 7 个主流 AI Agent 编程平台，GUI 安装器开箱即用',
    },
    install: {
      title: '快速开始',
      subtitle: '一行命令安装，或使用 GUI 安装器图形化部署到目标平台',
      copyAria: '复制或选中安装命令',
      copy: {
        idle: '复制',
        copied: '✓ 已复制',
        selected: '已选中',
        error: '复制失败',
      },
      methods: [
        {
          icon: '🖥️',
          title: 'GUI 安装器',
          desc: '图形化一键部署到 7 个 AI Agent 编程平台',
          command: 'python -m installer_gui',
        },
        {
          icon: '📦',
          title: '构建发布包',
          desc: '为特定平台构建专属 zip 发布包',
          command: 'python build_release.py',
        },
      ],
    },
  },
  en: {
    htmlLang: 'en',
    documentTitle: 'Engineering Calculation System — Full-Lifecycle Delivery',
    metaDescription: 'Engineering Calculation System - full-lifecycle engineering calculation delivery skill pack for AI agents',
    navAria: 'Primary navigation',
    homeAria: 'Back to home',
    navItems: [
      { label: 'Features', href: '#features' },
      { label: 'Pipeline', href: '#architecture' },
      { label: 'Platforms', href: '#platforms' },
      { label: 'Install', href: '#install' },
    ],
    language: {
      aria: 'Switch page language',
      zh: '中',
      en: 'EN',
      zhLabel: '中文',
      enLabel: 'English',
    },
    hero: {
      eyebrow: 'v2.6.0 · Full-lifecycle engineering calculation skill',
      titlePrimary: 'Engineering Calculation System',
      titleSecondary: 'Full-Lifecycle Delivery',
      body: 'From reference acquisition to auditable web calculation apps, ECS gives AI agents a complete delivery workflow for engineering calculation software. 14 pipeline stages, 7 gates, no skipped steps.',
      primaryCta: 'Install skill pack',
      secondaryCta: 'Explore more',
      tags: ['Python 3.9+', '7 platforms', 'GUI installer', 'Multi-agent orchestration'],
    },
    terminal: {
      title: 'ecs-deployment-console',
      command: 'ecs deploy --platform qoder',
      reference: '✓ Reference collection complete (18 sources)',
      blueprint: '✓ Calculation blueprint generated',
      deployed: '✓ 18 skills deployed to Qoder',
      verifying: '▸ Running verification suite...',
      complete: 'All 7 gates passed · Deployment complete',
    },
    stats: [
      { value: 18, label: 'Sub-skill modules', suffix: '' },
      { value: 7, label: 'Supported platforms', suffix: '' },
      { value: 14, label: 'Lifecycle stages', suffix: '' },
      { value: 7, label: 'Quality gates', suffix: '' },
    ],
    featuresSection: {
      title: 'Core Capabilities',
      subtitle: 'A complete delivery path from zero to production-ready engineering calculation software, with evidence and traceability at every step.',
    },
    features: [
      {
        icon: '📚',
        title: 'Automatic Reference Collection',
        desc: 'Searches engineering standards, codes, and handbooks, then builds a local evidence library with authority grading and conflict handling.',
      },
      {
        icon: '📐',
        title: 'Calculation Logic Blueprints',
        desc: 'Extracts formulas, lookup-table logic, and conditional branches from PDFs, Excel workbooks, and standards into structured blueprints.',
      },
      {
        icon: '🔒',
        title: 'Strict Quality Gates',
        desc: 'Seven gates run across the workflow: evidence, analysis, handoff, code, report, verification, and deployment.',
      },
      {
        icon: '⚡',
        title: 'Reusable Calculation Modules',
        desc: 'Decoupled module assets with type-safe BookInput and BookResult models, ready for reuse across projects.',
      },
      {
        icon: '🖥️',
        title: 'Production Web UI',
        desc: 'A professional calculation-book interface with inputs on the left, audit review on the right, and batch import/export support.',
      },
      {
        icon: '🚀',
        title: 'Linux Cloud Deployment',
        desc: 'A complete Docker, systemd, and nginx deployment path for publishing to cloud servers in one pass.',
      },
    ],
    architecture: {
      title: '14-Step Lifecycle Pipeline',
      subtitle: 'Strict gates plus intelligent routing keep every engineering calculation step evidence-backed and traceable.',
      gatesTitle: '7 Quality Gates',
      gates: ['Evidence', 'Analysis', 'Handoff', 'Code', 'Report', 'Verification', 'Deployment'],
    },
    phases: [
      { num: '00', name: 'Smart Routing', desc: 'Task classification and path planning' },
      { num: '01-03', name: 'Reference Collection', desc: 'Assess -> discover -> persist' },
      { num: '04-07', name: 'Logic Architecture', desc: 'Ingest -> blueprint -> extract -> handoff' },
      { num: '08-11', name: 'Calculation Book Build', desc: 'Architecture -> model -> module -> runner' },
      { num: '12', name: 'Interface Layer', desc: 'Reports / UI / import-export' },
      { num: '13', name: 'Verification Traceability', desc: 'Unit / regression / integration / smoke tests' },
      { num: '14', name: 'Cloud Release', desc: 'Docker / systemd / nginx' },
    ],
    platformsSection: {
      title: 'One-Click Cross-Platform Deployment',
      subtitle: 'Supports 7 mainstream AI agent coding platforms, with a GUI installer ready out of the box.',
    },
    install: {
      title: 'Quick Start',
      subtitle: 'Install with one command, or use the GUI installer to deploy to a target platform.',
      copyAria: 'Copy or select install command',
      copy: {
        idle: 'Copy',
        copied: '✓ Copied',
        selected: 'Selected',
        error: 'Copy failed',
      },
      methods: [
        {
          icon: '🖥️',
          title: 'GUI Installer',
          desc: 'Deploy to 7 AI agent coding platforms from a guided graphical installer.',
          command: 'python -m installer_gui',
        },
        {
          icon: '📦',
          title: 'Build Release Package',
          desc: 'Create a platform-specific zip package for distribution.',
          command: 'python build_release.py',
        },
      ],
    },
  },
} as const

type Language = keyof typeof translations
type Translation = (typeof translations)[Language]
type PlatformId = (typeof platforms)[number]['id']
type CopyState = 'idle' | 'copied' | 'selected' | 'error'

const platformLogoSrc: Record<PlatformId, string> = {
  codex: codexLogo,
  qoder: qoderLogo,
  'qoder-cn': qoderCnLogo,
  trae: traeLogo,
  opencode: opencodeLogo,
  zcode: zcodeLogo,
  'minimax-code': minimaxCodeLogo,
}

function getInitialLanguage(): Language {
  const saved = window.localStorage.getItem(LANGUAGE_STORAGE_KEY)
  return saved === 'en' ? 'en' : 'zh'
}

function selectElementText(element: HTMLElement) {
  const selection = window.getSelection()
  const range = document.createRange()
  range.selectNodeContents(element)
  selection?.removeAllRanges()
  selection?.addRange(range)
}

async function copyToClipboard(text: string, fallbackElement?: HTMLElement | null): Promise<'copied' | 'selected'> {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text)
      return 'copied'
    } catch {
      // Fall back to selection when the browser denies clipboard writes.
    }
  }

  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'fixed'
  textarea.style.top = '0'
  textarea.style.left = '0'
  textarea.style.opacity = '0'
  document.body.appendChild(textarea)
  textarea.focus()
  textarea.select()
  textarea.setSelectionRange(0, text.length)
  const copied = document.execCommand('copy')
  textarea.remove()

  if (copied) {
    return 'copied'
  }

  if (fallbackElement) {
    selectElementText(fallbackElement)
    return 'selected'
  }

  throw new Error('Clipboard copy failed')
}

// ---- Animation Variants ----
const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.6, ease: [0.4, 0, 0.2, 1] as [number, number, number, number] },
  }),
}

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
}

// ---- Particles Background ----
function ParticlesCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let animId: number | undefined
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const particles: { x: number; y: number; vx: number; vy: number; r: number; o: number }[] = []

    const resize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resize()
    window.addEventListener('resize', resize, { passive: true })

    for (let i = 0; i < 50; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 1.2 + 0.3,
        o: Math.random() * 0.4 + 0.1,
      })
    }

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      particles.forEach((p) => {
        p.x += p.vx
        p.y += p.vy
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(0,94,184,${p.o})`
        ctx.fill()
      })

      // Draw connections
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x
          const dy = particles[i].y - particles[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < 120) {
            ctx.beginPath()
            ctx.moveTo(particles[i].x, particles[i].y)
            ctx.lineTo(particles[j].x, particles[j].y)
            ctx.strokeStyle = `rgba(0,94,184,${0.06 * (1 - dist / 120)})`
            ctx.lineWidth = 0.6
            ctx.stroke()
          }
        }
      }
      if (!prefersReducedMotion) {
        animId = requestAnimationFrame(draw)
      }
    }
    draw()

    return () => {
      if (animId) cancelAnimationFrame(animId)
      window.removeEventListener('resize', resize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      className="fixed inset-0 pointer-events-none z-0"
      style={{ opacity: 0.6 }}
    />
  )
}

// ---- Counter Animation ----
function Counter({ value, suffix = '' }: { value: number; suffix?: string }) {
  const [count, setCount] = useState(0)
  const ref = useRef<HTMLSpanElement>(null)
  const isInView = useInView(ref, { once: true })

  useEffect(() => {
    if (!isInView) return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setCount(value)
      return
    }

    let current = 0
    const step = Math.ceil(value / 30)
    const timer = setInterval(() => {
      current += step
      if (current >= value) {
        current = value
        clearInterval(timer)
      }
      setCount(current)
    }, 40)
    return () => clearInterval(timer)
  }, [isInView, value])

  return (
    <span ref={ref} className="font-mono text-4xl md:text-5xl font-bold text-primary">
      {count}{suffix}
    </span>
  )
}

// ---- Section Wrapper ----
function Section({ id, children, className = '', dark = false }: {
  id?: string; children: ReactNode; className?: string; dark?: boolean
}) {
  return (
    <section
      id={id}
      className={`relative py-24 md:py-32 px-6 ${dark ? 'bg-[#0F172A] text-white' : 'bg-white'} ${className}`}
    >
      <div className="max-w-7xl mx-auto">{children}</div>
    </section>
  )
}

function LanguageToggle({
  language,
  labels,
  onChange,
}: {
  language: Language
  labels: Translation['language']
  onChange: (language: Language) => void
}) {
  const options: { value: Language; shortLabel: string; ariaLabel: string }[] = [
    { value: 'zh', shortLabel: labels.zh, ariaLabel: labels.zhLabel },
    { value: 'en', shortLabel: labels.en, ariaLabel: labels.enLabel },
  ]

  return (
    <div
      role="group"
      aria-label={labels.aria}
      className="inline-flex h-9 shrink-0 items-center rounded-lg border border-border bg-white/75 p-0.5 shadow-sm"
    >
      {options.map((option) => {
        const active = language === option.value
        return (
          <button
            key={option.value}
            type="button"
            aria-label={option.ariaLabel}
            aria-pressed={active}
            onClick={() => onChange(option.value)}
            className={`h-8 w-10 rounded-md text-xs font-semibold transition-colors ${
              active
                ? 'bg-primary text-white shadow-sm'
                : 'text-text3 hover:bg-accent-pale hover:text-primary'
            }`}
          >
            {option.shortLabel}
          </button>
        )
      })}
    </div>
  )
}

function PlatformLogo({ id, name }: { id: PlatformId; name: string }) {
  return (
    <img
      src={platformLogoSrc[id]}
      alt={`${name} logo`}
      loading="lazy"
      decoding="async"
      className="mx-auto h-14 w-14 object-contain transition-transform duration-300 group-hover:scale-105"
    />
  )
}

// ---- Navbar ----
function Navbar({
  language,
  t,
  onLanguageChange,
}: {
  language: Language
  t: Translation
  onLanguageChange: (language: Language) => void
}) {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 60)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav aria-label={t.navAria} className={`fixed top-0 left-0 right-0 z-50 nav-glass transition-all duration-300 ${scrolled ? 'scrolled' : ''}`}>
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <a href="#top" aria-label={t.homeAria} className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-sm">
            E
          </div>
          <span className="font-bold text-lg text-text">ECS</span>
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
            className="btn-primary !py-2 !px-4 sm:!px-5 !text-sm !rounded-lg whitespace-nowrap"
          >
            {t.install.title}
          </a>
        </div>
      </div>
    </nav>
  )
}

// ---- Hero Section ----
function Hero({ t }: { t: Translation }) {
  const { scrollY } = useScroll()
  const y = useTransform(scrollY, [0, 500], [0, 150])
  const opacity = useTransform(scrollY, [0, 400], [1, 0])

  return (
    <section id="top" className="relative min-h-[800px] flex items-center overflow-hidden">
      {/* Background layers */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#F8FBFF] via-white to-[#E8F1F8]" />
      <div className="absolute inset-0 blueprint-bg" />

      <motion.div style={{ y, opacity }} className="relative z-10 max-w-7xl mx-auto px-6 py-32 grid md:grid-cols-2 gap-16 items-center w-full">
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
              <span key={tag} className="px-3 py-1 text-xs font-medium rounded-full bg-bg2 text-text3 border border-border">
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
          className="hidden md:block"
        >
          <div className="product-window animate-float">
            <div className="window-titlebar">
              <div className="window-dot bg-[#FF5F56]" />
              <div className="window-dot bg-[#FFBD2E]" />
              <div className="window-dot bg-[#27C93F]" />
              <span className="text-white/60 text-xs ml-3 font-mono">{t.terminal.title}</span>
            </div>
            <div className="bg-[#0F172A] p-6 dark-blueprint-bg">
              {/* Simulated terminal output */}
              <div className="space-y-3 font-mono text-sm">
                <div className="flex items-center gap-2">
                  <span className="text-primary-light">$</span>
                  <span className="text-white/80">{t.terminal.command}</span>
                </div>
                <div className="text-success text-xs">
                  {t.terminal.reference}
                </div>
                <div className="text-success text-xs">
                  {t.terminal.blueprint}
                </div>
                <div className="text-success text-xs">
                  {t.terminal.deployed}
                </div>
                <div className="text-primary-light text-xs">
                  {t.terminal.verifying}
                </div>
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
        </motion.div>
      </motion.div>
    </section>
  )
}

// ---- Stats Row ----
function StatsRow({ stats }: { stats: Translation['stats'] }) {
  return (
    <section className="relative py-16 bg-bg2 border-y border-border">
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
              className="text-center"
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

// ---- Features Grid ----
function Features({ t }: { t: Translation }) {
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
          <motion.div key={f.title} variants={fadeUp} custom={i} className="glass-card p-8">
            <div className="w-14 h-14 rounded-lg bg-accent-pale flex items-center justify-center text-2xl mb-5">
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

// ---- Architecture Timeline ----
function Architecture({ t }: { t: Translation }) {
  return (
    <Section id="architecture" dark className="overflow-hidden">
      <div className="absolute inset-0 dark-blueprint-bg opacity-30" />
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
          <motion.p variants={fadeUp} className="text-white/60 max-w-2xl mx-auto">
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
              className="relative p-6 rounded-lg border border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 hover:border-primary/30 transition-all duration-300 group"
            >
              <div className="font-mono text-xs text-primary-light mb-2">{p.num}</div>
              <h3 className="font-bold text-lg mb-2 group-hover:text-primary-light transition-colors">
                {p.name}
              </h3>
              <p className="text-sm text-white/50">{p.desc}</p>
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
          className="mt-16 p-8 rounded-lg border border-primary/20 bg-primary/5 backdrop-blur-sm"
        >
          <h3 className="font-bold text-lg mb-6 text-center text-white/90">{t.architecture.gatesTitle}</h3>
          <div className="flex flex-wrap justify-center gap-3">
            {t.architecture.gates.map((gate, i) => (
              <motion.div
                key={gate}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: 0.6 + i * 0.08 }}
                className="px-4 py-2 rounded-full border border-primary/30 bg-primary/10 text-sm font-medium text-primary-light"
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

// ---- Platform Support ----
function Platforms({ t }: { t: Translation }) {
  return (
    <Section id="platforms">
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
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        {platforms.map((p, i) => (
          <motion.div
            key={p.name}
            variants={fadeUp}
            custom={i}
            aria-label={p.name}
            className="glass-card min-h-[150px] p-6 text-center group cursor-pointer flex flex-col items-center justify-center gap-4"
          >
            <PlatformLogo id={p.id} name={p.name} />
            <h3 className="font-bold text-sm text-text">{p.name}</h3>
          </motion.div>
        ))}
      </motion.div>
    </Section>
  )
}

// ---- Install CTA ----
function Install({ t }: { t: Translation }) {
  const installCommandRef = useRef<HTMLElement>(null)
  const [copyState, setCopyState] = useState<CopyState>('idle')

  const handleCopy = async () => {
    try {
      const result = await copyToClipboard(INSTALL_COMMAND, installCommandRef.current)
      setCopyState(result)
    } catch {
      setCopyState('error')
    } finally {
      window.setTimeout(() => setCopyState('idle'), 2000)
    }
  }

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
          <div className="bg-[#0F172A] rounded-lg p-6 text-left dark-blueprint-bg overflow-hidden">
            <div className="flex items-center gap-2 mb-4">
              <div className="window-dot bg-[#FF5F56]" />
              <div className="window-dot bg-[#FFBD2E]" />
              <div className="window-dot bg-[#27C93F]" />
              <span className="text-white/40 text-xs ml-2 font-mono">terminal</span>
            </div>
            <div className="font-mono text-sm flex items-center gap-3">
              <span className="text-primary-light">$</span>
              <code ref={installCommandRef} className="text-white/90 flex-1">{INSTALL_COMMAND}</code>
              <button
                type="button"
                onClick={handleCopy}
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
            <div key={method.title} className="glass-card p-6 text-left">
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

// ---- Footer ----
function Footer() {
  return (
    <footer className="bg-[#0F172A] text-white/60 py-12 px-6 border-t border-white/5">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-sm">
              E
            </div>
            <span className="font-bold text-white">Engineering Calculation System</span>
          </div>
          <div className="flex items-center gap-6 text-sm">
            <a href="https://zjic-international.com" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              ZJIC International
            </a>
            <span className="text-white/20">|</span>
            <span>v2.6.0</span>
            <span className="text-white/20">|</span>
            <span>© {new Date().getFullYear()}</span>
          </div>
        </div>
      </div>
    </footer>
  )
}

// ---- Main App ----
export default function App() {
  const [language, setLanguage] = useState<Language>(getInitialLanguage)
  const t = translations[language]

  useEffect(() => {
    window.localStorage.setItem(LANGUAGE_STORAGE_KEY, language)
    document.documentElement.lang = t.htmlLang
    document.title = t.documentTitle

    const metaDescription = document.querySelector<HTMLMetaElement>('meta[name="description"]')
    metaDescription?.setAttribute('content', t.metaDescription)
  }, [language, t])

  return (
    <div className="relative">
      <ParticlesCanvas />
      <Navbar language={language} t={t} onLanguageChange={setLanguage} />
      <main>
        <Hero t={t} />
        <StatsRow stats={t.stats} />
        <Features t={t} />
        <Architecture t={t} />
        <Platforms t={t} />
        <Install t={t} />
      </main>
      <Footer />
    </div>
  )
}
