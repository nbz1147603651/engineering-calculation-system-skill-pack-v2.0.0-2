/* ============================================
   ECS Homepage - Main App Component
   ============================================ */

import { useState } from "react";
import { APP_VERSION } from "@/data/constants";
import {
  ProductHeader,
  ProductHero,
  ProductFooter,
} from "@/components/product/ProductShell";
import Workflow from "@/components/product/Workflow";
import AgentPlatforms from "@/components/product/AgentPlatforms";
import Installation from "@/components/product/Installation";
import { useProductLanguage } from "@/components/product/content";

export default function App() {
  const { language, setLanguage, copy } = useProductLanguage();
  const [platform, setPlatform] = useState("dsh");

  return (
    <div className="nimo-product">
      <a href="#main" className="skip-link">
        {copy.skip}
      </a>
      <ProductHeader
        language={language}
        onLanguageChange={setLanguage}
        copy={copy}
      />
      <main id="main">
        <ProductHero copy={copy} />
        <Workflow copy={copy} language={language} />
        <AgentPlatforms
          copy={copy}
          language={language}
          selected={platform}
          onSelect={setPlatform}
        />
        <Installation copy={copy} language={language} selected={platform} />
      </main>
      <ProductFooter copy={copy} version={APP_VERSION} />
    </div>
  );
}
