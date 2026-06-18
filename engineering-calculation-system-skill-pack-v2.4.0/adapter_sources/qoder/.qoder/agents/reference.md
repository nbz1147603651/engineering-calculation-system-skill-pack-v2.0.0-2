# 工程计算系统 — 详细参考

本文件包含各技能的完整字段定义、产物清单和执行细节。主文件路由后按需读取对应章节。

---

## 完整交付契约

实现前必须声明交付模式：`core-only` / `report-only` / `prototype-web` / `web-complete`。

默认使用 `web-complete`，除非用户明确要求轻量原型或仅计算核心。`web-complete` 必须包含计算核心、`run_book(BookInput) -> BookResult`、Web/API、交互前端（含中英文切换：`/api/i18n/<lang>`、`data-i18n`、持久化语言偏好）、报告预览或下载、JSON 导入导出、批量接口、部署文件、smoke tests、release checklist 和项目校验记录。

生产 UI 必须使用统一 UI Kit：`templates/implementation/ui_design_system.md`、`webapp/templates/partials/_topbar.html`、`webapp/templates/partials/_report_modal.html`、`webapp/static/css/tokens.css`、`webapp/static/css/components.css`。计算书最终导出应通过 `GET /api/report/decision` 自动选择：有本地 `latexmk` 或 `pdflatex` 时走 LaTeX/PDF 且必须编译生成 `main.pdf`，否则走包含 `@page size: A4` 和公式逻辑追溯的 HTML 计算书。计算书导出也应支持 LaTeX/Overleaf 兼容 zip；初始化或首次导出时询问用户是否有指定模板，用户不提供则使用 `latex/templates/default_engineering_calcbook/`。生成项目必须提供 `GET /api/report/templates`、稳定的 `latex_template_id` 选择控件、`POST /api/report/final`，以及 `POST /api/report/latex` 的默认回退逻辑。

默认完整路径：

```text
08 → 09 → 10 → 11 → 12a → 12b → 12c → 13 → 14
```

不得把 `run_book.py`、静态 HTML、报告 HTML、notebook demo 或界面 mockup 标记为完成、可部署或 `web-complete`。如果当前安装只有 Qoder direct skill 的 3 个文件，它只是轻量入口；完整生成应使用 QODER Project 包或完整 single-file fallback。

---

## 技能01：参考充分性评估

### 充分性评估维度（16项）

工程领域与计算对象、管控规范/标准/手册、辖区和版本/年份、项目特定设计基础、荷载工况与组合、几何定义、材料/土/水力/结构参数、公式来源、查找表/图/插值规则、分支与适用性规则、单位和符号约定、安全系数/分项系数/抗力系数、算例或回归参考、报告要求、审查/批准要求。

### 覆盖矩阵结构

| Requirement ID | Requirement | Importance | Covered? | Current Source ID | Gap | Needed Source Type | Blocks Analysis? | Blocks Coding? |
|---|---|---|---|---|---|---|---|---|

Importance: `critical` / `high` / `medium` / `low`
Coverage: `covered` / `partially_covered` / `not_covered` / `conflicting` / `unknown`

### 获取计划字段

`gap_id`, `needed_information`, `why_it_matters`, `preferred_source_type`, `authority_priority`, `target_jurisdiction_or_standard`, `search_keywords`, `candidate_domains_or_publishers`, `minimum_acceptance_criteria`, `fallback_if_not_found`

### 产物

- `references/acquisition/reference_gap_assessment.md`
- `references/acquisition/source_coverage_matrix.csv`
- `references/acquisition/acquisition_plan.yaml`
- `references/acquisition/open_reference_questions.md`

---

## 技能02：参考发现与获取

### 源优先级（10级）

1. 项目合同要求和设计基础
2. 管控规范、标准、国家附件、客户标准
3. 官方规范注释或权威机构设计手册
4. 部委/机构/研究院/标准组织的官方技术指南
5. 已批准的历史计算书或已验证传统Excel
6. 可靠技术来源的已发布算例
7. 教科书、同行评审论文、大学笔记、制造商技术手册
8. 独立手算
9. 内部设计笔记
10. 未验证网页/论坛/AI摘要/未知来源

### 搜索策略字段

每个缺口定义：`search_objective`, `required_facts_or_tables`, `jurisdiction_and_language`, `preferred_publisher_or_authority`, `essential_keywords`, `alternative_keywords`, `source_acceptance_criteria`, `rejection_criteria`

### 搜索查询模板

```
<engineering object> <check> design manual pdf official
<standard/code name> <clause/table/equation> <topic>
<agency/ministry> <topic> design guide
<calculation type> worked example <code/version>
```

### 迭代搜索

找到候选源后，按其标题/出版商/条款标识符/版本再次搜索，寻找更好的一手来源或算例。

### 筛选标准字段（14项）

`candidate_id`, `title`, `publisher`, `source_type`, `url_or_location`, `access_date`, `version_or_date`, `jurisdiction`, `relevance_score`, `authority_level`, `coverage_tags`, `gaps_covered`, `limitations`, `license_or_access_notes`, `recommended_action`

### 推荐操作

`persist_raw` / `persist_source_card_only` / `use_for_background_only` / `reject` / `needs_user_access` / `needs_purchase_or_license` / `needs_confirmation`

### 搜索日志列

`search_id, gap_id, query, tool_or_location, date, results_reviewed, candidates_selected, notes`

### 检索决策列

`decision_id, candidate_id, decision, reason, local_target, raw_allowed, source_card_required, extraction_required, follow_up`

### 产物

- `references/acquisition/search_log.csv`
- `references/acquisition/candidate_sources.csv`
- `references/acquisition/retrieval_decisions.csv`
- `references/acquisition/source_coverage_matrix.csv`
- `references/acquisition/acquisition_notes.md`

### 互联网搜索要求

有搜索工具时：每个关键/高缺口多查询 → 优先官方域 → 打开检查一手来源 → 交叉检查版本/辖区/出版商 → 记录搜索日志 → 记录接受和拒绝的候选源 → 工具不可用时明确声明

### 主动补充搜索（即使有资料也应执行）

**为什么**：单一来源容易遗漏关键计算步骤、公式系数、适用条件或最新修订。

**何时触发**：
- 用户提供了资料但未经官方验证
- 资料年代较早（可能已有修订或勘误）
- 仅有一种来源（缺乏交叉验证）
- 涉及安全关键计算（承载力、抗震等）
- 公式来源不明确或为二手引用

**搜索目标**：
1. **验证公式完整性**：搜索原始规范确认公式未被截断或误引
2. **查找官方勘误**：搜索 `<规范名称> errata` 或 `<规范名称> 勘误`
3. **补充算例对比**：搜索 `<计算类型> worked example` 验证理解
4. **确认单位约定**：搜索规范原文确认内部单位系统
5. **获取更权威来源**：如当前来源为教科书，搜索其引用的原始规范
6. **检查最新修订**：搜索 `<规范名称> <年份> amendment` 确认版本

**搜索查询示例**：
```
<code name> <year> amendment corrigenda
<code name> <clause number> official commentary
<calculation type> design example <code name>
<standard name> errata sheet
```

**记录要求**：主动搜索结果同样记录到 `search_log.csv`，在 `gap_id` 字段标注 `VALIDATION-001` 等标识。

---

## 技能03：参考持久化与本地库

### 目录结构

```
references/
  acquisition/
    reference_gap_assessment.md, acquisition_plan.yaml, search_log.csv,
    candidate_sources.csv, retrieval_decisions.csv, source_coverage_matrix.csv,
    acquisition_notes.md, acquisition_handoff.yaml
  raw/
    S01_<short_source_name>.pdf, S02_<short_source_name>.xlsx
  extracted/
    S01_text.md, S01_tables/, S02_workbook_formula_map.md
    notes/S01_source_notes.md
  source_cards/
    S01_source_card.md, S02_source_card.md
  snapshots/
    README.md
  source_registry.yaml
  evidence_library_manifest.yaml
```

### 源ID分配

`S01, S02...` / `CODE-01` / `MANUAL-01` / `EXAMPLE-01` / `EXCEL-01` / `REPORT-01`

下游分析开始后不得更改已有ID。

### 原始文件保存规则

仅当：用户上传 / 明确授权 / 可公开下载且允许 / 公共领域或宽松许可。否则仅创建源卡片。

### 源卡片必填字段（19项）

`source_id`, `title`, `publisher_or_author`, `source_type`, `version_or_date`, `jurisdiction`, `url_or_location`, `access_date`, `raw_file_path`, `extracted_file_path`, `authority_level`, `coverage_tags`, `relevance_to_calculation`, `key_clauses_tables_equations_pages`, `short_excerpts`, `paraphrased_notes`, `limitations`, `license_or_access_notes`, `recommended_downstream_use`

### 提取规则

记录：提取日期、提取工具/方法、页/表/范围引用、不确定性和OCR风险。保留表标识符。避免长版权段落。优先结构化摘要和标识符。

电子表格额外记录：工作簿名、表名、命名范围、可见/隐藏表、公式映射、输入/输出/重要中间单元格、外部链接/宏。

### 哈希与清单

每个本地文件记录：`path`, `sha256`, `created_at`, `source_id`, `file_role`, `notes`

### 获取交接文件字段

`project_or_calculation_name`, `acquisition_status`, `source_ids`, `coverage_summary`, `remaining_gaps`, `recommended_analysis_path`, `sources_to_use_as_governing`, `sources_to_use_as_examples`, `sources_to_use_as_background`, `copyright_or_access_limitations`

### 产物

- `references/source_registry.yaml`
- `references/evidence_library_manifest.yaml`
- `references/acquisition/acquisition_handoff.yaml`
- `references/source_cards/*.md`
- `references/raw/*`（允许时）
- `references/extracted/*`（适当时）

---

## 技能04：源摄入与权威

### 输入

优先读取：`source_registry.yaml`, `evidence_library_manifest.yaml`, `acquisition_handoff.yaml`, `references/raw/`, `references/extracted/`, `references/source_cards/`

无证据库时直接使用上传材料并创建等效源清单。

### 源清单字段（12项）

`source_id`, `source_name`, `source_type`, `version_or_date`, `jurisdiction_or_project`, `role_in_analysis`, `priority`, `authority_level`, `reliability_notes`, `scope_of_applicability`, `known_limitations`, `local_path_or_source_card`

### 权威层级（10级）

1. 项目合同要求
2. 管控设计规范/标准
3. 官方规范注释/国家认可设计手册
4. 项目批准的计算基础
5. 可靠来源的已发布算例
6. 已验证历史计算报告
7. 传统电子表格
8. 内部设计笔记
9. 工程假设
10. 未知来源或未验证材料

### 冲突清单字段

`conflict_id`, `affected_formula_coefficient_branch_or_assumption`, `source_A_method`, `source_B_method`, `engineering_consequence`, `recommended_resolution`, `blocks_analysis_or_coding`

### 质量门控

通过前验证：来源已识别、ID稳定、版本/辖区已捕获、权威排序明确、项目来源与通用来源区分、源卡片/本地路径可用、冲突和缺口可见。

### 产物

- `analysis/01_source_inventory/source_inventory.yaml`
- `analysis/01_source_inventory/source_authority_table.csv`
- `analysis/01_source_inventory/source_conflicts.csv`
- `analysis/01_source_inventory/source_intake_notes.md`

---

## 技能05：工程逻辑蓝图

### 核心原则

Mermaid图是视图，不是产品。核心交付物是 `calculation_blueprint.md`。

### 概念层提取

提取概念：计算对象、设计状况、极限状态、荷载工况、荷载组合、材料模型、土模型、水/环境条件、几何模型、边界条件、设计方法、检查方法、安全格式、失效模式、适用性准则、极限准则、特殊条件、管控结果、报告输出。

### 规范化节点模型字段（17项）

`node_id`, `node_type`, `node_name`, `engineering_meaning`, `inputs`, `outputs`, `units`, `formula_or_method`, `source_reference`, `branch_condition`, `applicability`, `assumptions`, `module_candidate`, `result_visibility`, `report_visibility`, `test_requirement`, `risk_level`

### 节点类型（14种）

`Input`, `Validate`, `Normalize`, `SelectMethod`, `Lookup`, `Compute`, `Branch`, `Check`, `Aggregate`, `Output`, `Report`, `Warning`, `Error`, `Redesign`

### 软件映射

每个重要节点映射到至少一个：输入模型字段、验证器、规范化器、查找库、计算模块函数、运行器步骤、CheckResult、GoverningSummary、BookResult字段、ReportContext字段、测试目标。

### 产物

- `analysis/02_logic_blueprint/calculation_blueprint.md`
- `analysis/02_logic_blueprint/concept_map.csv`
- `analysis/02_logic_blueprint/calculation_nodes.csv`
- `analysis/02_logic_blueprint/input_inventory.csv`
- `analysis/02_logic_blueprint/intermediate_inventory.csv`
- `analysis/02_logic_blueprint/output_inventory.csv`
- `analysis/04_diagrams/global_flowchart.mmd`
- `analysis/04_diagrams/data_flow.mmd`（按需）
- `analysis/04_diagrams/branch_logic.mmd`（按需）
- `analysis/04_diagrams/module_dependency.mmd`（按需）

---

## 技能06：公式/查找/分支提取

### 提取目标

公式和方法、系数和因子、查找表和图、插值和超范围规则、分支条件和方法选择规则、适用性限制、单位和符号约定、安全格式、状态规则、警告和错误、假设和工程判断。

### 公式清单字段（13项）

`formula_id`, `name`, `purpose`, `inputs`, `outputs`, `units`, `source_reference`, `applicability`, `branch_dependencies`, `lookup_dependencies`, `implementation_note`, `test_requirement`, `risk_level`

公式来源分类：`code-defined` / `manual-defined` / `spreadsheet-derived` / `empirical` / `project-specific` / `engineering_assumption` / `needs_confirmation`

### 查找清单字段（10项）

`lookup_id`, `name`, `inputs`, `outputs`, `source_reference`, `interpolation_rule`, `out_of_range_behavior`, `implementation_note`, `test_requirement`, `risk_level`

查找行为：`exact_lookup` / `range_lookup` / `linear_interpolation` / `bilinear_interpolation` / `log_interpolation` / `nearest_conservative_value` / `chart_digitization` / `manual_selection` / `needs_confirmation`

### 分支清单字段（9项）

`branch_id`, `condition`, `engineering_meaning`, `source_reference`, `path_if_true`, `path_if_false`, `not_applicable_behavior`, `program_representation`, `required_tests`, `risk_level`

### 单位和符号规则

记录：输入单位、内部单位、输出单位、角度单位、力/弯矩符号约定、坐标方向、压力/应力约定、沉降/位移符号约定。不清晰项标记 `needs_confirmation`。

### 联网验证（建议执行）

**为什么**：提取的公式可能不完整、系数可能有误、适用条件可能被忽略。

**验证清单**：
1. **公式来源确认**：搜索公式ID对应的规范原文，确认公式未被截断
2. **系数交叉验证**：搜索同一公式的其他来源，对比系数值
3. **适用条件核实**：搜索规范注释，确认公式的适用范围
4. **算例对比**：搜索官方算例或权威手册算例，验证公式理解
5. **勘误检查**：搜索 `<规范名> errata` 确认无已知错误

**搜索查询示例**：
```
<formula name> <code name> clause <number>
<coefficient name> <code name> table <number>
<calculation type> design example verification
```

**记录要求**：验证结果记录到 `search_log.csv`，`gap_id` 标注 `FORMULA-VERIFY-001` 等。发现的差异记录到 `risk_register.csv`。

### 产物

- `analysis/03_logic_details/formula_inventory.csv`
- `analysis/03_logic_details/lookup_inventory.csv`
- `analysis/03_logic_details/branch_inventory.csv`
- `analysis/03_logic_details/applicability_limits.csv`
- `analysis/03_logic_details/unit_and_sign_conventions.md`
- `analysis/03_logic_details/assumption_register.csv`
- `analysis/05_risks_and_questions/risk_register.csv`
- `analysis/05_risks_and_questions/open_questions.csv`

---

## 技能07：实施交接契约

### 交接契约YAML字段

`handoff_id`, `book_name`, `version`, `status`, `source_basis`, `evidence_library_status`, `calculation_scope`, `input_model_groups`, `result_model_groups`, `runner_sequence`, `module_candidates`, `formula_inventory_refs`, `lookup_inventory_refs`, `branch_inventory_refs`, `validation_rules`, `test_requirements`, `report_sections`, `traceability_requirements`, `open_questions`, `coding_gate`

### 所需输入

- `references/acquisition/acquisition_handoff.yaml`
- `analysis/01_source_inventory/source_inventory.yaml`
- `analysis/02_logic_blueprint/calculation_blueprint.md` + `calculation_nodes.csv`
- `analysis/03_logic_details/formula_inventory.csv` + `lookup_inventory.csv` + `branch_inventory.csv` + `applicability_limits.csv` + `unit_and_sign_conventions.md`
- `analysis/05_risks_and_questions/risk_register.csv` + `open_questions.csv`

### 产物

- `handoff/implementation_handoff.yaml`
- `handoff/implementation_handoff.md`
- `handoff/artifact_index.yaml`
- `handoff/coding_go_no_go.md`
- `handoff/unresolved_items_before_coding.md`

---

## 技能08：计算书架构

### 功能分类层级（8层）

`core platform` / `reusable engineering library` / `calculation book runner` / `report context/renderer` / `review/frontend` / `batch/CLI/API` / `verification` / `release/deployment`

### 功能分类表

| Feature | Layer | Existing module? | New module needed? | Reusable? | Location | Notes |
|---|---|---|---|---|---|---|

### 产物

- `implementation/00_architecture/project_structure.md`
- `implementation/00_architecture/feature_classification.csv`
- `implementation/00_architecture/dependency_rules.md`
- `implementation/00_architecture/package_layout.md`

---

## 技能09：核心与数据模型

### 核心平台职责（10项）

status enums, CheckResult, FormulaTrace, RunMetadata, errors and warnings, validators, unit helpers, hashing, serialization, result path utilities

### 核心禁止

domain formulas, book-specific runner logic, UI code, report rendering, batch workflow

### 公共数据模型

`ProjectInfo`, `DesignBasis`, `DesignOptions`, `Assumption`, `BookInput`, `BookResult`, `ModuleInput`, `ModuleResult`, `CheckResult`, `GoverningSummary`, `ReportContext`

### 公共结果暴露字段

`status`, `demand`, `capacity`, `utilization`, `limit`, `unit`, `warnings`, `errors`, `intermediate_values`, `formula_traces`, `code_references`, `governing_reason`

### 产物

- `implementation/01_core_models/core_model_plan.md`
- `implementation/01_core_models/data_model_spec.md`
- `implementation/01_core_models/status_semantics.md`
- `implementation/01_core_models/unit_system.md`
- `src/<pkg>/core/`
- `src/<pkg>/books/<book_name>/book_models.py`

---

## 技能10：可复用计算模块

### 模块规则（12条）

1. 有类型化输入
2. 有类型化输出
3. 暴露一个稳定公共函数
4. 避免隐藏全局状态
5. 避免文件I/O
6. 避免UI依赖
7. 避免报告依赖
8. 避免批量特定行为
9. 验证模块特定假设
10. 返回审计所需的中间值
11. 返回警告而非静默裁剪值
12. 可独立测试

### 禁止

不得读取CSV、渲染报告、访问UI状态、写入批量摘要、或从可复用模块调用运行器。

### 产物

- `implementation/02_modules/module_interface_spec.md`
- `implementation/02_modules/formula_trace_spec.md`
- `implementation/02_modules/lookup_module_spec.md`
- `src/<pkg>/libraries/<domain>/<category>/`
- `tests/unit/test_<module>.py`
- `tests/regression/test_<module>_<reference>.py`

---

## 技能11：运行器与管控摘要

### 运行器必须做（10项）

验证book级输入、准备共享状态、应用设计选项和假设、调用可复用模块、收集模块结果、保留警告和错误、汇总管控检查、创建运行元数据、返回结构化BookResult

### 运行器禁止（5项）

渲染报告、读取原始CSV、管理UI状态、写入批量摘要、包含报告模板逻辑

### 管控摘要字段（9个）

`overall_status`, `governing_check_id`, `governing_check_name`, `governing_utilization_or_margin`, `governing_limit`, `critical_load_case_or_combination`, `controlling_location_member_foundation`, `warnings_count`, `errors_count`

### 产物

- `implementation/03_book_runner/runner_sequence.md`
- `implementation/03_book_runner/governing_summary_spec.md`
- `implementation/03_book_runner/result_path_registry.csv`
- `src/<pkg>/books/<book_name>/book_runner.py`
- `src/<pkg>/books/<book_name>/governing.py`
- `tests/integration/test_<book_name>_runner.py`

---

## 技能12：报告/审查/批量接口

### 报告生产决策协议（12项）

报告目的、目标受众、审查深度、报告状态、所需输出格式、管控来源基础、所需输入和结果来源、所需追溯元数据、报告章节、渲染器选择和理由、验证方法、已知限制

### 报告状态标签

`draft` / `review` / `final` / `superseded` / `prototype` / `not_for_construction`

### 接口允许职责

解析CSV/JSON/API输入、映射到BookInput、验证输入、调用run_book()、显示输入和结果、构建ReportContext、渲染报告、运行批量、保存标准化输入JSON、保存BookResult JSON、写入批量摘要

### 接口禁止职责

实现工程公式、为官方计算做单位转换（边界除外）、独立计算承载力/沉降/配筋/水力、重新计算pass/fail、隐藏警告/错误

### 报告流

`final_input.json → run_book() → BookResult → 保存BookResult JSON → build_report_context() → 模板/渲染 → 报告`

### 批量流

`batch_control.csv → 加载输入 → 验证 → run_book() → 保存输入JSON → 保存BookResult JSON → 按需渲染 → 批量摘要CSV → 日志`

### 产物

- `implementation/04_interfaces/input_mapping_spec.md`
- `implementation/04_interfaces/report_context_spec.md`
- `implementation/04_interfaces/review_schema.csv`
- `implementation/04_interfaces/frontend_fields.csv`
- `implementation/04_interfaces/batch_flow.md`
- `src/<pkg>/interfaces/`
- `src/<pkg>/report/`
- `tests/smoke/test_<report_or_interface>.py`

---

## 技能13：验证/回归/追溯

### 测试分类（10种）

公式单元测试、查找表测试、分支测试、边界条件测试、无效输入测试、参考回归测试、完整run_book集成测试、报告冒烟测试、批量冒烟测试、序列化与哈希测试

### 回归参考优先级（6级）

设计规范算例 > 已发布设计手册算例 > 已批准历史报告 > 已验证传统Excel > 独立手算 > 合成边界案例

### 追溯元数据字段（14个）

`book_type`, `book_name`, `case_id`, `project_id`, `design_code_and_version`, `run_timestamp`, `package_version`, `input_hash`, `result_hash`, `python_version`, `git_commit`, `formula_registry_version`, `runner_version`, `report_template_version`

### 验收检查清单（18项）

1. 来源基础已记录
2. 功能已按层级分类
3. 公式仅在可复用模块中
4. 运行器是官方计算入口
5. CSV/JSON/前端/API映射到同一BookInput
6. 单位转换仅在输入/输出边界
7. 模板不计算
8. 前端/审查不计算
9. 批量不独立计算
10. 单位是显式的
11. 结果对象包含中间值
12. 警告和错误已保留
13. 状态语义已定义
14. 管控摘要存在
15. 测试覆盖可复用模块
16. 计算书集成测试存在
17. 报告渲染冒烟测试存在（有报告时）
18. 追溯元数据存在、运行命令已文档化

### 产物

- `verification/test_matrix.csv`
- `verification/regression_references.md`
- `verification/tolerance_policy.md`
- `verification/acceptance_checklist.md`
- `tests/unit/`, `tests/regression/`, `tests/integration/`, `tests/smoke/`

---

## 技能14：云端 Web 发布与部署

### 发布目标

把工程计算系统打包为可本地运行、可 Linux/cloud 部署的 Web 计算程序，而不是静态 HTML、报告 HTML 或界面 mockup。

### 必需输入

- `handoff/implementation_handoff.yaml`
- `handoff/coding_go_no_go.md`
- 已实现的 `run_book(BookInput) -> BookResult`
- Web/API 入口、前端资源、测试、部署配置和 release checklist

### 生产 Web 最小要求

可复用计算模块、官方 runner、后端应用入口、薄 API 路由、前端模板和静态资源、表单到 BookInput 映射、BookResult 到 UI 映射、单元/集成/smoke 测试、本地运行命令、Linux/cloud 部署路径。

### 部署内容

`README.md`, `deploy/env.example`, `deploy/Dockerfile` 或 `deploy/systemd/*.service`, `deploy/nginx/*.conf`, `release/release_checklist.md`, `/health` health check, `POST /api/calculate` smoke test.

### 发布门禁

最终交付必须证明：

1. 本地运行和 health/API smoke test 通过
2. 生产入口和环境变量配置齐全
3. Docker 或 systemd/nginx 部署路径可执行
4. 计算模块不依赖 Web、报告、批量或部署层
5. `module_asset_registry.csv` 记录可复用模块
6. release checklist 记录 smoke test 和剩余假设

### 产物

- `deploy/`
- `release/release_checklist.md`
- `tests/smoke/test_web_routes.py`
- 本地运行命令和 Linux/cloud 部署命令

---

## 共享契约完整参考

### 源卡片必填字段（19项）

`source_id`, `title`, `publisher_or_author`, `source_type`, `version_or_date`, `jurisdiction`, `url_or_location`, `access_date`, `raw_file_path`, `extracted_file_path`, `authority_level`, `coverage_tags`, `relevance_to_calculation`, `key_clauses_tables_equations_pages`, `short_excerpts`, `paraphrased_notes`, `limitations`, `license_or_access_notes`, `recommended_downstream_use`

### 源获取决策状态（7种）

`persist_raw` / `persist_source_card_only` / `use_for_background_only` / `reject` / `needs_user_access` / `needs_purchase_or_license` / `needs_confirmation`

### 搜索日志字段（8项）

`search_id`, `gap_id`, `query`, `tool_or_location`, `date`, `results_reviewed`, `candidates_selected`, `notes`

### 候选源必填字段（14项）

`candidate_id`, `title`, `publisher`, `source_type`, `version_or_date`, `jurisdiction`, `url_or_location`, `access_date`, `authority_level`, `relevance_score`, `gaps_covered`, `recommended_action`, `limitations`, `license_or_access_notes`

### 本地持久化要求

必需目录：`references/raw/`, `references/source_cards/`, `references/extracted/`, `references/acquisition/`, `references/snapshots/`

必需注册表：`source_registry.yaml`, `evidence_library_manifest.yaml`, `acquisition_handoff.yaml`

哈希：SHA256，记录在 `evidence_library_manifest.yaml`。

### 互联网搜索行为要求

- 每个关键/高缺口多查询
- 优先一手和官方来源
- 可能时打开检查来源页面
- 交叉检查版本/辖区/出版商/适用性
- 记录工具到 `tool_or_location`
- 记录接受和拒绝的候选源
- 工具不可用时明确声明
