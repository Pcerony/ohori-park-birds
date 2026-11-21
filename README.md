# 福冈市大濠公园 · NFC 野鸟声音与立体展示项目

本项目围绕**日本福冈市大濠公园（Ōhori Park）**的野鸟生态调研展开，精选 **9 种代表性鸟类**（现有常见 3 种、现存极稀有 3 种、曾经有过但已消失/大幅减少 3 种），打造了一套完整的**“实体 3D 打印 NFC 展品 + 手机触碰纯日语极简网页导览”**互动展览系统。

本项目已严格按照 **“3D 硬件建模（`3d_hardware/`）”** 与 **“NFC 网页展示端（`web_exhibition/`）”** 两大独立模块进行解耦管理。

---

## 目录结构

```text
Ohori_Park_Birds_NFC/
├── README.md                          # 项目总览与快速上手指南（本文件）
├── AI_HANDOFF.md                      # 写给新接手 AI 的上下文交接文档、设计红线与待办清单
├── docs/
│   ├── 01_birds_species.md            # 9种大濠公园代表性鸟类的生态调研与选型档案
│   ├── 02_3d_cad_spec.md              # 3D硬件精密尺寸、公差配合逻辑与切片打印规范
│   └── 03_web_nfc_spec.md             # NFC 静态网页结构、部署方式与音频补全指引
│
├── 3d_hardware/                       # 【3D 硬件与矢量图标模块】（完全独立）
│   ├── svg/                           # 9个极简均匀连笔 Logo/Icon SVG 源图（256×256，无外框）
│   ├── models/
│   │   ├── caps_embossed/             # 正面凸起浮雕版鸟类盖子（STL / OBJ / 9合1整盘3MF）
│   │   ├── caps_engraved/             # 正面凹刻挖槽版鸟类盖子（STL / OBJ / 9合1整盘3MF）
│   │   ├── stand_cone/                # ⭐ 主推：下窄上宽极简省料倒圆锥高台支架（~2g PLA）
│   │   └── legacy_bases/              # 备选：平底外包托盘 / 等径齐平底 / 内嵌超薄塞片
│   ├── previews/                      # SVG、盖子正反面、支架剖面配合渲染图
│   ├── viewer_3d.html                 # 本地 3D 模型交互预览器（双击即可旋转检查模型）
│   └── scripts/                       # 可独立复现所有 SVG / STL / OBJ / 3MF 的 Python 脚本
│
├── web_exhibition/                    # 【纯静态 NFC 展示网页模块】（可直接整目录上传部署）
│   ├── index.html                     # 展厅总览测试入口
│   ├── 01_black_headed_gull.html      # 9个模板完全一致的纯日语移动端展页
│   ├── ...
│   ├── 09_ferruginous_duck.html
│   └── assets/
│       ├── images/                    # 9张真实高清生态摄影图（.jpg）
│       └── audio/                     # 8条真实鸟鸣 3~4s MP3（04青头潜鸭待手动补充）
│
└── scripts/
    └── build_exhibition.py            # 纯日语静态网页一键生成脚本
```

---

## 快速使用流程

### 1. 3D 打印制作流程
1. **选择盖子风格**：
   * 喜欢触感立体双色打印 → 使用 `3d_hardware/models/caps_embossed/all_9_caps_embossed_plate.3mf`（打印至 `Z = 2.5 mm` 处暂停换色）。
   * 喜欢平整顶面或滴胶/填色 → 使用 `3d_hardware/models/caps_engraved/all_9_caps_engraved_plate.3mf`。
2. **打印高台支架**：
   * 使用 `3d_hardware/models/stand_cone/all_9_stand_cones_plate.3mf`，模型已预置为**倒扣朝向（宽口 `Ø 26.15 mm` 在下贴热床，窄口 `Ø 15.0 mm` 朝上）**，贯穿中空一圈、曲线光滑，**无需旋转、无需支撑**（单只仅约 `1.76 g` PLA）。
3. **组装 NFC 芯片**：
   * 将直径约 **26 mm** 的超薄圆形 NFC 贴纸贴入盖子背面的 `Ø 26.4 mm × 1.3 mm` 凹槽内。
   * 将倒圆锥支架顶部 `Ø 26.15 mm` 的卡环压入盖子内侧卡槽即可完成合体（如遇公差微差，可加一滴少量瞬间胶巩固）。

### 2. 部署网页并写入 NFC
1. 将 **`web_exhibition/`** 整个文件夹直接拖拽部署到任意静态网站托管平台（如 Cloudflare Pages、Netlify、GitHub Pages、Vercel 等）。
2. 将部署后的 9 个独立 URL（例如 `https://your-domain.com/01_black_headed_gull.html`）分别用手机 NFC 工具 App 写入对应的 9 枚芯片中。
3. 参观者用手机触碰盖子顶部，即可弹出对应纯日语展页、查看实拍图并点击听取 3～4 秒真实鸟鸣。

> **注：关于新的 AI 接手工作**
> 请务必先阅读根目录下的 **[AI_HANDOFF.md](AI_HANDOFF.md)**，其中完整记录了不可破坏的设计规范、公差耦合关系及当前唯一待人工补全的项目事项（`04_baers_pochard.mp3` 音频）。
