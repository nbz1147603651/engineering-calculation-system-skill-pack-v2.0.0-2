# 工程计算系统技能包 v2.1.1

本包把工程计算软件工作流升级为三段式闭环：

```text
资料获取与本地持久化
→ 资料分析与计算逻辑蓝图
→ 编程实现与验证追溯
```

适用场景：

```text
没有资料，但用户想建立工程计算程序
资料不足，无法安全抽取公式/分支/查表
已有资料，需要分析成 Calculation Logic Blueprint
已有 Blueprint / handoff，需要架构编程
已有代码，需要重构、测试、报告、批量计算
```

## v2.0 的核心变化

v1.0 已经解决了：

```text
资料分析
→ Calculation Logic Blueprint
→ Implementation Handoff Contract
→ Calculation Book Implementation
```

v2.0 新增前置层：

```text
Reference Adequacy Assessment
→ Reference Discovery and Acquisition
→ Reference Persistence and Local Evidence Library
```

这意味着当没有资料或资料不足时，模型不应该直接编造公式，也不应该勉强编码，而应该先：

```text
判断资料缺口
制定检索计划
充分调用可用的上网搜索 / 浏览 / 检索工具寻找权威资料
筛选候选来源
把可保存内容、来源卡片、摘录、检索日志、覆盖矩阵持久化到本地
再进入资料分析
```

## 推荐主流程

```text
00-router
→ 01-reference-adequacy-and-gap-assessment
→ 02-reference-discovery-and-acquisition
→ 03-reference-persistence-and-local-library
→ 04-source-intake-and-authority
→ 05-engineering-logic-blueprint
→ 06-formula-lookup-branch-extraction
→ 07-implementation-handoff-contract
→ 08-calculation-book-architecture
→ 09-core-and-data-models
→ 10-reusable-calculation-modules
→ 11-book-runner-and-governing-summary
→ 12-report-review-batch-interfaces
→ 13-verification-regression-traceability
```

## 三个父级编排技能

```text
parent/engineering-calculation-reference-acquisition.skill.md
parent/engineering-calculation-logic-architecture.skill.md
parent/engineering-calculation-book.skill.md
```

父级技能只负责编排，子技能负责具体任务。这样既避免两个巨型技能过重，也避免碎片化失控。

## Agent 入口

Codex 兼容环境优先使用根目录：

```text
SKILL.md
```

Qoder / Trae / opencode 等环境可参考：

```text
adapters/agent-entrypoints.md
```

如果目标环境不适合加载多个文件，使用单文件版本：

```text
engineering-calculation-system.all-in-one.md
```

## 最关键的接口文件

```text
references/acquisition/acquisition_handoff.yaml
references/source_registry.yaml
analysis/02_logic_blueprint/calculation_blueprint.md
analysis/03_logic_details/formula_inventory.csv
handoff/implementation_handoff.yaml
handoff/artifact_index.yaml
handoff/coding_go_no_go.md
```

其中：

```text
acquisition_handoff.yaml
```

连接“找资料”与“分析资料”；

```text
implementation_handoff.yaml
```

连接“分析资料”与“架构编程”。

## 本地持久化原则

```text
用户上传或授权保存的原始资料 → references/raw/
公开可下载且允许保存的资料 → references/raw/
不能或不应完整保存的资料 → references/source_cards/ + references/extracted/notes/
检索过程 → references/acquisition/search_log.csv
候选资料 → references/acquisition/candidate_sources.csv
资料覆盖情况 → references/acquisition/source_coverage_matrix.csv
资料注册表 → references/source_registry.yaml
```

不要绕过付费墙、登录限制、版权限制或访问控制。对于标准、规范、教材、论文等受版权保护内容，应优先保存来源卡片、短摘录、条款编号、页码、摘要和引用信息，而不是保存大段原文。

## 安装建议

复制以下目录到你的技能环境：

```text
SKILL.md
parent/
skills/
shared/
templates/
schemas/
scripts/
```

如果你的环境不适合加载多个技能，可以使用：

```text
engineering-calculation-system.all-in-one.md
```

## 校验

校验技能包：

```bash
python3 scripts/validate_artifacts.py --package-root .
```

校验内置工程骨架：

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
```

运行骨架最小测试：

```bash
cd project_template/engineering_calc_project
python3 -m pytest -q
```

## 版本

```text
version: 2.1.1
created_at: 2026-06-16
status: complete_packaged_release
```
