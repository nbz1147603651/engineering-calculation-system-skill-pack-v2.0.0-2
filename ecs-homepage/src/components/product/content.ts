import { useEffect, useState } from "react";
import { APP_VERSION, LANGUAGE_STORAGE_KEY } from "@/data/constants";

export type ProductLanguage = "zh" | "en";
export const productCopy = {
  zh: {
    title: "NIMO Engineering · 工程计算助手",
    description:
      "NIMO Engineering 将工程资料、计算蓝图、实现与验证串成可追溯的交付流程，支持 Codex、OpenCode、DeepSeekHarness 等 Agent。",
    skip: "跳到主要内容",
    nav: ["产品概览", "工作流程", "Agent 平台"],
    menu: "切换导航菜单",
    download: "下载客户端",
    heading: ["让工程计算，", "有据可循。"],
    intro:
      "从资料、公式到可复核的计算成果。NIMO Engineering 将工程经验整理成可复用的技能，让你熟悉的 Agent 协助完成可靠交付。",
    explore: "探索工作流程",
    runtime: `Windows 客户端 · 本地运行 · v${APP_VERSION}`,
    preview: "客户端预览",
    connect: "连接你的 Agent",
    shared: "延续你的习惯，让工程更高效",
    previewState: "示例平台",
    previewNote: "准备好，把复杂交给 Nimo。",
    rail: "适配你的工作方式",
    overview: "把复杂流程，变成清晰的下一步。",
    pillars: [
      [
        "明确依据",
        "整理工程资料、设计条件与计算依据，形成可复用、可追溯的输入。",
      ],
      [
        "开展计算",
        "梳理公式、方法与参数，让工程经验成为可重复使用的计算方法。",
      ],
      ["验证交付", "校核计算过程与结果，保留完整流程记录，支持审查与追溯。"],
    ],
    workflow: ["从下一步开始，", "而不是从头再来。"],
    workflowIntro:
      "新项目走完整链路；小修改只回到受影响的阶段。资料与公式有出处，验证记录可追溯。",
    routes: ["开始新的计算", "调整计算方法", "整理参考资料"],
    stages: [
      ["需求与依据", "明确条件，保存来源"],
      ["计算方法", "核对公式、单位与适用范围"],
      ["计算与成果", "整理过程，形成所需成果"],
      ["校核与交付", "核验结果，保留可追溯记录"],
    ],
    routeNotes: [
      "从明确依据到成果校核，逐步完成工程任务",
      "沿用已确认的依据，重新校核受影响的成果；条件变化时重新梳理资料",
      "整理可靠来源，标注适用条件，方便后续查阅与引用",
    ],
    platforms: "选择你熟悉的 Agent。",
    platformsIntro: "延续工作习惯，轻松开始。",
    more: "更多平台",
    less: "收起平台",
    method: "开始使用",
    location: "适用场景",
    details: "开始使用",
    compatibility: "同时支持",
    installTitle: "让 Nimo 加入你的下一个项目。",
    installIntro:
      "下载桌面客户端，检测可用平台并安装工程技能。已有项目按需接入，运行结果留在本地。",
    desktop: "Windows 桌面客户端",
    installer: `安装程序 · v${APP_VERSION}`,
    guide: "轻松开始",
    steps: [
      "下载并启动客户端",
      "检测平台，确认目标路径",
      "安装技能，开始工程任务",
    ],
    footer: "工程有依据，交付可追溯。",
    rights: "NIMO Software",
  },
  en: {
    title: "NIMO Engineering · Engineering assistant",
    description:
      "Traceable engineering delivery, from sources and calculation blueprints to implementation and verification. Connect Codex, OpenCode, DeepSeekHarness and more.",
    skip: "Skip to content",
    nav: ["Overview", "Workflow", "Agent platforms"],
    menu: "Toggle navigation",
    download: "Download client",
    heading: ["Engineering calculations,", "with a clear foundation."],
    intro:
      "From sources and formulas to calculations you can review. NIMO Engineering turns engineering knowledge into reusable skills for the agents you already use.",
    explore: "Explore the workflow",
    runtime: `Windows client · Runs locally · v${APP_VERSION}`,
    preview: "Client preview",
    connect: "Connect your agent",
    shared: "Familiar tools. Better engineering.",
    previewState: "Example platform",
    previewNote: "Ready? Leave the complexity to Nimo.",
    rail: "Fits the way you work",
    overview: "A clear next step for complex work.",
    pillars: [
      [
        "Establish evidence",
        "Organize sources, design conditions and calculation assumptions into traceable inputs.",
      ],
      [
        "Work through calculations",
        "Organize formulas, methods and parameters into engineering methods you can reuse.",
      ],
      [
        "Verify delivery",
        "Check the process and results, retaining reproducible records for review.",
      ],
    ],
    workflow: ["Start at the next step,", "without starting over."],
    workflowIntro:
      "Use the full path for new projects. Resume affected stages for small changes. Keep sources explicit and verification traceable.",
    routes: ["Start a calculation", "Adjust a method", "Organize sources"],
    stages: [
      ["Requirements & evidence", "Define conditions and preserve sources"],
      ["Calculation methods", "Check formulas, units and applicability"],
      ["Calculations & results", "Document the process and prepare results"],
      ["Review & delivery", "Verify results and preserve traceable records"],
    ],
    routeNotes: [
      "Work through the task, from clear evidence to reviewed results",
      "Reuse confirmed evidence and recheck affected results; revisit sources when conditions change",
      "Organize reliable sources with clear applicability for future use",
    ],
    platforms: "Choose your familiar agent.",
    platformsIntro: "Keep your workflow. Get started easily.",
    more: "More platforms",
    less: "Fewer platforms",
    method: "Get started",
    location: "Use cases",
    details: "Get started",
    compatibility: "Also supports",
    installTitle: "Bring Nimo to your next project.",
    installIntro:
      "Download the desktop client, discover available platforms and install engineering skills. Connect existing projects as needed and keep results local.",
    desktop: "Windows desktop client",
    installer: `Installer · v${APP_VERSION}`,
    guide: "Get started easily",
    steps: [
      "Download and open the client",
      "Detect platforms and confirm the target",
      "Install skills and start engineering",
    ],
    footer: "Grounded engineering. Traceable delivery.",
    rights: "NIMO Software",
  },
};
export type ProductCopy = (typeof productCopy)[ProductLanguage];

export function useProductLanguage() {
  const [language, setLanguage] = useState<ProductLanguage>(() => {
    try {
      return localStorage.getItem(LANGUAGE_STORAGE_KEY) === "en" ? "en" : "zh";
    } catch {
      return "zh";
    }
  });
  const copy = productCopy[language];
  useEffect(() => {
    try {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, language);
    } catch {
      /* Storage may be disabled. */
    }
    document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
    document.title = copy.title;
    document
      .querySelector('meta[name="description"]')
      ?.setAttribute("content", copy.description);
  }, [language, copy]);
  return { language, setLanguage, copy };
}
