/* ============================================
   ECS Homepage — Particles Background Effect
   ============================================ */

import { useEffect, useRef } from 'react'

export default function ParticlesCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let animId: number | undefined
    let width = window.innerWidth
    let height = window.innerHeight
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const pointer = { x: width * 0.68, y: height * 0.38, active: false }
    const palette = [
      '0,94,184',
      '65,142,216',
      '8,145,178',
      '0,48,135',
    ]
    const particles: { x: number; y: number; vx: number; vy: number; r: number; o: number; tone: string }[] = []
    const connectionDistance = 120

    const resize = () => {
      width = window.innerWidth
      height = window.innerHeight
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      canvas.width = Math.floor(width * dpr)
      canvas.height = Math.floor(height * dpr)
      canvas.style.width = `${width}px`
      canvas.style.height = `${height}px`
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    }
    resize()
    window.addEventListener('resize', resize, { passive: true })

    const movePointer = (event: PointerEvent) => {
      pointer.x = event.clientX
      pointer.y = event.clientY
      pointer.active = true
    }
    const leavePointer = () => {
      pointer.active = false
    }
    window.addEventListener('pointermove', movePointer, { passive: true })
    window.addEventListener('pointerleave', leavePointer, { passive: true })

    for (let i = 0; i < 64; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.22,
        vy: (Math.random() - 0.5) * 0.22,
        r: Math.random() * 1.2 + 0.3,
        o: Math.random() * 0.34 + 0.08,
        tone: palette[i % palette.length],
      })
    }

    const draw = () => {
      ctx.clearRect(0, 0, width, height)
      const time = performance.now() * 0.001
      const sweepX = ((time * 72) % (width + 280)) - 140
      const sweep = ctx.createLinearGradient(sweepX - 80, 0, sweepX + 80, 0)
      sweep.addColorStop(0, 'rgba(0,94,184,0)')
      sweep.addColorStop(0.5, 'rgba(65,142,216,0.12)')
      sweep.addColorStop(1, 'rgba(0,94,184,0)')
      ctx.fillStyle = sweep
      ctx.fillRect(sweepX - 80, 0, 160, height)

      particles.forEach((p) => {
        const dxp = p.x - pointer.x
        const dyp = p.y - pointer.y
        const pointerDistance = Math.sqrt(dxp * dxp + dyp * dyp)
        if (pointer.active && pointerDistance < 180) {
          p.vx += (dxp / Math.max(pointerDistance, 1)) * 0.006
          p.vy += (dyp / Math.max(pointerDistance, 1)) * 0.006
        }
        p.vx *= 0.995
        p.vy *= 0.995
        p.x += p.vx
        p.y += p.vy
        if (p.x < 0 || p.x > width) p.vx *= -1
        if (p.y < 0 || p.y > height) p.vy *= -1
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(${p.tone},${p.o})`
        ctx.fill()
      })

      const grid = new Map<string, number[]>()
      for (let i = 0; i < particles.length; i++) {
        const cellX = Math.floor(particles[i].x / connectionDistance)
        const cellY = Math.floor(particles[i].y / connectionDistance)
        const key = `${cellX}:${cellY}`
        const cell = grid.get(key)
        if (cell) {
          cell.push(i)
        } else {
          grid.set(key, [i])
        }
      }

      for (let i = 0; i < particles.length; i++) {
        const cellX = Math.floor(particles[i].x / connectionDistance)
        const cellY = Math.floor(particles[i].y / connectionDistance)

        for (let offsetX = -1; offsetX <= 1; offsetX++) {
          for (let offsetY = -1; offsetY <= 1; offsetY++) {
            const neighborIndexes = grid.get(`${cellX + offsetX}:${cellY + offsetY}`)
            if (!neighborIndexes) continue

            for (const j of neighborIndexes) {
              if (j <= i) continue

          const dx = particles[i].x - particles[j].x
          const dy = particles[i].y - particles[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)
              if (dist < connectionDistance) {
            ctx.beginPath()
            ctx.moveTo(particles[i].x, particles[i].y)
            ctx.lineTo(particles[j].x, particles[j].y)
                ctx.strokeStyle = `rgba(0,94,184,${0.075 * (1 - dist / connectionDistance)})`
            ctx.lineWidth = 0.6
            ctx.stroke()
              }
            }
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
      window.removeEventListener('pointermove', movePointer)
      window.removeEventListener('pointerleave', leavePointer)
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
