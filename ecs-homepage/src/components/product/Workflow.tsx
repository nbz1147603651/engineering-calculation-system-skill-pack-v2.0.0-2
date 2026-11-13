import { useState } from "react";
import type { ProductCopy, ProductLanguage } from "./content";

export default function Workflow({
  copy,
  language,
}: {
  copy: ProductCopy;
  language: ProductLanguage;
}) {
  const [route, setRoute] = useState(0);
  const stageIndices =
    route === 2 ? [0] : route === 1 ? [1, 2, 3] : [0, 1, 2, 3];
  return (
    <section className="container workflow-section" id="workflow">
      <div className="workflow-copy">
        <h2>
          {copy.workflow[0]}
          <br />
          <span>{copy.workflow[1]}</span>
        </h2>
        <p>{copy.workflowIntro}</p>
        <div
          className="route-tabs"
          role="tablist"
          aria-label={language === "zh" ? "任务路径" : "Task path"}
        >
          {copy.routes.map((label, index) => (
            <button
              key={label}
              id={`route-tab-${index}`}
              role="tab"
              aria-selected={route === index}
              aria-controls="route-panel"
              onClick={() => setRoute(index)}
              onKeyDown={(event) => {
                if (
                  ["ArrowRight", "ArrowLeft", "Home", "End"].includes(event.key)
                ) {
                  event.preventDefault();
                  const next =
                    event.key === "Home"
                      ? 0
                      : event.key === "End"
                        ? 2
                        : (route + (event.key === "ArrowRight" ? 1 : 2)) % 3;
                  setRoute(next);
                  document.getElementById(`route-tab-${next}`)?.focus();
                }
              }}
              tabIndex={route === index ? 0 : -1}
            >
              {label}
            </button>
          ))}
        </div>
      </div>
      <div
        className="workflow-panel"
        role="tabpanel"
        id="route-panel"
        aria-labelledby={`route-tab-${route}`}
        tabIndex={0}
      >
        <ol>
          {stageIndices.map((index) => (
            <li key={index}>
              <span className="timeline-dot" />
              <span className="stage-number">0{index + 1}</span>
              <h3>{copy.stages[index][0]}</h3>
              <p>{copy.stages[index][1]}</p>
            </li>
          ))}
        </ol>
        <p className="route-note" aria-live="polite">
          {copy.routeNotes[route]}
        </p>
      </div>
    </section>
  );
}
