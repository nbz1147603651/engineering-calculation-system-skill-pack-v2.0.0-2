/* ============================================
   ECS Homepage — Counter Animation Component
   ============================================ */

import { useEffect, useRef, useState } from 'react'
import { useInView } from 'framer-motion'

export default function Counter({ value, suffix = '' }: { value: number; suffix?: string }) {
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
