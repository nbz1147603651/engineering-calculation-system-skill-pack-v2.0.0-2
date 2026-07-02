/* ============================================
   ECS Homepage — Constants
   ============================================ */

export const INSTALL_COMMAND = 'pip install engineering-calculation-system'
export const LANGUAGE_STORAGE_KEY = 'ecs-homepage-language'
export const APP_VERSION = __APP_VERSION__

// Animation variants
export const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.6, ease: [0.4, 0, 0.2, 1] as [number, number, number, number] },
  }),
}

export const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
}

// Feature card tone class names
export const featureToneClassNames = [
  'feature-tone-primary',
  'feature-tone-cyan',
  'feature-tone-emerald',
  'feature-tone-amber',
] as const
