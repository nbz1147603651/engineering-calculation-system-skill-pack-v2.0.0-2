/* ============================================
   ECS Homepage - Main App Component
   ============================================ */

import ParticlesCanvas from '@/components/effects/ParticlesCanvas'
import Footer from '@/components/layout/Footer'
import Navbar from '@/components/layout/Navbar'
import Architecture from '@/components/sections/Architecture'
import Features from '@/components/sections/Features'
import Hero from '@/components/sections/Hero'
import Install from '@/components/sections/Install'
import Platforms from '@/components/sections/Platforms'
import StatsRow from '@/components/sections/StatsRow'
import ScrollToTop from '@/components/ui/ScrollToTop'
import { APP_VERSION } from '@/data/constants'
import { useLanguage } from '@/hooks/useLanguage'

export default function App() {
  const { language, setLanguage, t } = useLanguage()

  return (
    <div className="relative">
      <ParticlesCanvas />
      <Navbar language={language} t={t} onLanguageChange={setLanguage} />
      <main>
        <Hero t={t} />
        <StatsRow stats={t.stats} />
        <Features t={t} />
        <Architecture t={t} />
        <Platforms t={t} />
        <Install t={t} />
      </main>
      <Footer t={t} version={APP_VERSION} />
      <ScrollToTop label={t.scrollToTop} />
    </div>
  )
}
