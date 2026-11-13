# NIMO Engineering：架构与流程审视

本次以原有工程计算 skill 为计算方法与交付契约的来源，加入 NIMO 产品管理，重做官网和部署客户端。计算项目运行时与“安装 skill 的客户端”职责不同：客户端负责宿主发现、安装、验包和移除，发行包内嵌完整运行载荷，安装无需源码检出或外部 Python；无需为了显示安装状态再引入常驻 Web 服务、数据库或模型 SDK。

## 保留正确的边界

原架构最值得保留的部分是：权威来源和适用范围先于公式提取，公式与单位规则先于实现交接，`run_book(BookInput) -> BookResult` 是唯一计算入口。API、界面、报告和批处理读取同一结果；来源、单位、分支、黄金算例和公式追踪构成工程正确性的证据。不能用更漂亮的 UI 替代这些约束。

01–14 的内容基本合理，但把它当成每次任务都必须从头走完的向导，会导致不必要的资料检索、交接文件重写与界面重建。现在将其解释为有依赖的能力/验收阶段：首次建设走适用的完整流程，维护先确认既有基线，再按变更层和契约影响选择阶段。上游来源变化会使下游证据失效；仅调整布局且不改计算契约时，复用已验证的计算内核。

对用户显示五个工作流域：资料与依据、分析与交接、计算内核、报告与交互、验证与交付。具体阶段编号和审查记录仍可下钻。四张执行卡写入同一持久记录并更新，避免每条消息重复展示。机器路由只是建议，不自动授予 `production_allowed` 或宣称验证完成。

交付范围现在由用户请求的成品决定：模块、CLI、批计算选择 `core-only`，独立计算书/报告选择 `report-only`，界面原型选择 `prototype-web`，运营网站/在线计算系统选择 `web-complete`。前两种在范围内可以验收完成，同时不能宣称交付了网站；真正的 `web-complete` 仍须通过完整网站交付保证。显式范围记录在 handoff，校验器的路径、接口与运行验收也使用同一范围，避免只改说明而继续强制生成全套网站。

Marimo 现在是显式选择的审查适配器（`review_adapter: marimo`）；默认不安装或启动 notebook 服务。Web 交付仍保留独立 JSON 会话/决定日志，所有生产范围仍核验来源、单位、公式追踪、稳定结果路径、重复输入重跑和实际黄金算例数值比较。核心 JSON 输入映射移至 `src/pkg/interfaces/input_mapping.py`，网页只是兼容转发；核心/报告验收和黄金算例不再导入 `webapp`。Docker/Compose 与本地启动同样使用显式 review 开关，不需要维护另一套计算 fork。

## 轻量应用边界

```text
Qt 客户端 / JSON CLI
        ↓
installer_gui.service  应用服务：catalog / inspect / execute
        ↓
平台契约 + 工作流路由 + 部署策略
        ↓
内嵌预构建载荷 / 原生宿主管理器 / 可恢复文件安装
        ↓
canonical core + host overlay → 生成的发布载荷
```

`tools/nimo.py` 是无图形环境入口。它与客户端工作线程复用服务、契约、路由和错误语义，导入时不加载 Qt/Tk。服务按进程串行处理部署，避免现有发布路径的进程全局配置被不同调用交叉使用；Qt 仍在后台线程执行操作。发行客户端内嵌七种预构建平台载荷、核心、包装器和配置，安装时不依赖源码目录或外部 Python；当前不增加常驻服务的启动和维护成本。DSH 的 `file:` bundle 先放入 LOCALAPPDATA 的载荷摘要缓存，使宿主引用在 EXE 临时解压目录消失后仍然有效。

```powershell
python engineering-calculation-system/tools/nimo.py catalog
python engineering-calculation-system/tools/nimo.py inspect --agent deepseek-harness
python engineering-calculation-system/tools/nimo.py workflow --task-type change --changed-layer ui --baseline-verified --evidence-gate analysis_allowed --coding-gate production_allowed
```

最后一条得到 `12b, 13`，表示复用已验证基线后检查界面与验证层。`--baseline-verified` 必须对应实际保存的基线证据；CLI 不会把一个布尔参数伪装成工程验证。

## 吸收开源架构的方式

DeepSeek Harness 官方以 Cordis 服务和可组合插件组织能力；技能注册表区分发现摘要、完整正文和相对资源基址。NIMO 复用现有 DSH 原生 bundle、`ctx.skills` provider 和宿主 CLI，保留宿主的会话、审批、沙箱与配置生命周期，不维护另一套 Harness fork。官方参考：[架构](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)、[技能注册表](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)。

本仓库已有 Codex、ZCode 的 core + overlay 同步器，现将这个优点用于发布构建：三种 native plugin 在临时生成目录从 canonical core 重新分层组装，而不把已复制的旧 skill 快照当成计算方法真源。它避免版本号一致而内容漂移。DSH 原有未跟踪源目录保持原状，构建不会调用 `--force` 改写它。

DeepSeek Harness 在客户端选定 `<DSH_HOME>/profiles/<profile>`，调用原生 `dsh plugin ... add/remove` 管理 bundle；验包同时检查依赖、`dsh.profile.bundles`、载荷文件与配置合成命令。存在一个 `SKILL.md` 不再被当成“已原生安装”的充分证据。`DSH_HOME` 只传给子进程，不改当前进程的环境或手写用户 profile。

## 资源保护与冗余整理

旧项目适配器移除会递归删除 `.opencode`、`.agents` 等共享目录，并删除备份；这些目录可能有其他技能和业务文件。本版使用 `.engineering-calc/installs/<agent>.json` 精确记录文件和摘要，移除只处理本次安装拥有且未被修改的文件，恢复被替换的原文件，保留用户修改、借用的同内容文件、无关文件和备份。旧安装没有所有权清单时拒绝猜测删除范围。用户级目录安装移除保留可恢复的副本。

清理了部署器中已无调用的整目录项目安装/移除路径。历史发布包、Reference、原始工程资料、旧品牌图片与源插件快照均保留；它们不能仅凭“看起来重复”被删除。后续若压缩源码分发，应先明确 generated/source 边界、校验发布可再生性，再根据逐项清单处理。

## 验证边界

后端用临时目录覆盖精确文件安装/恢复、修改保留、路径越界拒绝、原生 DSH argv/环境/状态、工作流路由和静默子进程超时。DSH provider 使用其既有 Node 合同测试。原生打包验证在本机完成；未在本次验证中向真实用户 profile 安装、移除插件，也未使用真实模型密钥发起工程计算。
