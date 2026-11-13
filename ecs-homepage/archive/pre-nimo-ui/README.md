# NIMO 前端重构前的界面源码

这里保留重构前的页面、样式、动画及语言数据，供历史回退和对照；所有原有图片与平台图标继续保存在 src/assets 和 public，未删除。

当前入口是 src/App.tsx，产品界面由 src/components/product 和 src/product.css 组成。归档代码不参与 TypeScript 检查或 Vite 打包；不需要为它重新安装 Framer Motion 或 Tailwind。

活动界面使用系统字体、原生 CSS、React 和透明 Nimo 原资源。用户页面不公开部署目录、CLI、插件内部接口或校验清单；工程维护信息在工程核心的 docs/NIMO_ARCHITECTURE.md。
