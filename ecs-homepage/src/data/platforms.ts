/* ============================================
   ECS Homepage — Platform Data
   ============================================ */

import codexLogo from '@/assets/platform-logos/codex.png'
import minimaxCodeLogo from '@/assets/platform-logos/minimax-code.png'
import opencodeLogo from '@/assets/platform-logos/opencode.png'
import qoderCnLogo from '@/assets/platform-logos/qoder-cn.png'
import qoderLogo from '@/assets/platform-logos/qoder.svg'
import traeLogo from '@/assets/platform-logos/trae.png'
import zcodeLogo from '@/assets/platform-logos/zcode.png'
import type { PlatformId } from '@/types'

export const platforms = [
  { id: 'codex', name: 'Codex' },
  { id: 'qoder', name: 'Qoder' },
  { id: 'qoder-cn', name: 'QoderCN' },
  { id: 'trae', name: 'Trae' },
  { id: 'opencode', name: 'Opencode' },
  { id: 'zcode', name: 'ZCode' },
  { id: 'minimax-code', name: 'MiniMaxCode' },
] as const

export const platformLogoSrc: Record<PlatformId, string> = {
  codex: codexLogo,
  qoder: qoderLogo,
  'qoder-cn': qoderCnLogo,
  trae: traeLogo,
  opencode: opencodeLogo,
  zcode: zcodeLogo,
  'minimax-code': minimaxCodeLogo,
}
