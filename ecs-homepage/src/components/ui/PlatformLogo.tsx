/* ============================================
   ECS Homepage — Platform Logo Component
   ============================================ */

import { platformLogoSrc } from '@/data/platforms'
import type { PlatformId } from '@/types'

export default function PlatformLogo({ id, name }: { id: PlatformId; name: string }) {
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
