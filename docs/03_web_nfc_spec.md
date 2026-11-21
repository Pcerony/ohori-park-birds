# 03 · NFC 网页展示端规格与部署指南

本模块对应目录：`web_exhibition/`，已与 3D 硬件文件彻底剥离，**可整体作为纯静态网站根目录直接部署上线**。

---

## 一、 页面清单与 URL 映射规划

部署到您的域名（假设为 `https://birds.example.com`）后，按如下表将 URL 写入 9 枚 NFC 芯片：

| 序号 | 写入 NFC 的网页文件名 | 日语页面标题 | 鸟鸣音频文件 | 状态 |
| :--- | :--- | :--- | :--- | :--- |
| 01 | `01_black_headed_gull.html` | ユリカモメ | `assets/audio/01_black_headed_gull.mp3` (3.8s) | ✅ 已就绪 |
| 02 | `02_common_kingfisher.html` | カワセミ | `assets/audio/02_common_kingfisher.mp3` (3.8s) | ✅ 已就绪 |
| 03 | `03_grey_heron.html` | アオサギ | `assets/audio/03_grey_heron.mp3` (3.8s) | ✅ 已就绪 |
| 04 | `04_baers_pochard.html` | アカハジロ | *待人工补充 `04_baers_pochard.mp3`* | ⏳ 音频待补 |
| 05 | `05_falcated_duck.html` | ヨシガモ | `assets/audio/05_falcated_duck.mp3` (3.8s) | ✅ 已就绪 |
| 06 | `06_osprey.html` | ミサゴ | `assets/audio/06_osprey.mp3` (3.0s) | ✅ 已就绪 |
| 07 | `07_feral_pigeon.html` | カワラバト（ドバト） | `assets/audio/07_feral_pigeon.mp3` (3.8s) | ✅ 已就绪 |
| 08 | `08_northern_pintail.html` | オナガガモ | `assets/audio/08_northern_pintail.mp3` (3.8s) | ✅ 已就绪 |
| 09 | `09_ferruginous_duck.html` | メジロガモ | `assets/audio/09_ferruginous_duck.mp3` (3.8s) | ✅ 已就绪 |

> 测试导航页：`index.html`（上线后若不希望游客翻到目录页，可在写入 NFC 后选择保留或删除 `index.html`，不影响 9 个单页各自独立访问）。

---

## 二、 极简页面交互与音频播放机制

1. **视觉风格**：日式和纸微暖灰底色（`#F9F8F5`）、纯黑墨色文字（`#1C1917`）、极细分割线（`#E7E5E4`），单栏手机端宽度 `460px`，保证在任何手机浏览器中打开都简洁安静。
2. **双图像融合**：主图为高清真实野外生态照（`assets/images/*.jpg`），照片右下角悬浮圆形印章嵌入了与物理 NFC 盖子正面完全一致的**极简连笔 SVG 矢量图标**，强化实体盖子与手机页面的对应感。
3. **自动播放与手动降级兼容**：
   * 现代手机浏览器（尤其是 iOS Safari 与 Android Chrome）普遍会屏蔽未经过页面手势点击的有声自动播放。
   * 页面加载时会先尝试 `audio.play()`；如果系统放行则直接响起鸟鸣，如果被拦截则立刻在播放栏提示 **`タップして鳴き声を聴く`**，观众单指轻触按钮即可立刻播放 3～4 秒音频与进度条。

---

## 三、 补充 04 号青头潜鸭音频的方法

当您手动从 YouTube（如搜索 `Baer's pochard kinked-neck call and head-throw display`）或 Macaulay Library / 观鸟录像中截取获得原始音视频后：
1. 利用 `ffmpeg` 截取有效发声片段并做标准化处理，保存至 `web_exhibition/assets/audio/04_baers_pochard.mp3`：
   ```powershell
   ffmpeg -y -ss 起始秒数 -t 3.8 -i 原始音频.mp4 -af "highpass=f=180,loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.18,afade=t=out:st=3.55:d=0.25" -codec:a libmp3lame -b:a 128k web_exhibition/assets/audio/04_baers_pochard.mp3
   ```
2. 在项目根目录运行重新编译脚本：
   ```powershell
   python scripts/build_exhibition.py
   ```
   脚本会自动检测到 `04_baers_pochard.mp3` 文件存在并重新生成启用完整播放器的 `04_baers_pochard.html`。

---

## 四、 零成本托管部署建议

1. **Cloudflare Pages / Netlify**：无需 Git，直接在后台选择“Direct Upload（直接上传文件夹）”，将整个 `web_exhibition/` 文件夹拖入即获得全球 HTTPS 链接（国内及日本访问速度极佳，NFC 标签必须写入 HTTPS 链接才不会被手机系统安全拦截）。
2. **GitHub Pages**：将 `web_exhibition/` 里的内容推入仓库根目录或 `docs/` 分支启用 Pages 即可。
3. **NFC 写入工具**：手机下载免费的 **NFC Tools**（iOS / Android 通用）→ 选择「写」→「添加记录」→「URL / URI」→ 填入对应鸟页的 `https://...` 链接 → 贴近盖子背面写入即可（建议在写入后开启只读保护或避免覆盖，若展期需改链接请勿锁定死只读）。
