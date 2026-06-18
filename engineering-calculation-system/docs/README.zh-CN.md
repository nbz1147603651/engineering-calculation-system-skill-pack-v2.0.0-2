# 工程计算系统技能包 v2.4.0

本技能包把工程计算软件开发组织成完整交付生命周期：

```text
资料获取与本地证据库
-> 资料分析与计算逻辑蓝图
-> 编程实现、报告、批量计算、验证、追溯、发布与 Linux 云部署
```

实现阶段默认采用可审查、可复用、可部署的工程计算系统，而不是一次性页面或脚本。

## 默认技术栈

本技能包默认采用 Python-first 技术栈：

```text
主运行时: Python 3.9+
计算模块: src/<pkg>/libraries/ 下的 Python package
官方计算入口: run_book(BookInput) -> BookResult
后端/API: Flask 或 FastAPI 的薄路由层
前端格式: webapp/ 下的浏览器网页应用
默认网页文件: Jinja2 模板 + Bootstrap 5 + vanilla JavaScript modules
审查/后台: 需要 Python 原生模块审查或公式发布时使用 Marimo
```

如果用户明确要求非 Python 计算核心，handoff 必须补充适配方案。Marimo 是 Python 原生工具，不能直接深入审查非 Python 模块，除非提供 Python wrapper、CLI 或 API adapter。

## 质量优先原则

不要为了轻量而轻量。优先保证工程师和审查人的操作质量、便捷性、可追溯性和发布可靠性。

默认技术栈保持简单，是为了降低维护成本；但如果输入校验、导入导出、报告预览、图表、i18n、公式/来源追踪、Marimo 审查后台能显著提升工程质量，就应纳入交付范围，而不是为了少依赖而删除。

v2.4 新增可选多 Agent 编排能力。只有当用户明确要求多 Agent、子代理、委派或并行工作时，才读取 `shared/multi-agent-orchestration.md` 并使用 `templates/orchestration/`。supervisor 保留路由、来源权威、ID 分配、handoff 冻结、`run_book()` 公共合同和最终门禁判断；worker 只处理边界清晰、路径互不重叠的任务。

## 核心原则

```text
正确性和可追溯性优先
计算模块复用性其次
前端、报告和展示层最后
```

正式计算必须流经：

```python
run_book(BookInput) -> BookResult
```

公式、查表、分支判断、荷载组合和独立通过/失败逻辑不得放在：

```text
UI / 前端 JavaScript
HTML 模板
报告模板
批处理脚本
CSV / Excel 输入文件
仅用于展示的代码
```

## 交付边界

最终 Web 工程计算系统不能只交付一个 `.html` 文件、导出的 HTML 报告或静态界面 mockup。

除非用户明确只要静态原型，否则生产交付必须包含：

```text
可复用计算模块
官方 book runner
后端应用入口 create_app()
薄 API 路由
前端模板和静态资源
表单到 BookInput 的映射
BookResult 到 UI 的映射
单元、集成和 smoke 测试
本地运行命令
Linux / 云部署路径
release checklist
```

HTML 报告属于输出产物，不等同于应用本身。

## 主流程

```text
00 router
01 reference adequacy and gap assessment
02 reference discovery and acquisition
03 reference persistence and local library
04 source intake and authority
05 engineering logic blueprint
06 formula lookup branch extraction
07 implementation handoff contract
08 calculation book architecture
09 core and data models
10 reusable calculation modules
11 book runner and governing summary
12 report review batch interface router
12a report context and rendering
12b frontend and review interfaces
12c batch import/export packages
13 verification regression traceability
14 cloud web release deployment
```

## v2.2.0 接口层拆分

```text
12  接口路由：报告、前端、审查、批量和发布范围判断
12a 报告上下文、渲染、报告状态和模板边界
12b 生产前端、API、表单映射、i18n、图表、数值清洗和 Marimo 审查
12c 数据区、上传包、导入导出、哈希、清单和批量运行
14  本地可运行 Web 客户端、Linux 云部署和发布 smoke test
```

## 关键 handoff 产物

```text
references/acquisition/acquisition_handoff.yaml
references/source_registry.yaml
analysis/02_logic_blueprint/calculation_blueprint.md
analysis/03_logic_details/formula_inventory.csv
analysis/03_logic_details/lookup_inventory.csv
analysis/03_logic_details/branch_inventory.csv
handoff/implementation_handoff.yaml
handoff/artifact_index.yaml
handoff/coding_go_no_go.md
implementation/02_modules/module_asset_registry.csv
verification/acceptance_checklist.md
release/release_checklist.md
```

`implementation_handoff.yaml` 现在应明确区分：

```text
calculation_module_contract
book_runner_contract
backend_api_contract
frontend_contract
release_contract
```

这样下游实现者能知道哪些内容属于计算核心，哪些属于后端 API，哪些属于前端界面，哪些属于最终发布。

## 入口文件

Codex 兼容环境优先从根目录加载：

```text
dist/core/engineering-calculation-system/SKILL.md
```

默认安装 `dist/core/engineering-calculation-system/`。MiniMax Code 标准技能导入或自动发现时使用 `dist/release/engineering-calculation-system-MiniMaxCode-v2.4.0.zip`。QODER 直接上传 Skill 时使用 `dist/release/engineering-calculation-system-QODER-v2.4.0.zip`；需要复制到 QODER 项目根时使用 `dist/release/engineering-calculation-system-QODER-Project-v2.4.0.zip`。Qoder 原始入口位于 `dist/qoder-addon/`，OpenCode、AGENTS.md 和 TRAE 兼容入口位于 `dist/adapters-light/`。

各 Agent 的加载方式可参考：

```text
dist/adapters-light/adapters/agent-entrypoints.md
```

可选 MCP 建议位于：

```text
dist/adapters-light/adapters/mcp-recommendations.md
```

MCP 只作为加速器，不作为正确性依赖。建议只按任务启用搜索/抓取、文档查询、公共代码搜索、诊断/LSP、授权文档提取、浏览器测试等 MCP；不要默认启用带密钥、外部系统或可能绕过访问控制的 MCP。

可选多 Agent 编排说明位于：

```text
dist/core/engineering-calculation-system/shared/multi-agent-orchestration.md
dist/core/engineering-calculation-system/templates/orchestration/
```

如果目标环境不适合加载多个文件，可使用：

```text
dist/singlefile/engineering-calculation-system.all-in-one.md
```

## 版权和访问规则

不要绕过付费墙、登录限制、许可限制或访问控制。只有在用户提供、明确授权，或公开可下载且允许合理使用时，才保存完整原始资料。

对于受版权保护的规范、标准、手册、论文和教材，优先保存来源卡片、引用信息、条款号、页码、短摘录和改写摘要，而不是保存大段原文。

## 校验

校验技能包：

```bash
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core
```

校验内置工程模板：

```bash
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core --project dist/core/engineering-calculation-system/project_template/engineering_calc_project
```

运行模板测试：

```bash
cd dist/core/engineering-calculation-system/project_template/engineering_calc_project
python -m pytest -q
```

## 版本

```text
version: 2.4.0
created_at: 2026-06-17
status: complete_packaged_release
```
