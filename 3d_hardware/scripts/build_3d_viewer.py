# -*- coding: utf-8 -*-
"""
编译 3d_hardware/viewer_3d.html 本地 3D 硬件模型与 SVG 矢量预览展厅（纯离线，无 CORS 限制）。
"""
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HW_DIR = os.path.dirname(SCRIPT_DIR)
SVG_DIR = os.path.join(HW_DIR, "svg")
MODELS_DIR = os.path.join(HW_DIR, "models")
OUTPUT_HTML = os.path.join(HW_DIR, "viewer_3d.html")

base_meta = [
    {
        "id": "nfc_stand_cone",
        "rel_dir": "models/stand_cone",
        "name_zh": "⭐ 极简曲线中空喇叭口支架（主推）",
        "tag": "贯穿中空 / 曲线造型 / 约1.76g",
        "color": "#0EA5E9",
        "desc": "下窄（Ø15.0mm 环底）上宽（Ø26.15mm 插环）的优雅凹弧线杯状支架，全贯穿中空（无底无顶仅外围一圈）。顶部无多余外凸台子，直接插卡进盖子 Ø26.4mm 内侧凹槽。已预置倒扣朝向可直接切片打印！",
        "features": ["底部环圈：Ø15.0mm 窄口环接触桌面，曲线感十足", "顶部直插：Ø26.15mm × 1.1mm 环直接卡入 Ø26.4mm 盖槽内侧", "极致省料：全贯穿空心 1.55mm 环壁，单只仅约 1.76g PLA"]
    },
    {
        "id": "nfc_base_tray",
        "rel_dir": "models/legacy_bases",
        "name_zh": "备选 A：矮款外包托盘底座",
        "tag": "平置防掉免胶",
        "color": "#0284C7",
        "desc": "从下方兜住整个 Ø31.0mm 鸟类盖子（内槽 Ø31.3mm × 深 1.5mm，底板厚 1.2mm），适合不需要抬高时平置桌面。",
        "features": ["外径：Ø34.2mm（总高 2.7mm）", "内槽：Ø31.3mm 预留 +0.3mm 紧配裕量"]
    },
    {
        "id": "nfc_base_flush",
        "rel_dir": "models/legacy_bases",
        "name_zh": "备选 B：等径齐平定位底盖",
        "tag": "Ø31.0mm 等径原轮廓",
        "color": "#4F46E5",
        "desc": "外径与盖子一致（Ø31.0mm），中央带 Ø26.0mm × 0.4mm 定位凸台插入盖内居中。",
        "features": ["外径：Ø31.0mm × 底板厚 1.2mm", "内部留隙：0.9mm 高度"]
    }
]

bird_meta = [
    {"id": "01_black_headed_gull", "category_id": "common", "name_zh": "红嘴鸥", "name_en": "Black-headed Gull", "name_ja": "ユリカモメ", "status": "福冈市市鸟 / 常见冬候鸟", "color": "#DC2626", "theme_bg": "#FEF2F2", "desc": "福冈市市鸟，展翼滑翔连笔图标。盖背面 Ø26.4×1.3mm 凹槽既作 NFC 芯片限位，也用于卡合底部倒圆锥支架。", "features": ["外径 Ø31.0mm / 背面槽 Ø26.4×1.3mm", "正面 1.02mm 均匀线宽连笔图案"]},
    {"id": "02_common_kingfisher", "category_id": "common", "name_zh": "普通翠鸟", "name_en": "Common Kingfisher", "name_ja": "カワセミ", "status": "湖畔常驻明星留鸟", "color": "#0284C7", "theme_bg": "#F0FDF4", "desc": "常驻大濠公园的水边精灵，提炼粗长匕首喙与短尾轮廓。", "features": ["凸起版总高 3.1mm / 凹刻版 3.0mm", "适合双色打印或凹槽填漆"]},
    {"id": "03_grey_heron", "category_id": "common", "name_zh": "苍鹭", "name_en": "Grey Heron", "name_ja": "アオサギ", "status": "大型涉禽霸主", "color": "#334155", "theme_bg": "#F1F5F9", "desc": "大濠公园常驻涉禽，极简 S 型曲颈与脑后飘垂羽冠。", "features": ["盖底壁厚 1.1~1.2mm 隔断防穿透", "手机贴近盖顶即可穿透读卡"]},
    {"id": "04_baers_pochard", "category_id": "rare", "name_zh": "青头潜鸭", "name_en": "Baer's Pochard", "name_ja": "アカハジロ", "status": "全球极危物种 (CR)", "color": "#065F46", "theme_bg": "#ECFDF5", "desc": "全球极危潜鸭，突显圆顶头部与镂空白眼瞳环特征。", "features": ["100% 闭合水密流形", "兼容 26mm 极薄 NFC 贴纸"]},
    {"id": "05_falcated_duck", "category_id": "rare", "name_zh": "罗纹鸭", "name_en": "Falcated Duck", "name_ja": "ヨシガモ", "status": "稀有冬候鸟", "color": "#047857", "theme_bg": "#F0FDF4", "desc": "优雅“拿破仑帽”头冠与垂挂镰刀飞羽特征。", "features": ["顶部外沿 0.4mm 45° 倒角", "圆润不刮手"]},
    {"id": "06_osprey", "category_id": "rare", "name_zh": "鹗 (鱼鹰)", "name_en": "Osprey", "name_ja": "ミサゴ", "status": "罕见食鱼猛禽", "color": "#B45309", "theme_bg": "#FFFBEB", "desc": "M 字振翅俯冲造型，弯钩喙与抓鱼利爪张力十足。", "features": ["一笔流线居中对称构图", "适配倒圆锥支架悬浮展示"]},
    {"id": "07_feral_pigeon", "category_id": "historical", "name_zh": "广场家鸽", "name_en": "Feral Pigeon", "name_ja": "カワラバト", "status": "昔日常见 / 禁喂后绝迹", "color": "#6D28D9", "theme_bg": "#F5F3FF", "desc": "承载大濠公园喂鸽记忆的历史鸟种，饱满圆胸与翼上双斑。", "features": ["双版本盖子可选", "可直接下载 9 合 1 整盘 3MF"]},
    {"id": "08_northern_pintail", "category_id": "historical", "name_zh": "针尾鸭", "name_en": "Northern Pintail", "name_ja": "オナガガモ", "status": "昔日核心水禽 / 现退散", "color": "#1E293B", "theme_bg": "#F1F5F9", "desc": "长颈长针尾造型，极简流畅无碎点。", "features": ["线宽 1.02mm（0.4mm 喷嘴清晰打印）", "背面卡槽预留 +0.4mm 防缩空间"]},
    {"id": "09_ferruginous_duck", "category_id": "historical", "name_zh": "白眼潜鸭", "name_en": "Ferruginous Duck", "name_ja": "メジロガモ", "status": "90年代传奇迷鸟", "color": "#9F1239", "theme_bg": "#FFF1F2", "desc": "曾在大濠公园引爆日本观鸟圈的迷鸟，尖顶冠廓与大白眼环。", "features": ["正面 SVG + 背面支架卡口双功能合一", "可单独调整脚本公差参数"]}
]

svg_dict, emb_obj_dict, eng_obj_dict, base_obj_dict = {}, {}, {}, {}

for bm in base_meta:
    bid = bm["id"]
    with open(os.path.join(HW_DIR, bm["rel_dir"], "obj", f"{bid}.obj"), "r", encoding="utf-8") as f:
        base_obj_dict[bid] = f.read()

for b in bird_meta:
    bid = b["id"]
    with open(os.path.join(SVG_DIR, f"{bid}.svg"), "r", encoding="utf-8") as f:
        svg_dict[bid] = f.read()
    with open(os.path.join(MODELS_DIR, "caps_embossed", "obj", f"{bid}_nfc_cap.obj"), "r", encoding="utf-8") as f:
        emb_obj_dict[bid] = f.read()
    with open(os.path.join(MODELS_DIR, "caps_engraved", "obj", f"{bid}_nfc_cap_engraved.obj"), "r", encoding="utf-8") as f:
        eng_obj_dict[bid] = f.read()

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>3D 硬件工程预览器 · 大濠公园 NFC 鸟类展</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <style>
    :root {{ --bg: #0B1120; --surface: #131C31; --border: rgba(255,255,255,0.08); --text: #F8FAFC; --muted: #94A3B8; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
    header {{ background: linear-gradient(135deg, #0B1120 0%, #172554 100%); padding: 2rem 1.5rem; border-bottom: 1px solid var(--border); text-align: center; }}
    header h1 {{ font-size: 1.85rem; font-weight: 800; background: linear-gradient(to right, #38BDF8, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }}
    header p {{ color: var(--muted); max-width: 820px; margin: 0 auto; font-size: 0.88rem; }}
    .plate-group {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 0.6rem; margin-top: 1.15rem; }}
    .plate-dl {{ padding: 0.48rem 1rem; background: #0284C7; color: white; border-radius: 8px; text-decoration: none; font-size: 0.8rem; font-weight: 700; }}
    .plate-dl.alt {{ background: #4F46E5; }}
    .plate-dl.teal {{ background: #0D9488; }}
    .nav-tabs {{ display: flex; justify-content: center; gap: 0.65rem; margin-top: 1.25rem; flex-wrap: wrap; }}
    .nav-btn {{ padding: 0.42rem 1rem; background: rgba(255,255,255,0.05); border: 1px solid var(--border); border-radius: 9999px; color: var(--text); font-weight: 600; font-size: 0.82rem; cursor: pointer; }}
    .nav-btn.active {{ background: #0284C7; border-color: #38BDF8; }}
    .container {{ max-width: 1400px; margin: 2rem auto; padding: 0 1.5rem; }}
    .section-header {{ margin: 2rem 0 1rem; display: flex; align-items: center; gap: 0.8rem; }}
    .section-badge {{ padding: 0.25rem 0.7rem; border-radius: 6px; font-size: 0.76rem; font-weight: 700; }}
    .badge-base {{ background: rgba(56,189,248,0.18); color: #38BDF8; border: 1px solid #0284C7; }}
    .badge-common {{ background: rgba(16,185,129,0.18); color: #34D399; border: 1px solid #10B981; }}
    .badge-rare {{ background: rgba(245,158,11,0.18); color: #FBBF24; border: 1px solid #F59E0B; }}
    .badge-hist {{ background: rgba(244,63,94,0.18); color: #FB7185; border: 1px solid #F43F5E; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(390px, 1fr)); gap: 1.5rem; }}
    .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; display: flex; flex-direction: column; }}
    .card-top {{ padding: 1rem 1.2rem; display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid var(--border); }}
    .bird-names h3 {{ font-size: 1.15rem; font-weight: 700; }}
    .bird-sub {{ font-size: 0.78rem; color: var(--muted); }}
    .status-tag {{ font-size: 0.7rem; padding: 0.22rem 0.6rem; border-radius: 9999px; font-weight: 700; }}
    .media-container {{ position: relative; height: 290px; background: #0A0F1D; border-bottom: 1px solid var(--border); }}
    .media-tabs {{ position: absolute; top: 10px; right: 10px; z-index: 20; display: flex; gap: 4px; background: rgba(15, 23, 42, 0.88); padding: 4px; border-radius: 8px; }}
    .m-btn {{ background: transparent; border: none; color: #94A3B8; font-size: 0.7rem; font-weight: 600; padding: 4px 8px; border-radius: 5px; cursor: pointer; }}
    .m-btn.active {{ background: #0284C7; color: #FFF; }}
    .svg-pane {{ width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; padding: 1.2rem; background: radial-gradient(circle at center, #FFFFFF 0%, #F1F5F9 100%); }}
    .svg-pane svg {{ width: 210px; height: 210px; }}
    .three-pane {{ width: 100%; height: 100%; position: absolute; inset: 0; display: none; background: #0A0F1D; }}
    .three-pane canvas {{ width: 100% !important; height: 100% !important; outline: none; }}
    .flip-btn {{ position: absolute; bottom: 10px; right: 10px; z-index: 20; background: rgba(2, 132, 199, 0.92); color: white; border: none; padding: 5px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 600; cursor: pointer; }}
    .three-hint {{ position: absolute; bottom: 10px; left: 12px; z-index: 15; font-size: 0.68rem; color: rgba(255,255,255,0.5); pointer-events: none; }}
    .card-body {{ padding: 1.1rem; flex: 1; display: flex; flex-direction: column; gap: 0.7rem; }}
    .bird-desc {{ font-size: 0.84rem; color: #CBD5E1; }}
    .feature-list {{ list-style: none; font-size: 0.76rem; color: #94A3B8; background: rgba(0,0,0,0.22); padding: 0.55rem 0.8rem; border-radius: 8px; border-left: 3px solid #38BDF8; }}
    .card-footer {{ padding: 0.75rem 1.1rem; background: rgba(0,0,0,0.22); border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem; }}
    .dl-btn {{ font-size: 0.7rem; padding: 0.3rem 0.65rem; border-radius: 6px; text-decoration: none; font-weight: 600; background: rgba(255,255,255,0.08); color: #E2E8F0; border: 1px solid var(--border); }}
    .dl-btn:hover {{ background: #0284C7; color: white; }}
  </style>
</head>
<body>
  <header>
    <h1>3D 硬件工程预览器 · 大濠公园 NFC 鸟类展</h1>
    <p>本页面仅负责本地 3D 模型（倒圆锥支架、备选底座、9 款双版鸟类盖子）与 SVG 矢量源图检查与导出；对外展出的纯日语 NFC 手机网页已独立分离至 ../web_exhibition/。</p>
    <div class="plate-group">
      <a class="plate-dl teal" href="models/stand_cone/all_9_stand_cones_plate.3mf" download>⭐ 倒圆锥支架 9合1 (.3MF)</a>
      <a class="plate-dl" href="models/caps_embossed/all_9_caps_embossed_plate.3mf" download>📦 凸起版盖子 9合1 (.3MF)</a>
      <a class="plate-dl alt" href="models/caps_engraved/all_9_caps_engraved_plate.3mf" download>📦 凹刻版盖子 9合1 (.3MF)</a>
    </div>
    <div class="nav-tabs">
      <button class="nav-btn active" onclick="filterCategory('all', this)">全部</button>
      <button class="nav-btn" onclick="filterCategory('bases', this)">支架与底座</button>
      <button class="nav-btn" onclick="filterCategory('common', this)">常见鸟类</button>
      <button class="nav-btn" onclick="filterCategory('rare', this)">稀有鸟类</button>
      <button class="nav-btn" onclick="filterCategory('historical', this)">历史鸟类</button>
    </div>
  </header>
  <main class="container" id="cards-container"></main>
  <script>
    const basesData = {json.dumps(base_meta, ensure_ascii=False)};
    const birdsData = {json.dumps(bird_meta, ensure_ascii=False)};
    const svgsData = {json.dumps(svg_dict, ensure_ascii=False)};
    const embObjsData = {json.dumps(emb_obj_dict, ensure_ascii=False)};
    const engObjsData = {json.dumps(eng_obj_dict, ensure_ascii=False)};
    const baseObjsData = {json.dumps(base_obj_dict, ensure_ascii=False)};
    const categoryTitles = {{
      "common": {{ name: "现有常见鸟类盖子 (3种)", badge: "badge-common", tag: "常见" }},
      "rare": {{ name: "极度稀有鸟类盖子 (3种)", badge: "badge-rare", tag: "稀有" }},
      "historical": {{ name: "曾经有过鸟类盖子 (3种)", badge: "badge-hist", tag: "历史" }}
    }};
    const container = document.getElementById('cards-container');
    const viewers = {{}};

    function renderAll() {{
      container.innerHTML = '';
      const baseSec = document.createElement('div');
      baseSec.className = 'category-section cat-bases';
      baseSec.innerHTML = `<div class="section-header"><span class="section-badge badge-base">支架与底座</span><h2 style="font-size:1.25rem;">高台支架（主推）与备选平底托盘</h2></div><div class="grid" id="grid-bases"></div>`;
      container.appendChild(baseSec);
      const baseGrid = baseSec.querySelector('#grid-bases');

      basesData.forEach(bm => {{
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div class="card-top"><div class="bird-names"><h3>${{bm.name_zh}}</h3><div class="bird-sub">${{bm.id}}</div></div><span class="status-tag" style="background:rgba(56,189,248,0.15); color:#38BDF8">${{bm.tag}}</span></div>
          <div class="media-container"><div class="three-pane" id="base-pane-${{bm.id}}" style="display:block;"><div class="three-hint">🖱️ 拖拽旋转 / 滚轮缩放</div></div></div>
          <div class="card-body"><p class="bird-desc">${{bm.desc}}</p><ul class="feature-list">${{bm.features.map(f => `<li>✦ ${{f}}</li>`).join('')}}</ul></div>
          <div class="card-footer"><span style="font-size:0.72rem; color:var(--muted)">导出:</span><div style="display:flex; gap:0.4rem;"><a class="dl-btn" href="${{bm.rel_dir}}/stl/${{bm.id}}.stl" download>.STL</a><a class="dl-btn" href="${{bm.rel_dir}}/obj/${{bm.id}}.obj" download>.OBJ</a></div></div>
        `;
        baseGrid.appendChild(card);
        setTimeout(() => initThreeViewer(bm.id, 'base'), 50);
      }});

      ['common', 'rare', 'historical'].forEach(cat => {{
        const info = categoryTitles[cat];
        const sec = document.createElement('div');
        sec.className = `category-section cat-${{cat}}`;
        sec.innerHTML = `<div class="section-header"><span class="section-badge ${{info.badge}}">${{info.tag}}</span><h2 style="font-size:1.25rem;">${{info.name}}</h2></div><div class="grid" id="grid-${{cat}}"></div>`;
        container.appendChild(sec);
        const grid = sec.querySelector(`#grid-${{cat}}`);
        birdsData.filter(b => b.category_id === cat).forEach(bird => {{
          const card = document.createElement('div');
          card.className = 'card';
          card.innerHTML = `
            <div class="card-top"><div class="bird-names"><h3>${{bird.name_zh}}</h3><div class="bird-sub">${{bird.name_en}} · ${{bird.name_ja}}</div></div><span class="status-tag" style="background:${{bird.theme_bg}}; color:${{bird.color}}">${{bird.status}}</span></div>
            <div class="media-container" id="media-${{bird.id}}">
              <div class="media-tabs">
                <button class="m-btn active" onclick="switchMedia('${{bird.id}}', 'svg', this)">连笔 SVG</button>
                <button class="m-btn" onclick="switchMedia('${{bird.id}}', 'emb', this)">凸起盖子</button>
                <button class="m-btn" onclick="switchMedia('${{bird.id}}', 'eng', this)">凹刻盖子</button>
              </div>
              <div class="svg-pane" id="svg-pane-${{bird.id}}">${{svgsData[bird.id]}}</div>
              <div class="three-pane" id="emb-pane-${{bird.id}}"><div class="three-hint">🖱️ 旋转 / 缩放</div><button class="flip-btn" onclick="flipNFC('emb-${{bird.id}}')">🔄 翻转看背面槽</button></div>
              <div class="three-pane" id="eng-pane-${{bird.id}}"><div class="three-hint">🖱️ 旋转 / 缩放</div><button class="flip-btn" onclick="flipNFC('eng-${{bird.id}}')">🔄 翻转看背面槽</button></div>
            </div>
            <div class="card-body"><p class="bird-desc">${{bird.desc}}</p><ul class="feature-list">${{bird.features.map(f => `<li>✦ ${{f}}</li>`).join('')}}</ul></div>
            <div class="card-footer"><span style="font-size:0.72rem; color:var(--muted)">导出:</span><div style="display:flex; gap:0.35rem; flex-wrap:wrap;"><a class="dl-btn" href="svg/${{bird.id}}.svg" download>SVG</a><a class="dl-btn" href="models/caps_embossed/stl/${{bird.id}}_nfc_cap.stl" download>凸起 STL</a><a class="dl-btn" href="models/caps_engraved/stl/${{bird.id}}_nfc_cap_engraved.stl" download>凹刻 STL</a></div></div>
          `;
          grid.appendChild(card);
        }});
      }});
    }}

    function filterCategory(cat, btnEl) {{
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      btnEl.classList.add('active');
      document.querySelectorAll('.category-section').forEach(sec => {{
        sec.style.display = (cat === 'all' || sec.classList.contains(`cat-${{cat}}`)) ? 'block' : 'none';
      }});
    }}

    function switchMedia(birdId, mode, btnEl) {{
      const box = document.getElementById(`media-${{birdId}}`);
      box.querySelectorAll('.m-btn').forEach(b => b.classList.remove('active'));
      btnEl.classList.add('active');
      document.getElementById(`svg-pane-${{birdId}}`).style.display = mode === 'svg' ? 'flex' : 'none';
      document.getElementById(`emb-pane-${{birdId}}`).style.display = mode === 'emb' ? 'block' : 'none';
      document.getElementById(`eng-pane-${{birdId}}`).style.display = mode === 'eng' ? 'block' : 'none';
      if ((mode === 'emb' || mode === 'eng') && !viewers[`${{mode}}-${{birdId}}`]) initThreeViewer(birdId, mode);
    }}

    function parseOBJTwoTone(objText, accentHex, mode) {{
      const lines = objText.split('\\n');
      const verts = [], pos = [], cols = [];
      const baseCol = new THREE.Color(mode === 'base' ? 0x64748B : 0xF1F5F9);
      const accentCol = new THREE.Color(accentHex || 0x1E293B);
      const cavityCol = new THREE.Color(0x94A3B8);
      for (let i = 0; i < lines.length; i++) {{
        let line = lines[i].trim();
        if (line.startsWith('v ')) verts.push(line.split(/\\s+/).slice(1).map(Number));
        else if (line.startsWith('f ')) {{
          const p = line.split(/\\s+/).slice(1).map(s => parseInt(s.split('/')[0]) - 1);
          const tris = p.length === 4 ? [[p[0], p[1], p[2]], [p[0], p[2], p[3]]] : [[p[0], p[1], p[2]]];
          for (const [a, b, c] of tris) {{
            const va = verts[a], vb = verts[b], vc = verts[c];
            pos.push(...va, ...vb, ...vc);
            const avgZ = (va[2] + vb[2] + vc[2]) / 3.0;
            const avgR = Math.hypot((va[0]+vb[0]+vc[0])/3.0, (va[1]+vb[1]+vc[1])/3.0);
            let tc = baseCol;
            if (mode === 'emb' && avgZ > 2.52) tc = accentCol;
            else if (mode === 'eng' && avgZ > 1.8 && avgZ < 2.95 && avgR < 14.0) tc = accentCol;
            else if (mode !== 'base' && avgZ < 1.35 && avgR < 13.3) tc = cavityCol;
            cols.push(tc.r, tc.g, tc.b, tc.r, tc.g, tc.b, tc.r, tc.g, tc.b);
          }}
        }}
      }}
      const geom = new THREE.BufferGeometry();
      geom.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      geom.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
      geom.computeVertexNormals();
      return geom;
    }}

    function initThreeViewer(itemId, mode) {{
      const key = `${{mode}}-${{itemId}}`;
      const container = document.getElementById(`${{mode}}-pane-${{itemId}}`);
      const width = container.clientWidth || 390;
      const height = container.clientHeight || 290;
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x0A0F1D);
      const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 200);
      camera.position.set(0, 26, 26);
      const renderer = new THREE.WebGLRenderer({{ antialias: true }});
      renderer.setSize(width, height);
      renderer.setPixelRatio(window.devicePixelRatio);
      container.appendChild(renderer.domElement);
      const controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.autoRotate = (mode === 'base');
      controls.autoRotateSpeed = 1.2;
      scene.add(new THREE.AmbientLight(0xffffff, 0.65));
      const d1 = new THREE.DirectionalLight(0xffffff, 0.85); d1.position.set(20, 40, 25); scene.add(d1);
      const d2 = new THREE.DirectionalLight(0x38bdf8, 0.45); d2.position.set(-20, -25, -20); scene.add(d2);

      let objText = null, accent = '#1E293B';
      if (mode === 'base') {{
        objText = baseObjsData[itemId];
        const bm = basesData.find(x => x.id === itemId);
        if (bm) accent = bm.color;
      }} else {{
        objText = mode === 'emb' ? embObjsData[itemId] : engObjsData[itemId];
        const bi = birdsData.find(x => x.id === itemId);
        if (bi) accent = bi.color;
      }}
      const meshGroup = new THREE.Group();
      if (objText) {{
        const geom = parseOBJTwoTone(objText, accent, mode);
        geom.center();
        const mat = new THREE.MeshStandardMaterial({{ vertexColors: true, roughness: 0.35, metalness: 0.08, side: THREE.DoubleSide }});
        const mesh = new THREE.Mesh(geom, mat);
        mesh.rotation.x = -Math.PI / 2;
        meshGroup.add(mesh);
        scene.add(meshGroup);
      }}
      function animate() {{ requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }}
      animate();
      viewers[key] = {{ scene, camera, renderer, controls, meshGroup, flipped: false }};
    }}

    function flipNFC(key) {{
      const v = viewers[key];
      if (!v) return;
      v.flipped = !v.flipped;
      v.meshGroup.rotation.x = v.flipped ? Math.PI : 0;
    }}
    renderAll();
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Built 3D viewer at: {OUTPUT_HTML}")
