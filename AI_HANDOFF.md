# AI_HANDOFF.md — 后续接手 AI 工作交接指南

> 本文件专为后续接手继续迭代本项目的 AI 助手编写。在修改任何代码、3D 参数、SVG 或网页之前，请先完整通读本文档与 `docs/` 目录下的规格说明。

---

## 1. 项目核心目标与边界

这是一个**物理 3D 展品 + 手机 NFC 网页**结合的极简艺术/生态展示项目，主题为**日本福冈市大濠公园的 9 种野鸟**：
* **硬件端（`3d_hardware/`）**：9 个盖子（正面带鸟类极简连笔 SVG 图案，背面带 Ø26mm NFC 限位及卡口凹槽） + 下窄上宽的中空倒圆锥省料支架。
* **网页端（`web_exhibition/`）**：9 个结构完全一致的纯日语移动端极简展示页，手机触碰 NFC 后弹出对应鸟类网页（播放叫声 + 看图片 + 简单介绍 + 与大濠公园的关系）。
* **解耦原则**：`web_exhibition/` 必须保持纯静态零脚本零 3D 冗余文件，可直接整文件夹上传托管服务器；所有生成脚本和 3D 资产均放在 `3d_hardware/` 与 `scripts/`。

---

## 2. 绝对不可随意破坏的设计红线

### 红线一：SVG 图标风格规范
* **禁止加圆形/方形外框**：此前试版因为外轮廓加了圆圈导致盖上后质感极差，已被用户明确否定。当前 `3d_hardware/svg/*.svg` 为 **透明底、无外框、无文字** 的纯符号。
* **均匀线宽与连笔风格**：必须维持 `viewBox="0 0 256 256"` 与均匀 `stroke-width="10.0"`、`stroke-linecap="round"`、`stroke-linejoin="round"`。该线宽映射至 3D 盖面后约 **1.02 mm**，刚好匹配标准 `0.4 mm` 喷嘴的 2～3 道壁线打印；改细会导致 3D 打印断线或挤出失败。

### 红线二：3D 硬件尺寸耦合链（修改一处必须联动校核配对件）
目前盖子与支架通过 **内侧卡合** 精准配合，各关键尺寸（mm）联动如下：
1. **盖子外径**：`31.0 mm`（`generate_caps.py` -> `OUTER_DIAMETER = 31.0`）
2. **盖子背面凹槽（限位芯片 + 卡住支架）**：
   * 直径 `26.4 mm`（为 26 mm 贴片和打印热收缩预留 `+0.4 mm` 裕量，入口倒角至 `Ø26.9 mm`）
   * 深度 `1.3 mm`（`CAVITY_DEPTH = 1.3`）
3. **盖子顶部实心隔离层**：
   * 凸起版盖子底部 `2.5 mm`（实心隔层 `1.2 mm`）+ 图案凸起 `0.6 mm` = 总高 `3.1 mm`
   * 凹刻版盖子总高 `3.0 mm` - 向下刻深 `0.6 mm` = 实心隔层 `1.1 mm`（严禁刻穿至 `Z = 1.3 mm`）
4. **曲线中空高台支架（`generate_stand_cone.py`）**：
   * **全贯穿中空环形壳体**（无底封、无顶封，壁厚 `WALL_T = 1.55 mm`），单只体积仅约 `1420 mm³`（~`1.76 g` PLA）。
   * **无外凸承托台**：顶部最高端外径即为 `Ø 26.15 mm`（`R_TOP = 13.075`，直环高度 `INSERT_H = 1.1 mm`），直接插卡进盖子 `Ø 26.4 mm` 洞内壁；盖内余下 `0.2 mm` 空间给极薄 NFC 贴纸。
   * **优雅曲线轮廓**：底部窄圈 `Ø 15.0 mm`（`R_BOT = 7.5`）经三次贝塞尔凹弧线平滑外扩至 `Ø 26.15 mm`（高 `CURVE_H = 16.0 mm`，最大斜率仅 `45°`，全自动零支撑打印）。
   * **预置倒扣打印朝向**：导出文件 `nfc_stand_cone.stl` 及 `all_9_stand_cones_plate.3mf` 默认已是宽口（`Ø 26.15 mm`）平贴热床 `Z=0`、窄口朝上的倒扣姿态，拖入切片软件无需翻转即可直接打印！若需微调卡环松紧，只需修改 `R_TOP` 后重跑脚本即可。

### 红线三：网页端规范
* **全站纯日语**：`web_exhibition/` 下所有对游客展示的页面（`index.html` 与 `01..09.html`）必须保持 100% 纯自然日语，不得混入中文提示或英文 UI 按钮。
* **移动端音频兼容**：保留 `AUDIO_SCRIPT` 中“自动尝试 `audio.play()` + 被浏览器策略拦截时无缝显示 `タップして鳴き声を聴く` 单击播放”的双保险逻辑。

---

## 3. 当前唯一已知待办事项（TODO）

### 待补全：04 号青头潜鸭（`04_baers_pochard` / アカハジロ）的真实鸟鸣音频
* **现状原因**：青头潜鸭为全球极危物种（IUCN CR）且越冬期几乎不发声，Wikimedia Commons、Xeno-canto、GBIF、iNaturalist 等公开无门坎数据库中均为 0 音频；Macaulay Library（`baepoc`）有记录但网站启用了人机验证门禁。因此目前 `web_exhibition/assets/audio/` 下仅有 **8 个 MP3**，`04_baers_pochard.html` 暂显示“公開音声アーカイブが未収録です”的诚实提示。
* **后续 AI 如何协助用户完成此项**：
  1. 当用户从 YouTube（如 `Baer's pochard kinked-neck call and head-throw display`）、Macaulay Library 手动下载或通过国内观鸟 App 取得任何格式的原始视频/音频文件后；
  2. 使用已安装的 `ffmpeg` 截取出最清晰的 **3.8 秒**片段，进行高通滤波、响度均衡（`loudnorm`）与淡入淡出，输出为：
     `web_exhibition/assets/audio/04_baers_pochard.mp3`
  3. 运行 `python scripts/build_exhibition.py`——脚本会自动检测到文件已存在且大于 1KB，立刻将 `04_baers_pochard.html` 切换为带完整播放器的版本！

---

## 4. 环境依赖与一键重构命令

已验证本地运行环境（Windows PowerShell + Python 3.11.9）：
* **Python 第三方库**：`numpy`, `scipy`, `PIL (Pillow)`, `shapely (2.2.0)`, `trimesh (5.2.1)`, `manifold3d`
* **系统命令行工具**：`ffmpeg`（已安装 `Gyan.FFmpeg` 8.1）

常用重编译命令（均在项目根目录 `Ohori_Park_Birds_NFC/` 下执行）：
```powershell
# 1. 重新生成 9 个连笔 SVG 矢量图
python 3d_hardware/scripts/generate_svgs.py

# 2. 修改公差后重新生成 18 个凸起/凹刻版盖子 STL/OBJ 及 3MF 整盘
python 3d_hardware/scripts/generate_caps.py

# 3. 修改卡环直径或高度后重新生成倒圆锥支架 STL/OBJ/3MF
python 3d_hardware/scripts/generate_stand_cone.py

# 4. 重新打包离线 3D 工程预览器 (3d_hardware/viewer_3d.html)
python 3d_hardware/scripts/build_3d_viewer.py

# 5. 重新编译纯日语 NFC 展示网页 (web_exhibition/*.html)
python scripts/build_exhibition.py
```
