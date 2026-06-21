"""Internationalization (i18n) module for the deployment console.

Provides translation support for Chinese (zh) and English (en).
All UI strings are centralized here so adding new languages is straightforward.
"""

from __future__ import annotations

from typing import Literal

Language = Literal["en", "zh"]

_TRANSLATIONS: dict[Language, dict[str, str]] = {
    "en": {
        # Window title
        "window_title": "Engineering Calculation System - Deployment Console",
        "window_title_zh": "工程计算系统 - 部署控制台",
        # Top bar
        "title": "Engineering Calculation System — Deployment Console",
        "title_zh": "工程计算系统 — 部署控制台",
        "theme_light": "Light",
        "theme_light_zh": "浅色",
        "theme_dark": "Dark",
        "theme_dark_zh": "深色",
        "theme_system": "System",
        "theme_system_zh": "跟随系统",
        "lang_en": "EN",
        "lang_zh": "中文",
        # Scrollable frame
        "target_agents": "Target Agents",
        "target_agents_zh": "目标代理",
        # Status badge
        "checking": "checking…",
        "checking_zh": "检测中…",
        "program_installed": "program installed",
        "program_installed_zh": "程序已安装",
        "program_not_found": "program not found",
        "program_not_found_zh": "未找到程序",
        "deployed": "deployed",
        "deployed_zh": "已部署",
        "not_deployed": "not deployed",
        "not_deployed_zh": "未部署",
        # Kind tags
        "kind_user": "user",
        "kind_user_zh": "用户级",
        "kind_project": "project",
        "kind_project_zh": "项目级",
        # Root label
        "root_not_set": "root: (not set)",
        "root_not_set_zh": "根目录：（未设置）",
        "root_prefix": "root: ",
        "root_prefix_zh": "根目录：",
        # Action buttons
        "btn_deploy": "Deploy",
        "btn_deploy_zh": "部署",
        "btn_verify": "Verify",
        "btn_verify_zh": "验证",
        "btn_remove": "Remove",
        "btn_remove_zh": "移除",
        "btn_folder": "Folder…",
        "btn_folder_zh": "文件夹…",
        # Bottom action row
        "btn_rescan": "Re-scan",
        "btn_rescan_zh": "重新扫描",
        "btn_build_all": "Build all profiles",
        "btn_build_all_zh": "构建所有配置",
        "btn_repo": "Repo…",
        "btn_repo_zh": "仓库…",
        "repo_not_set": "repo: (not set)",
        "repo_not_set_zh": "仓库：（未设置）",
        "repo_prefix": "repo: ",
        "repo_prefix_zh": "仓库：",
        "status_ready": "ready",
        "status_ready_zh": "就绪",
        # Bottom controls
        "btn_clear_log": "Clear log",
        "btn_clear_log_zh": "清除日志",
        "btn_stop": "Stop",
        "btn_stop_zh": "停止",
        # Progress
        "progress_idle": "idle",
        "progress_idle_zh": "空闲",
        "progress_starting": "starting…",
        "progress_starting_zh": "启动中…",
        "progress_done": "done",
        "progress_done_zh": "完成",
        "progress_failed": "failed",
        "progress_failed_zh": "失败",
        # Dialogs
        "dlg_select_repo_title": "Select the Engineering Calculation System skill-pack repository folder\n(contains tools/build_release.py)",
        "dlg_select_repo_title_zh": "选择工程计算系统技能包仓库文件夹\n(包含 tools/build_release.py)",
        "dlg_invalid_repo": "Invalid repo folder",
        "dlg_invalid_repo_zh": "无效的仓库文件夹",
        "dlg_no_repo_warn": "[warn] no repo root selected. Pick one with the 'Repo…' button before deploying.",
        "dlg_no_repo_warn_zh": "[警告] 未选择仓库根目录。部署前请使用 '仓库…' 按钮选择一个。",
        "dlg_select_project_root": "Select project root for {name}",
        "dlg_select_project_root_zh": "为 {name} 选择项目根目录",
        "dlg_select_root_title": "Select project root",
        "dlg_select_root_title_zh": "选择项目根目录",
        "dlg_select_root_msg": "Pick a project root for {name} first (Folder… button).",
        "dlg_select_root_msg_zh": "请先为 {name} 选择项目根目录（使用 文件夹… 按钮）。",
        "dlg_confirm_uninstall": "Confirm uninstall",
        "dlg_confirm_uninstall_zh": "确认卸载",
        "dlg_confirm_uninstall_msg": (
            "Remove the Engineering Calculation System files for {name}?\n"
            "Existing files are backed up; only this package's managed files are removed."
        ),
        "dlg_confirm_uninstall_msg_zh": (
            "确定要移除 {name} 的工程计算系统文件吗？\n"
            "现有文件会被备份，仅移除此包管理的文件。"
        ),
        # Log messages
        "log_deploy": "=== Deploy {name} ===",
        "log_deploy_zh": "=== 部署 {name} ===",
        "log_verify": "=== Verify {name} ===",
        "log_verify_zh": "=== 验证 {name} ===",
        "log_uninstall": "=== Uninstall {name} ===",
        "log_uninstall_zh": "=== 卸载 {name} ===",
        "log_build_all": "=== Build all release profiles ===",
        "log_build_all_zh": "=== 构建所有发布配置 ===",
        "log_job_busy": "[warn] a job is already running; wait for it to finish.",
        "log_job_busy_zh": "[警告] 已有任务正在运行，请等待完成。",
        "log_job_rejected": "[warn] worker rejected the job.",
        "log_job_rejected_zh": "[警告] 工作线程拒绝了该任务。",
        "log_cancel": "[warn] cancel requested; finishing current step…",
        "log_cancel_zh": "[警告] 已请求取消，正在完成当前步骤…",
        "log_done": "[done] {msg}",
        "log_done_zh": "[完成] {msg}",
        "log_error": "[error] {msg}",
        "log_error_zh": "[错误] {msg}",
        "log_repo_set": "[repo] skill-pack root set to {path}",
        "log_repo_set_zh": "[仓库] 技能包根目录已设为 {path}",
        # Job titles
        "job_deploy": "Deploy",
        "job_deploy_zh": "部署",
        "job_verify": "Verify",
        "job_verify_zh": "验证",
        "job_uninstall": "Uninstall",
        "job_uninstall_zh": "卸载",
        "job_build_all": "Build all profiles",
        "job_build_all_zh": "构建所有配置",
        # Agent summaries
        "summary_codex": "OpenAI Codex skill folder install",
        "summary_codex_zh": "OpenAI Codex 技能文件夹安装",
        "summary_minimax": "Mavis skills repository layout",
        "summary_minimax_zh": "Mavis 技能仓库布局",
        "summary_zcode": "~/.zcode user skill folder install",
        "summary_zcode_zh": "~/.zcode 用户级技能文件夹安装",
        "summary_qoder": "~/.qoder overlay (supervisor + workers)",
        "summary_qoder_zh": "~/.qoder 覆盖层（主程序 + 工作器）",
        "summary_qoder_project": "Project-root .qoder/ overlay (recommended)",
        "summary_qoder_project_zh": "项目根目录 .qoder/ 覆盖层（推荐）",
        "summary_trae": "Project-root .trae/ + AGENTS.md overlay",
        "summary_trae_zh": "项目根目录 .trae/ + AGENTS.md 覆盖层",
        "summary_opencode": "Project-root .opencode/ overlay",
        "summary_opencode_zh": "项目根目录 .opencode/ 覆盖层",
        "summary_agents_generic": "AGENTS.md + .agents/skills convention",
        "summary_agents_generic_zh": "AGENTS.md + .agents/skills 约定",
        # Agent display names
        "name_qoder_user": "Qoder (user)",
        "name_qoder_user_zh": "Qoder（用户级）",
        "name_qoder_project": "Qoder Project",
        "name_qoder_project_zh": "Qoder 项目级",
        "name_agents_generic": "AGENTS Generic",
        "name_agents_generic_zh": "AGENTS 通用",
        # Deployer messages
        "deployer_invalid_repo": "selected folder does not look like the skill-pack repo (tools/build_release.py missing): {path}",
        "deployer_invalid_repo_zh": "所选文件夹不是技能包仓库（缺少 tools/build_release.py）：{path}",
        "deployer_no_python": "no system Python found on PATH. The deployment exe needs Python 3.9+ installed on the target machine to build the skill pack (it runs tools/build_release.py). Install Python or run from source.",
        "deployer_no_python_zh": "在 PATH 中未找到系统 Python。部署程序需要目标机器上安装 Python 3.9+ 来构建技能包（运行 tools/build_release.py）。请安装 Python 或从源码运行。",
        "deployer_no_repo_root": "skill-pack repository location is not set. Select the repo folder in the UI first.",
        "deployer_no_repo_root_zh": "技能包仓库位置未设置。请先在界面中选择仓库文件夹。",
        "deployer_source_missing": "source missing: {src} (run build first)",
        "deployer_source_missing_zh": "源文件缺失：{src}（请先运行构建）",
        "deployer_source_file_missing": "source file missing: {src}",
        "deployer_source_file_missing_zh": "源文件缺失：{src}",
        "deployer_no_install_root": "no install root selected (pick a directory first)",
        "deployer_no_install_root_zh": "未选择安装根目录（请先选择一个目录）",
        "deploy_codex_done": "Codex deploy complete",
        "deploy_codex_done_zh": "Codex 部署完成",
        "uninstall_codex_done": "[done] Codex skill removed",
        "uninstall_codex_done_zh": "[完成] Codex 技能已移除",
        "deploy_minimax_done": "MiniMax deploy complete",
        "deploy_minimax_done_zh": "MiniMax 部署完成",
        "uninstall_minimax_done": "[done] MiniMax skill removed",
        "uninstall_minimax_done_zh": "[完成] MiniMax 技能已移除",
        "deploy_zcode_done": "ZCode skill deploy complete",
        "deploy_zcode_done_zh": "ZCode 技能部署完成",
        "uninstall_zcode_done": "[done] ZCode skill removed",
        "uninstall_zcode_done_zh": "[完成] ZCode 技能已移除",
        "deploy_qoder_user_done": "Qoder user overlay installed",
        "deploy_qoder_user_done_zh": "Qoder 用户级覆盖层已安装",
        "uninstall_qoder_user_done": "[done] Qoder user overlay removed",
        "uninstall_qoder_user_done_zh": "[完成] Qoder 用户级覆盖层已移除",
        "deploy_project_done": "{agent} project overlay deployed",
        "deploy_project_done_zh": "{agent} 项目覆盖层已部署",
        "uninstall_qoder_project_done": "[done] .qoder overlay removed (core skill left intact)",
        "uninstall_qoder_project_done_zh": "[完成] .qoder 覆盖层已移除（核心技能保留）",
        "uninstall_trae_done": "[done] .trae overlay removed",
        "uninstall_trae_done_zh": "[完成] .trae 覆盖层已移除",
        "uninstall_opencode_done": "[done] .opencode overlay removed",
        "uninstall_opencode_done_zh": "[完成] .opencode 覆盖层已移除",
        "uninstall_agents_generic_done": "[done] AGENTS.md + .agents overlay removed",
        "uninstall_agents_generic_done_zh": "[完成] AGENTS.md + .agents 覆盖层已移除",
        # Detector messages
        "detector_codex_not_found": "codex CLI not on PATH and ~/.codex absent",
        "detector_codex_not_found_zh": "codex CLI 不在 PATH 中且 ~/.codex 不存在",
        "detector_mavis_not_found": "mavis CLI not on PATH and ~/.mavis absent",
        "detector_mavis_not_found_zh": "mavis CLI 不在 PATH 中且 ~/.mavis 不存在",
        "detector_zcode_not_found": "zcode CLI not on PATH and ~/.zcode absent",
        "detector_zcode_not_found_zh": "zcode CLI 不在 PATH 中且 ~/.zcode 不存在",
        "detector_qoder_not_found": "qoder CLI not on PATH and ~/.qoder absent",
        "detector_qoder_not_found_zh": "qoder CLI 不在 PATH 中且 ~/.qoder 不存在",
        "detector_trae_not_found": "trae CLI not on PATH (project-overlay install only)",
        "detector_trae_not_found_zh": "trae CLI 不在 PATH 中（仅支持项目覆盖层安装）",
        "detector_opencode_not_found": "opencode CLI not on PATH (project-overlay install only)",
        "detector_opencode_not_found_zh": "opencode CLI 不在 PATH 中（仅支持项目覆盖层安装）",
        "detector_unknown_agent": "unknown agent",
        "detector_unknown_agent_zh": "未知代理",
        "detector_no_root_selected": "no install root selected",
        "detector_no_root_selected_zh": "未选择安装根目录",
        "detector_no_sentinel": "no sentinel defined for",
        "detector_no_sentinel_zh": "未定义检测标记文件",
        "detector_sentinel_missing": "sentinel missing under",
        "detector_sentinel_missing_zh": "检测标记文件缺失：",
    },
    "zh": {
        # Will be filled dynamically from "en" with zh overrides
    },
}

# Build the zh dict: start from en values, then override with zh-specific ones.
def _build_zh() -> dict[str, str]:
    en = _TRANSLATIONS["en"]
    zh: dict[str, str] = {}
    for key, val in en.items():
        # Skip _zh variant keys; they are translation sources, not real keys.
        if key.endswith("_zh"):
            continue
        # If there's a _zh variant, use it; otherwise keep the English value
        zh_key = key + "_zh"
        if zh_key in en:
            zh[key] = en[zh_key]
        else:
            zh[key] = val
    return zh

_TRANSLATIONS["zh"] = _build_zh()


class I18n:
    """Simple translation helper. Thread-safe for read-only access."""

    def __init__(self, language: Language = "en") -> None:
        self._lang: Language = language

    @property
    def language(self) -> Language:
        return self._lang

    @language.setter
    def language(self, value: Language) -> None:
        if value not in _TRANSLATIONS:
            raise ValueError(f"Unsupported language: {value}")
        self._lang = value

    def t(self, key: str, **kwargs) -> str:
        """Translate a key, optionally formatting with kwargs."""
        table = _TRANSLATIONS.get(self._lang, _TRANSLATIONS["en"])
        text = table.get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                pass
        return text


# Global singleton - set language via set_language()
_i18n = I18n("en")


def get_i18n() -> I18n:
    return _i18n


def set_language(lang: Language) -> None:
    _i18n.language = lang


def t(key: str, **kwargs) -> str:
    """Convenience function: translate using the global i18n instance."""
    return _i18n.t(key, **kwargs)
