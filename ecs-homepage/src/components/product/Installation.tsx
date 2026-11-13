import { GUI_INSTALLER_DOWNLOAD_PATH } from "@/data/constants";
import { platformDetails } from "./platformCatalog";
import Icon from "./Icon";
import type { ProductCopy, ProductLanguage } from "./content";

export default function Installation(props: {
  copy: ProductCopy;
  language: ProductLanguage;
  selected: string;
}) {
  return <PlatformInstallation key={props.selected} {...props} />;
}

function PlatformInstallation({
  copy,
  language,
  selected,
}: {
  copy: ProductCopy;
  language: ProductLanguage;
  selected: string;
}) {
  const platform = platformDetails(selected);
  return (
    <section className="install-section" id="install">
      <div className="container install-layout">
        <div className="install-intro">
          <img
            src="./nimo-mascot.png"
            width="76"
            height="106"
            alt="Nimo"
            loading="lazy"
          />
          <h2>{copy.installTitle}</h2>
          <p>{copy.installIntro}</p>
          <ol>
            {copy.steps.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ol>
        </div>
        <div className="install-panel">
          <h3>{copy.desktop}</h3>
          <p>{copy.installer}</p>
          <a
            className="button button-primary download-button"
            href={GUI_INSTALLER_DOWNLOAD_PATH}
          >
            <Icon name="download" />
            {copy.download}
          </a>
          <div className="setup-guide">
            <h4>
              {platform.name} · {copy.guide}
            </h4>
            <p>
              {language === "zh"
                ? `打开客户端，选择 ${platform.name}，按照提示完成接入，即可在熟悉的 Agent 中使用 Nimo 工程技能。`
                : `Open the client, select ${platform.name} and follow the setup steps. Then use Nimo engineering skills in your familiar agent.`}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
