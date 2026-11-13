# NIMO Engineering 产品网站

这是面向使用者的产品介绍与客户端下载站。工程技能、宿主部署和工程验收契约由同一仓库的 `engineering-calculation-system` 维护。

## 本地运行

```powershell
npm ci
npm run dev -- --host 127.0.0.1
npm run build
npm run version:check
npm run preview -- --host 127.0.0.1
```

版本来自 `engineering-calculation-system/tools/release_config.json`。开发与预览服务器在已登记的 NimoSoftware 工作区中优先读取最近成功冻结的客户端；独立仓库则使用原 `dist/ui-client`。只提供匹配版本、文件名和 SHA-256 的 EXE 及对应校验文本，缺失时返回 404，不以页面 HTML 冒充下载。

## 页面与资源

- `src/App.tsx` 只负责组合页面；`src/components/product` 分别维护品牌导航、产品介绍、流程选择、平台介绍与下载区域。
- `src/product.css` 是活动样式源，使用系统字体和原生 CSS。主题为橙色 `#E58A24`、石墨色 `#202B36`、白色和浅灰 `#F5F6F8`。橙色按钮采用深色文字保证可读性。
- `public/nimo-mascot.png` 是现有品牌库 `nimo-print-clerk.png` 的透明原资源，保留 RGBA 透明通道；客户端和品牌站采用同一角色。
- 用户页面介绍使用场景与使用步骤，不显示宿主内部路径、CLI、开发工作台或校验清单；完整性校验在构建和部署层执行。
- 原界面源码保存在 `archive/pre-nimo-ui`，不参与活动构建；原图片、图标和发布包均保留。
- DeepSeek Harness 图标原样来自官方 `/harness/favicon.svg`，来源和摘要记录在对应 `deepseek-harness.source.json`；图片显式使用浅色主题，避免系统深色模式下图形变白。
- 平台展开为双列选择区，与详情面板等高；收起时保留当前选择。手机改为上下布局。
- `src/data/siteLinks.json` 维护品牌、CAD、GeoVision、Engineering、公司站及个人站的标准网址；集成打包时与 management portfolio 逐项核对。页首返回品牌站，页脚提供其他站点入口。

## 完整交付

从 NimoSoftware 工作区执行 `management/installer/Build-Engineering.ps1`，默认 `All` 联合构建客户端和网页。`-Component Desktop` 仅构建客户端，不调用 npm；`-Component Website` 仅构建网页，引用已验证的既有客户端下载，不携带 EXE；`-Component Source` 交付源码。旧 `-Component Client` 保持联合交付的含义。

`npm run build` 只生成静态前端。首次部署可使用 All 包建立 `/engineering/` 与该版本的精确下载路由；仅网页包只提供 `/engineering/` 片段，切换前应按包内摘要验证既有下载，保留原下载目录与路由。所有包均不自动上传或切换线上服务。
