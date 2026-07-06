# ECS Skill & Plugin 体系搭建完备性分析

## Context

ECS v2.6.0 是一个面向 AI Agent 的工程计算技能包，目标是让 AI 按照 14 步生命周期自主产出具备工业生产能力的工程计算书。本文从 **Agent Skill 定义 + 多平台 Plugin 适配 + 多 Agent 编排** 的角度，分析当前搭建是否完备。

---

## 一、Skill 定义层：18 个 Skill 文件

### 1.1 覆盖度

| Skill | 文件 | 职责 | 状态 |
|-------|------|------|------|
| 00 | `00-engineering-calculation-router.skill.md` (6.5KB) | 路由分类 + 任务分发 | ✅ 完备 |
| 01 | `01-reference-adequacy-and-gap-assessment.skill.md` (3.6KB) | 参考充分性评估 | ✅ 完备 |
| 02 | `02-reference-discovery-and-acquisition.skill.md` (3.9KB) | 参考发现与获取 | ✅ 完备 |
| 03 | `03-reference-persistence-and-local-library.skill.md` (3.2KB) | 本地证据库持久化 | ✅ 完备 |
| 04 | `04-source-intake-and-authority.skill.md` (2.5KB) | 来源摄入与权威性 | ✅ 完备 |
| 05 | `05-engineering-logic-blueprint.skill.md` (6.3KB) | 计算逻辑蓝图 | ✅ 完备 |
| 06 | `06-formula-lookup-branch-extraction.skill.md` (4.3KB) | 公式/查表/分支提取 | ✅ 完备 |
| 07 | `07-implementation-handoff-contract.skill.md` (5.2KB) | 实现交接合同 | ✅ 完备 |
| 08 | `08-calculation-book-architecture.skill.md` (2.9KB) | 架构设计 | ✅ 完备 |
| 09 | `09-core-and-data-models.skill.md` (2.5KB) | 核心与数据模型 | ✅ 完备 |
| 10 | `10-reusable-calculation-modules.skill.md` (3.8KB) | 可复用计算模块 | ✅ 完备 |
| 11 | `11-book-runner-and-governing-summary.skill.md` (4.6KB) | 计算书运行器 | ✅ 完备 |
| 12 | `12-report-review-batch-interfaces.skill.md` (4.2KB) | 接口路由 | ✅ 完备 |
| 12a | `12a-report-context-and-rendering.skill.md` (7.1KB) | 报告上下文与渲染 | ✅ 完备 |
| 12b | `12b-frontend-and-review-interfaces.skill.md` (10.5KB) | 前端与审查界面 | ✅ 完备 |
| 12c | `12c-batch-import-export-packages.skill.md` (3.4KB) | 批量/导入导出 | ✅ 完备 |
| 13 | `13-verification-regression-traceability.skill.md` (4.8KB) | 验证/回归/追溯 | ✅ 完备 |
| 14 | `14-cloud-web-release-deployment.skill.md` (5.7KB) | 发布部署 | ✅ 完备 |

**每个 Skill 均包含**：frontmatter（name + description）、When to use、Steps、Artifacts、Exit gate。

### 1.2 Skill 层评价

- ✅ **14 步全覆盖**，每步有明确的输入/输出/退出门控
- ✅ **渐进式加载**（progressive disclosure）：路由器 → 父编排器 → 子技能，避免一次性加载全部
- ✅ **3 个 Parent Orchestrator** 分阶段管理：01-03 / 04-07 / 08-14
- ⚠️ **Skill 文件体量偏轻**：多数 2.5-6KB，对 AI 的指引粒度偏"原则性"，缺少具体的代码示例/模式

---

## 二、Agent 定义层：1 Supervisor + 7 Workers

### 2.1 Supervisor（`engineering-calc-system.md`, 459 行 / ~27KB）

| 能力 | 状态 | 说明 |
|------|------|------|
| 路由决策 | ✅ | 内嵌完整路由表 + 资料状态分类 |
| 工具绑定 | ✅ | `tools: Read,Write,Edit,Grep,Glob,Bash,WebSearch,WebFetch` |
| 专家团映射 | ✅ | 调研员/全栈工程师/QA/代码审查员/UI操作者/故障诊断工程师 |
| Worker 委派表 | ✅ | 7 个 worker agent 的职责/路径/边界清晰 |
| 行为工程层 | ✅ | Route Card + Gate Card + Artifact Contract + Validation Evidence |
| 串行门控制 | ✅ | 明确列出 8 个不可并行的门控决策 |
| 安装形态感知 | ✅ | 区分 Qoder CLI/CN IDE/CN CLI/Cloud Agents 等形态 |
| 完成证据框架 | ✅ | 引用 `completion-evidence.md`，禁止从 UI/HTML 推断完成 |

### 2.2 Worker Agents

| Worker | 文件 | 覆盖阶段 | 工具 | 行数 |
|--------|------|----------|------|------|
| Reference Acquirer | `engineering-calc-reference-acquirer.md` | 01-03 | +WebSearch/WebFetch | 49 |
| Source Intake | `engineering-calc-source-intake.md` | 04 | +WebSearch/WebFetch | 45 |
| Logic Extractor | `engineering-calc-logic-extractor.md` | 05-07 | +WebSearch/WebFetch | 48 |
| Module Worker | `engineering-calc-module-worker.md` | 08-11 | 无 Web | 51 |
| Interface Worker | `engineering-calc-interface-worker.md` | 12/12a/12b/12c | 无 Web | 65 |
| Verification Worker | `engineering-calc-verification-worker.md` | 13 | 无 Web | 62 |
| Release Worker | `engineering-calc-release-worker.md` | 14 | 无 Web | 45 |

**每个 Worker 均包含**：
- ✅ `Use only when delegated by engineering-calc-system`（防止越权）
- ✅ `Owned outputs` 路径边界
- ✅ `Do` / `Do not` 行为约束
- ✅ `agent_result_packet.yaml` 返回规范
- ✅ 禁止自行做门控决策

### 2.3 Agent 层评价

- ✅ **职责划分清晰**：Supervisor 管门控/ID/交接冻结，Worker 管执行
- ✅ **路径隔离**：每个 Worker 有明确的 `owned_paths`，不得越界写入
- ✅ **串行门控制**：8 个关键决策只能 Supervisor 做
- ⚠️ **Worker 缺少步骤级指引**：Worker 知道"做什么"和"不做什么"，但具体怎么做需要自行读取对应的 child skill 文件——这增加了 Worker 的理解负担
- ⚠️ **Worker 之间无直接通信**：所有协调通过 Supervisor 中转，增加了 Supervisor 的上下文压力

---

## 三、Plugin 适配层：4 种平台

### 3.1 平台覆盖矩阵

| 平台 | 插件目录 | 形态 | 状态 |
|------|----------|------|------|
| **Qoder (主力)** | `adapter_sources/qoder/.qoder/` | Agent + Skill + Reference + Asset | ✅ 最完备 |
| **ZCode** | `plugins/engineering-calculation-system-zcode/` | Plugin (marketplace.json + skills/) | ✅ 完备 |
| **Codex** | `plugins/engineering-calculation-system/.codex-plugin/` | Plugin (plugin.json + skills/) | ✅ 完备 |
| **OpenCode** | `opencodeplugin/` | npm 包 (TypeScript) | ⚠️ 有代码但缺安装后 skill |
| **Light/通用** | `adapter_sources/light/` | AGENTS.md + .agents/ + .trae/ | ✅ 完备 |

### 3.2 Qoder 适配（主力平台）

```
.qoder/
├── agents/
│   ├── engineering-calc-system.md          (Supervisor, 459行)
│   ├── engineering-calc-reference-acquirer.md  (Worker 01-03)
│   ├── engineering-calc-source-intake.md       (Worker 04)
│   ├── engineering-calc-logic-extractor.md     (Worker 05-07)
│   ├── engineering-calc-module-worker.md       (Worker 08-11)
│   ├── engineering-calc-interface-worker.md    (Worker 12/12a/12b/12c)
│   ├── engineering-calc-verification-worker.md (Worker 13)
│   └── engineering-calc-release-worker.md      (Worker 14)
├── skills/engineering-calc-system/
│   ├── SKILL.md           (轻量入口, 539行)
│   ├── qoder_quickstart.md (快速启动)
│   ├── reference.md       (长参考, 28KB)
│   └── assets/
│       └── lifecycle-console.html (46KB 可视化控制台)
└── references/
    └── engineering-calc-system.md (29KB 参考文档)
```

- ✅ Supervisor + 7 Workers 全部就位
- ✅ Skill 入口 + 快速启动 + 长参考 + 可视化资产
- ✅ 区分"轻量入口"和"完整项目包"

### 3.3 ZCode 适配

```
plugins/engineering-calculation-system-zcode/
├── .zcode-plugin/         (插件元数据)
├── skills/
│   ├── engineering-calculation-system/
│   │   ├── SKILL.md       (核心技能 + ZCode 适配器)
│   │   ├── skills/        (18 个子技能)
│   │   ├── shared/        (19 个共享契约)
│   │   ├── templates/     (~100 个模板)
│   │   ├── schemas/       (验证规范)
│   │   └── project_template/ (项目脚手架)
│   └── engineering-calculation-verification/
│       └── SKILL.md       (验证子技能入口)
├── marketplace.json       (市场发布配置)
└── package.json
```

- ✅ 完整核心包嵌入插件
- ✅ 独立验证子技能
- ✅ marketplace.json 支持市场安装

### 3.4 OpenCode 适配

```
opencodeplugin/
├── src/
│   ├── domain.ts          (生命周期阶段定义, 523行)
│   ├── create-tools.ts    (工具创建, 10KB)
│   ├── create-hooks.ts    (钩子创建)
│   ├── gate-enforcer.ts   (门控执行器)
│   ├── gates.ts           (门控逻辑, 13KB)
│   ├── paths.ts           (路径管理)
│   ├── manifest.ts        (清单)
│   └── ...
├── templates/.opencode/   (项目模板)
├── package.json           (npm 包, @opencode-ai/plugin 依赖)
└── assets/engineering-calc-system.schema.json
```

- ✅ TypeScript 实现，有门控执行器 (`gate-enforcer.ts`)
- ✅ 有 schema 验证
- ⚠️ 没有像 Qoder/ZCode 那样的 Markdown skill 安装后文件——它通过代码 hook 而非 skill 文件工作

### 3.5 Light/通用适配

```
adapter_sources/light/
├── AGENTS.md              (通用 Agent 规则, 115行)
├── .agents/skills/engineering-calc-system/SKILL.md
├── .opencode/skills/engineering-calc-system/SKILL.md
├── .trae/rules/
│   ├── engineering-calc-system.md
│   └── project_rules.md
└── adapters/
    ├── agent-entrypoints.md  (366行, 多平台入口指引)
    └── mcp-recommendations.md
```

- ✅ 覆盖 Trae / OpenCode / 通用 AGENTS.md 兼容平台
- ✅ `agent-entrypoints.md` 提供详细的平台映射说明

---

## 四、共享契约与模板支撑

### 4.1 共享契约（19 个文件）

| 类别 | 文件 | 作用 |
|------|------|------|
| **核心生命周期** | `lifecycle.md` (11KB) | 14步门控矩阵 + 交付模式 + 不可协商规则 |
| **执行纪律** | `execution-discipline.md` | Route Card / Gate Card / Artifact Contract / Validation Evidence |
| **计划纪律** | `planning-discipline.md` | 多步计划的质量门 |
| **反馈纪律** | `review-feedback-discipline.md` | 反馈分类与路由 |
| **版本控制** | `version-control-discipline.md` | 工作区隔离与同步 |
| **完成证据** | `completion-evidence.md` | 声明→证据矩阵 |
| **调试纪律** | `systematic-debugging.md` | 根因链 + 最低正确层修复 |
| **多 Agent 编排** | `multi-agent-orchestration.md` (5.5KB) | Supervisor/Worker/Reviewer 角色 + 并行/串行规则 |
| **交接合同模板** | `handoff-contract-template.yaml` (7.4KB) | 12 个子合约 |
| **ID 约定** | `id-convention.md` | S01/F001/N001 等统一 ID |
| **单位约定** | `unit-convention.md` | 默认内部单位制 |
| **状态语义** | `status-semantics.md` | PASS/FAIL/WARNING 等 7 种状态 |
| **其他** | 7 个文件 | 文件命名、结果路径、版权、制品索引、交付合同、质量门、生命周期矩阵 |

### 4.2 模板（~100 个文件，7 个子目录）

| 目录 | 文件数 | 关键模板 |
|------|--------|----------|
| `acquisition/` | 13 | 搜索日志、候选来源、覆盖矩阵、来源卡片 |
| `analysis/` | 29 | 蓝图、概念图、方法选择矩阵、输入语义账本、计算节点、公式/查表/分支清单 |
| `handoff/` | 5 | implementation_handoff.yaml/md、coding_go_no_go.md |
| `implementation/` | 41 | 架构、模型、模块、运行器、UI 设计系统、报告规范、i18n、图表、Marimo |
| `verification/` | 6 | 测试矩阵、黄金案例、容差策略、验收清单 |
| `deployment/` | 3 | 云部署指南、发布清单 |
| `orchestration/` | 6 | 并行工作计划、任务简报、结果包、合并审查 |

### 4.3 Schema 验证

`artifact_contracts.json` (43.5KB) 定义了：
- 110+ 技能包必需路径
- 22 个技能文件清单
- 30+ CSV 列头精确定义
- 8 种 YAML 必需键
- 40+ 文件必须包含的关键短语
- 110+ 项目必需路径

---

## 五、构建与分发

`tools/build_release.py` (2545 行) 是完整的构建系统：

- ✅ 从 `core/` 源 + `adapter_sources/` 构建多个分发档案
- ✅ 支持 Qoder Project 包、Qoder Skill 包、ZCode 插件、Light 适配器等
- ✅ 版本同步（`versioning.py`）+ frontmatter 版本校验
- ✅ 哈希校验 + 文件树生成

---

## 六、发现的问题与缺口

### 问题 1：Qoder Skill 入口（SKILL.md）职责过载

`SKILL.md`（539 行）同时承担：
- 安装形态说明（Qoder CLI/CN IDE/CN CLI/Cloud）
- 行为工程层（Route Card/Gate Card 等）
- Marimo 审查闭合规则
- 静态报告分流逻辑
- A4 HTML 优先规则
- 完整生命周期总览（含 Mermaid 图）
- 路由决策表
- 启动条件表
- 核心原则
- LaTeX 导出逻辑

**风险**：AI 加载这一个文件就消耗大量上下文窗口，后续 14 步执行时可用的上下文空间被压缩。

### 问题 2：Supervisor Agent 与 Skill 入口内容大量重复

`engineering-calc-system.md`（459 行）与 `SKILL.md`（539 行）有约 60% 内容重复（架构说明、行为工程层、生命周期、路由等）。两者同时安装时会浪费上下文。

### 问题 3：Worker Agent 缺少步骤级执行指引

每个 Worker（45-65 行）只定义了：
- 边界（owned_paths）
- Do / Do not
- 返回规范

但**没有**包含对应 child skill 的关键步骤摘要。Worker 需要自行读取 2-6KB 的 child skill 文件才能知道"怎么做"。这增加了一层间接性，Worker 可能因为上下文限制而跳过关键步骤。

### 问题 4：模板文件内容为空壳

多数模板 CSV 只有列头没有示例数据（如 `formula_inventory.csv` 只有 `formula_id,name,...`），YAML 模板只有骨架键。AI 需要从零填充，缺少"参考样例"来理解期望的粒度和格式。

### 问题 5：reference.md（28KB）+ references/（29KB）双重长文档

Qoder 适配有两个大参考文件：
- `.qoder/skills/engineering-calc-system/reference.md` (28KB)
- `.qoder/references/engineering-calc-system.md` (29KB)

加上 Supervisor（27KB）+ Skill 入口（539行），AI 在任务开始时就面临 ~60KB 的基础上下文消耗。

### 问题 6：OpenCode 插件与其他平台形态差异大

OpenCode 插件是 TypeScript npm 包，通过代码 hook 工作，没有 Markdown skill 文件。这意味着：
- 同一套生命周期逻辑在 OpenCode 上由代码执行，在 Qoder/ZCode 上由 AI 读 Markdown 执行
- 行为一致性难以保证

### 问题 7：轻量入口 → 完整包的升级路径不自动化

Skill 入口明确说"这只是轻量入口，不能独立产出 production 级交付"，但从轻量入口升级到完整项目包需要用户手动下载/安装对应平台的 Project 包。AI 无法自动完成这个升级。

### 问题 8：`validate_artifacts.py` 的可达性

验证脚本在 `core/` 包中，但轻量 Skill 入口不包含它。当 AI 通过轻量入口开始工作时，它无法运行验证——直到用户安装完整包。

---

## 七、评估总结

| 维度 | 评分 | 说明 |
|------|------|------|
| **Skill 定义完备性** | ★★★★☆ | 18 个 skill 全覆盖，每步有输入/输出/门控，但粒度偏原则性 |
| **Agent 架构完备性** | ★★★★☆ | 1 Supervisor + 7 Workers 职责清晰，但 Worker 缺步骤级指引 |
| **多平台 Plugin 覆盖** | ★★★★☆ | Qoder/ZCode/Codex/Light 完备，OpenCode 形态差异大 |
| **共享契约体系** | ★★★★★ | 19 个契约文件 + 43.5KB schema，极其完备 |
| **模板支撑** | ★★★☆☆ | ~100 个模板覆盖全流程，但多数为空壳缺示例 |
| **构建与分发** | ★★★★★ | 2545 行构建脚本，多平台档案自动生成 |
| **上下文效率** | ★★☆☆☆ | Supervisor + Skill + Reference 合计 ~60KB 基础消耗，Worker 需额外加载 |
| **端到端自主执行可行性** | ★★★☆☆ | 流程完整但 AI 需同时维护 100+ 制品一致性，上下文压力大 |

### 最终判断

**Skill + Plugin 体系的"搭建完备性"很高**——18 个 skill、8 个 agent、4 个平台插件、19 个共享契约、100 个模板、2545 行构建脚本，从规范角度几乎无可挑剔。

**但从"AI 自主执行"的角度存在效率瓶颈**：
1. 基础上下文消耗过大（~60KB），压缩了实际工作空间
2. Worker 需要二次加载 child skill 才能执行，增加了跳步风险
3. 模板空壳意味着 AI 每次都要从零推断期望格式
4. 轻量入口到完整包的升级不是自动的

**结论**：体系搭建已接近完备，但要让 AI 真正"自主"产出工业生产级计算书，还需要在**上下文效率优化**（精简重复内容）、**Worker 执行指引增强**（内联关键步骤）、**模板示例填充**（至少为高频步骤提供样例）三个方向做针对性改进。
