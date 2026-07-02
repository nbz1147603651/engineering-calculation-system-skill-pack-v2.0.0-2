/* ============================================
   ECS Homepage — Section Layout Components
   ============================================ */

import type { ReactNode } from 'react'

export function Section({ id, children, className = '' }: {
  id?: string; children: ReactNode; className?: string
}) {
  return (
    <section
      id={id}
      className={`cv-section relative bg-white py-24 px-6 md:py-32 ${className}`}
    >
      <div className="max-w-7xl mx-auto">{children}</div>
    </section>
  )
}
