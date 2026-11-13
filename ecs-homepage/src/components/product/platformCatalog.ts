import { platformLogoSrc } from "@/data/platforms";
import deepseekHarnessLogo from "@/assets/platform-logos/deepseek-harness.svg";

export const agentCatalog: { id: string; name: string; logo: string }[] = [
  { id: "codex", name: "Codex", logo: platformLogoSrc.codex },
  { id: "opencode", name: "OpenCode", logo: platformLogoSrc.opencode },
  { id: "dsh", name: "DeepSeek Harness", logo: deepseekHarnessLogo },
  { id: "qoder", name: "Qoder", logo: platformLogoSrc.qoder },
  { id: "qoder-cn", name: "QoderCN", logo: platformLogoSrc["qoder-cn"] },
  {
    id: "qoderwork-cn",
    name: "QoderWorkCN",
    logo: platformLogoSrc["qoderwork-cn"],
  },
  { id: "workbuddy", name: "WorkBuddy", logo: platformLogoSrc.workbuddy },
  { id: "trae", name: "Trae", logo: platformLogoSrc.trae },
  { id: "zcode", name: "ZCode", logo: platformLogoSrc.zcode },
  {
    id: "minimax-code",
    name: "MiniMaxCode",
    logo: platformLogoSrc["minimax-code"],
  },
];

export function platformDetails(id: string) {
  return agentCatalog.find((platform) => platform.id === id) ?? agentCatalog[2];
}

export function platformMethod(id: string, language: "zh" | "en") {
  const plugin = ["dsh", "codex", "qoderwork-cn", "workbuddy", "zcode"].includes(id);
  if (plugin) return language === "zh" ? "原生插件与工程技能" : "Native plugin & engineering skills";
  return language === "zh" ? "平台适配与工程技能" : "Platform adapter & engineering skills";
}
