/* ============================================
   ECS Homepage — Platform Data
   ============================================ */

import codexLogo from "@/assets/platform-logos/codex.png";
import minimaxCodeLogo from "@/assets/platform-logos/minimax-code.png";
import opencodeLogo from "@/assets/platform-logos/opencode.png";
import qoderCnLogo from "@/assets/platform-logos/qoder-cn.png";
import qoderLogo from "@/assets/platform-logos/qoder.svg";
import qoderWorkCnLogo from "@/assets/platform-logos/qoderwork-cn.png";
import traeLogo from "@/assets/platform-logos/trae.png";
import workBuddyLogo from "@/assets/platform-logos/workbuddy.png";
import zcodeLogo from "@/assets/platform-logos/zcode.png";

export const platforms = [
  { id: "codex", name: "Codex" },
  { id: "qoder", name: "Qoder" },
  { id: "qoder-cn", name: "QoderCN" },
  { id: "qoderwork-cn", name: "QoderWorkCN" },
  { id: "workbuddy", name: "WorkBuddy" },
  { id: "trae", name: "Trae" },
  { id: "opencode", name: "Opencode" },
  { id: "zcode", name: "ZCode" },
  { id: "minimax-code", name: "MiniMaxCode" },
] as const;

export const platformLogoSrc: Record<(typeof platforms)[number]["id"], string> =
  {
    codex: codexLogo,
    qoder: qoderLogo,
    "qoder-cn": qoderCnLogo,
    "qoderwork-cn": qoderWorkCnLogo,
    workbuddy: workBuddyLogo,
    trae: traeLogo,
    opencode: opencodeLogo,
    zcode: zcodeLogo,
    "minimax-code": minimaxCodeLogo,
  };
