/* ============================================
   ECS Homepage — Translations (zh/en)
   ============================================ */

import { APP_VERSION } from '@/data/constants'

export const translations = {
  zh: {
    htmlLang: 'zh-CN',
    documentTitle: 'Engineering Calculation System — 工程计算系统',
    metaDescription: 'Engineering Calculation System - AI Agent 工程计算全生命周期交付技能包',
    navAria: '主导航',
    homeAria: '返回首页',
    mobileMenu: {
      open: '打开导航菜单',
      close: '关闭导航菜单',
    },
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
      eyebrow: `v${APP_VERSION} · 全生命周期工程计算技能`,
      titlePrimary: '工程计算系统',
      titleSecondary: '全生命周期交付',
      body: '从参考文献采集到可审计的 Web 计算应用，为 AI Agent 赋予完整的工程计算软件全生命周期交付能力。14 步流水线，7 大门控，杜绝跳步。',
      primaryCta: '安装技能包',
      secondaryCta: '了解更多',
      tags: ['Python 3.9+', '7 平台', 'GUI 安装器', '多 Agent 编排'],
    },
    terminal: {
      title: 'ecs-skill-orchestrator',
      command: 'ecs skill run --workflow calculation-book',
      reference: '✓ 参考采集完成（18 个来源）',
      blueprint: '✓ 计算蓝图已生成',
      deployed: '✓ 18 个技能已安装到 Qoder',
      verifying: '▸ 正在运行验证套件...',
      complete: '全部 7 道门控通过 · 交付闭环完成',
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
        desc: '7 大质量门控贯穿全流程：证据门、分析门、交接门、编码门、报告门、验证门、交付门。',
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
        title: '工程交付闭环',
        desc: '把证据、蓝图、模块、Web UI、报告与验证连接成可复用、可审计的工程计算交付件。',
      },
    ],
    architecture: {
      title: '14 步生命周期流水线',
      subtitle: '严格门控 + 智能路由，确保工程计算的每一步都有据可查',
      gatesTitle: '7 大质量门控',
      gates: ['证据门', '分析门', '交接门', '编码门', '报告门', '验证门', '交付门'],
    },
    phases: [
      { num: '00', name: '智能路由', desc: '任务分类与路径规划' },
      { num: '01-03', name: '参考采集', desc: '评估 -> 发现 -> 持久化' },
      { num: '04-07', name: '逻辑架构', desc: '摄入 -> 蓝图 -> 提取 -> 交接' },
      { num: '08-11', name: '计算书构建', desc: '架构 -> 模型 -> 模块 -> 运行器' },
      { num: '12', name: '接口层', desc: '报告 / UI / 导入导出' },
      { num: '13', name: '验证追溯', desc: '单元/回归/集成/烟雾测试' },
      { num: '14', name: '交付闭环', desc: 'UI / 报告 / 验证资产' },
    ],
    platformsSection: {
      title: '跨平台一键安装',
      subtitle: '支持 7 个主流 AI Agent 编程平台，GUI 安装器开箱即用',
    },
    install: {
      title: '快速开始',
      subtitle: '一行命令安装，或使用 GUI 安装器图形化接入目标平台',
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
          desc: '图形化安装 ECS 技能包，快速接入 7 个 AI Agent 编程平台',
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
    footer: {
      description: '面向 AI Agent 的工程计算交付技能包，把证据、公式、模块、Web UI 与验证串成可复用闭环。',
      productTitle: '产品',
      companyTitle: '组织',
      versionLabel: '版本',
      copyrightPrefix: '版权所有',
      website: 'ZJIC International',
    },
    scrollToTop: '回到顶部',
  },
  en: {
    htmlLang: 'en',
    documentTitle: 'Engineering Calculation System — Full-Lifecycle Delivery',
    metaDescription: 'Engineering Calculation System - full-lifecycle engineering calculation delivery skill pack for AI agents',
    navAria: 'Primary navigation',
    homeAria: 'Back to home',
    mobileMenu: {
      open: 'Open navigation menu',
      close: 'Close navigation menu',
    },
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
      eyebrow: `v${APP_VERSION} · Full-lifecycle engineering calculation skill`,
      titlePrimary: 'Engineering Calculation System',
      titleSecondary: 'Full-Lifecycle Delivery',
      body: 'From reference acquisition to auditable web calculation apps, ECS gives AI agents a complete delivery workflow for engineering calculation software. 14 pipeline stages, 7 gates, no skipped steps.',
      primaryCta: 'Install skill pack',
      secondaryCta: 'Explore more',
      tags: ['Python 3.9+', '7 platforms', 'GUI installer', 'Multi-agent orchestration'],
    },
    terminal: {
      title: 'ecs-skill-orchestrator',
      command: 'ecs skill run --workflow calculation-book',
      reference: '✓ Reference collection complete (18 sources)',
      blueprint: '✓ Calculation blueprint generated',
      deployed: '✓ 18 skills installed into Qoder',
      verifying: '▸ Running verification suite...',
      complete: 'All 7 gates passed · Delivery loop complete',
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
        desc: 'Seven gates run across the workflow: evidence, analysis, handoff, code, report, verification, and delivery.',
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
        title: 'Delivery Closure',
        desc: 'Connects evidence, blueprints, modules, web UI, reports, and verification into reusable auditable engineering calculation deliverables.',
      },
    ],
    architecture: {
      title: '14-Step Lifecycle Pipeline',
      subtitle: 'Strict gates plus intelligent routing keep every engineering calculation step evidence-backed and traceable.',
      gatesTitle: '7 Quality Gates',
      gates: ['Evidence', 'Analysis', 'Handoff', 'Code', 'Report', 'Verification', 'Delivery'],
    },
    phases: [
      { num: '00', name: 'Smart Routing', desc: 'Task classification and path planning' },
      { num: '01-03', name: 'Reference Collection', desc: 'Assess -> discover -> persist' },
      { num: '04-07', name: 'Logic Architecture', desc: 'Ingest -> blueprint -> extract -> handoff' },
      { num: '08-11', name: 'Calculation Book Build', desc: 'Architecture -> model -> module -> runner' },
      { num: '12', name: 'Interface Layer', desc: 'Reports / UI / import-export' },
      { num: '13', name: 'Verification Traceability', desc: 'Unit / regression / integration / smoke tests' },
      { num: '14', name: 'Delivery Closure', desc: 'UI / reports / verified assets' },
    ],
    platformsSection: {
      title: 'One-Click Cross-Platform Installation',
      subtitle: 'Supports 7 mainstream AI agent coding platforms, with a GUI installer ready out of the box.',
    },
    install: {
      title: 'Quick Start',
      subtitle: 'Install with one command, or use the GUI installer to connect ECS to a target platform.',
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
          desc: 'Install the ECS skill pack into 7 AI agent coding platforms from a guided graphical installer.',
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
    footer: {
      description: 'A delivery skill pack for AI agents that connects evidence, formulas, modules, web UIs, and verification into reusable engineering calculation workflows.',
      productTitle: 'Product',
      companyTitle: 'Organization',
      versionLabel: 'Version',
      copyrightPrefix: 'Copyright',
      website: 'ZJIC International',
    },
    scrollToTop: 'Back to top',
  },
} as const
