# -*- coding: utf-8 -*-
"""
编译纯粹可部署的纯日语 NFC 展示静态网页模块 (../web_exhibition/*.html)。
读取 ../3d_hardware/svg/*.svg 并检测 ../web_exhibition/assets/audio/*.mp3 是否存在。
（若后续补入了 04_baers_pochard.mp3，直接重新运行本脚本即可自动激活 04 号页面播放器！）
"""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SVG_DIR = os.path.join(PROJECT_ROOT, "3d_hardware", "svg")
EX_DIR = os.path.join(PROJECT_ROOT, "web_exhibition")
AUDIO_DIR = os.path.join(EX_DIR, "assets", "audio")
os.makedirs(EX_DIR, exist_ok=True)

EXHIBITION_BIRDS = [
    {
        "id": "01_black_headed_gull", "num": "01",
        "category_ja": "現在よく見られる鳥", "cat_style": "common",
        "name_ja": "ユリカモメ", "name_kana": "百合鷗", "name_sci": "Chroicocephalus ridibundus",
        "intro_ja": "白い体に鮮やかな赤い嘴（くちばし）と脚が映える、小型で軽やかなカモメの仲間です。冬羽では目の後ろに小さな黒褐色の斑点が現れ、古くから「都鳥（みやこどり）」の名でも親しまれてきました。",
        "ohori_ja": "福岡市の「市の鳥」に指定されており、大濠公園の冬を象徴する存在です。毎年秋から春にかけて北の繁殖地から大群で飛来し、広い池の上空を優雅に舞ったり、橋の欄干や杭の上で羽を休めたりする姿が見られます。"
    },
    {
        "id": "02_common_kingfisher", "num": "02",
        "category_ja": "現在よく見られる鳥", "cat_style": "common",
        "name_ja": "カワセミ", "name_kana": "翡翠", "name_sci": "Alcedo atthis",
        "intro_ja": "コバルトブルーの背中と鮮やかなオレンジ色の腹部を持つことから「空飛ぶ宝石」と呼ばれる小鳥です。体のわりに長く真っ直ぐなくちばしを持ち、水辺の枝から一気にダイブして小魚を捕らえます。",
        "ohori_ja": "一年を通して大濠公園で観察できる人気の留鳥です。中の島や鴨島、野鳥の森周辺の石垣や柳の枝にとまって水面を見つめる姿がよく見られ、都会の中心にありながらその美しい輝きに間近に出会えます。"
    },
    {
        "id": "03_grey_heron", "num": "03",
        "category_ja": "現在よく見られる鳥", "cat_style": "common",
        "name_ja": "アオサギ", "name_kana": "蒼鷺", "name_sci": "Ardea cinerea",
        "intro_ja": "日本に生息するサギ類の中で最大級の大型水鳥です。青みがかった灰色の翼、S字に湾曲する長い首、そして後頭部からなびく黒い冠羽が特徴で、浅瀬で獲物をじっと待ち伏せて鋭いくちばしで捕食します。",
        "ohori_ja": "大濠公園の岸辺や池の杭の上で最もよく見かける常連の住人です。散歩やジョギングをする人々を恐れることなくすぐ近くで堂々と佇む姿は公園の日常風景の一部であり、野鳥の森などをねぐらに暮らしています。"
    },
    {
        "id": "04_baers_pochard", "num": "04",
        "category_ja": "現在いるが極めて希少な鳥", "cat_style": "rare",
        "name_ja": "アカハジロ", "name_kana": "赤羽白", "name_sci": "Aythya baeri",
        "intro_ja": "深い暗緑色の光沢を持つ頭と、オスの透き通るような白い虹彩（白目）、脇腹の白い模様が特徴の潜水が上手なカモです。世界的な生息数が極めて少なく、絶滅危惧IA類（CR）に指定されています。",
        "ohori_ja": "日本への飛来数自体が非常に少ない希少種ですが、福岡市内の自然調査において大濠公園およびその周辺水系で貴重な記録が残されています。冬に訪れるホシハジロなどの群れにひっそりと紛れて姿を見せます。"
    },
    {
        "id": "05_falcated_duck", "num": "05",
        "category_ja": "現在いるが極めて希少な鳥", "cat_style": "rare",
        "name_ja": "ヨシガモ", "name_kana": "葦鴨", "name_sci": "Mareca falcata",
        "intro_ja": "オスは頭頂部から後頭にかけて緑と赤紫に輝くふっくらとした冠羽を持ち、その形が「ナポレオンの帽子」に例えられる美しいカモです。尾の近くに垂れ下がる、鎌のように湾曲した長い飾り羽も印象的です。",
        "ohori_ja": "大濠公園に冬になるとごく少数だけが飛来する、ひときわ優雅で貴重な冬鳥です。ホシハジロやヒドリガモの大群に混じって静かに泳いでいることが多く、その華麗な姿はバードウォッチャーたちの密かな人気を集めています。"
    },
    {
        "id": "06_osprey", "num": "06",
        "category_ja": "現在いるが極めて希少な鳥", "cat_style": "rare",
        "name_ja": "ミサゴ", "name_kana": "鶚", "name_sci": "Pandion haliaetus",
        "intro_ja": "魚を主食とする大型の猛禽類（タカの仲間）です。白い頭部に目の横を通る太い黒帯模様があり、水面上空でホバリングしたあと、鋭いトゲ状の突起がある大きな足から豪快に水中へダイブして魚を掴み上げます。",
        "ohori_ja": "普段は博多湾などの沿岸部で多く暮らしていますが、豊かな魚類が生息する大濠公園の広い池にも稀に飛来します。ビル群を背景に池の上空を力強く旋回し、水面へ急降下する姿は都会の公園とは思えない迫力があります。"
    },
    {
        "id": "07_feral_pigeon", "num": "07",
        "category_ja": "かつていた鳥", "cat_style": "historical",
        "name_ja": "カワラバト（ドバト）", "name_kana": "河原鳩", "name_sci": "Columba livia",
        "intro_ja": "丸みのあるふくよかな胸元と、灰色の翼に入った2本のくっきりとした黒い帯が特徴のハトです。首元の羽毛には光の当たり方で紫や緑に輝く金属光沢があり、人によく馴れる習性を持っています。",
        "ohori_ja": "昭和から平成初期にかけての大濠公園では、売店のポップコーンやパンくずを求める数百羽ものドバトがベンチ周辺に群がり、人々と触れ合うのが定番の光景でした。しかし現在は環境保全から餌やりが全面禁止となり、かつての大群は姿を消しました。"
    },
    {
        "id": "08_northern_pintail", "num": "08",
        "category_ja": "かつていた鳥", "cat_style": "historical",
        "name_ja": "オナガガモ", "name_kana": "尾長鴨", "name_sci": "Anas acuta",
        "intro_ja": "名前の通り、ピンと長く尖った針のような尾羽と、すっきりと伸びた細長い首を持つ優美なカモです。オスはチョコレート色の頭に首筋へ伸びる白いラインが気品を感じさせ、水草や穀物を好んで食べます。",
        "ohori_ja": "かつては人馴れして岸辺でパンなどをもらうのが得意だったため、冬の大濠公園を埋め尽くすほど多く見られました。餌やりの禁止後は自然の餌場を求めて博多湾の干潟などへ移り、現在の大濠公園ではかつてのような大群は見られなくなりました。"
    },
    {
        "id": "09_ferruginous_duck", "num": "09",
        "category_ja": "かつていた鳥", "cat_style": "historical",
        "name_ja": "メジロガモ", "name_kana": "目白鴨", "name_sci": "Aythya nyroca",
        "intro_ja": "深みのある濃い栗褐色の羽毛と、尾羽の下側にある鮮やかな純白の三角形模様、そして名前（目白鴨）の由来となった白い虹彩が特徴の小型潜水ガモです。本来はユーラシア大陸西部を中心に分布しています。",
        "ohori_ja": "1990年代初頭の冬、珍しい迷鳥として遠く離れた福岡の大濠公園に飛来し、越冬した記録は全国の野鳥ファンの間で大きな話題となりました。その後は九州沿岸でまれに記録されることはあるものの、大濠公園での定期的な姿は見られなくなっています。"
    }
]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>{name_ja} | 大濠公園 野鳥アーカイブ展</title>
  <style>
    :root {{ --bg: #F9F8F5; --card: #FFFFFF; --ink: #1C1917; --muted: #78716C; --line: #E7E5E4; --accent: {accent_color}; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
    body {{ font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Noto Sans JP", "Yu Gothic", sans-serif; background-color: var(--bg); color: var(--ink); line-height: 1.85; min-height: 100vh; display: flex; justify-content: center; padding: 24px 16px 48px; }}
    .wrap {{ width: 100%; max-width: 460px; }}
    .top-bar {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; letter-spacing: 0.12em; color: var(--muted); margin-bottom: 18px; padding-bottom: 10px; border-bottom: 1px solid var(--line); }}
    .badge {{ display: inline-block; font-size: 11px; font-weight: 600; letter-spacing: 0.06em; padding: 4px 12px; border-radius: 999px; color: var(--accent); border: 1px solid var(--accent); margin-bottom: 14px; }}
    .photo-box {{ position: relative; width: 100%; background: #EFECE6; border-radius: 12px; overflow: hidden; margin-bottom: 20px; }}
    .photo-box img.bird-photo {{ width: 100%; height: auto; max-height: 460px; object-fit: cover; object-position: 50% 20%; display: block; }}
    .svg-seal {{ position: absolute; bottom: 12px; right: 12px; width: clamp(44px, 12vw, 56px); height: clamp(44px, 12vw, 56px); background: rgba(255, 255, 255, 0.92); backdrop-filter: blur(6px); border-radius: 50%; padding: 9px; box-shadow: 0 4px 14px rgba(0,0,0,0.12); display: flex; align-items: center; justify-content: center; }}
    .svg-seal svg {{ width: 100%; height: 100%; }}
    .title-area {{ margin-bottom: 20px; }}
    .title-area h1 {{ font-size: 28px; font-weight: 700; letter-spacing: 0.06em; line-height: 1.3; }}
    .title-sub {{ font-size: 12px; color: var(--muted); letter-spacing: 0.04em; margin-top: 4px; }}
    .audio-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; margin-bottom: 24px; display: flex; align-items: center; gap: 14px; }}
    .play-btn {{ width: 44px; height: 44px; border-radius: 50%; border: none; background: var(--ink); color: #FFFFFF; font-size: 15px; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; transition: transform 0.15s; }}
    .play-btn:active {{ transform: scale(0.94); }}
    .play-btn.disabled {{ background: #D6D3D1; cursor: default; }}
    .audio-meta {{ flex: 1; min-width: 0; }}
    .audio-label {{ font-size: 13px; font-weight: 600; color: var(--ink); margin-bottom: 6px; display: flex; justify-content: space-between; }}
    .audio-time {{ font-size: 11px; font-weight: 400; color: var(--muted); font-variant-numeric: tabular-nums; }}
    .progress-track {{ width: 100%; height: 3px; background: var(--line); border-radius: 2px; overflow: hidden; }}
    .progress-fill {{ width: 0%; height: 100%; background: var(--ink); transition: width 0.1s linear; }}
    .audio-note {{ font-size: 11px; color: var(--muted); margin-top: 4px; }}
    .section {{ margin-bottom: 22px; padding-top: 18px; border-top: 1px solid var(--line); }}
    .section h2 {{ font-size: 12px; font-weight: 600; letter-spacing: 0.1em; color: var(--muted); margin-bottom: 8px; }}
    .section p {{ font-size: 14.5px; color: #292524; text-align: justify; }}
    .footer {{ margin-top: 36px; padding-top: 16px; border-top: 1px solid var(--line); text-align: center; font-size: 11px; letter-spacing: 0.1em; color: var(--muted); }}
  </style>
</head>
<body>
  <main class="wrap">
    <div class="top-bar"><span>大濠公園 野鳥アーカイブ展</span><span>NO. {num} / 09</span></div>
    <span class="badge">{category_ja}</span>
    <div class="photo-box">
      <img class="bird-photo" src="assets/images/{id}.jpg" alt="{name_ja}">
      <div class="svg-seal" title="NFCキャップアイコン">{inline_svg}</div>
    </div>
    <div class="title-area">
      <h1>{name_ja}</h1>
      <div class="title-sub">{name_kana} ／ <i>{name_sci}</i></div>
    </div>
    {audio_block}
    <section class="section"><h2>特徴・生態</h2><p>{intro_ja}</p></section>
    <section class="section"><h2>大濠公園との関わり</h2><p>{ohori_ja}</p></section>
    <footer class="footer">福岡市 大濠公園 ・ NFC 野鳥サウンドガイド</footer>
  </main>
  {audio_script}
</body>
</html>
"""

AUDIO_AVAILABLE = """<div class="audio-card">
      <button class="play-btn" id="playBtn" aria-label="鳴き声を再生">▶</button>
      <div class="audio-meta">
        <div class="audio-label"><span id="statusText">鳴き声を聴く</span><span class="audio-time" id="timeText">0:00</span></div>
        <div class="progress-track"><div class="progress-fill" id="progressBar"></div></div>
      </div>
      <audio id="birdAudio" src="assets/audio/{id}.mp3" preload="auto" playsinline></audio>
    </div>"""

AUDIO_UNAVAILABLE = """<div class="audio-card">
      <button class="play-btn disabled" disabled aria-label="音声なし">—</button>
      <div class="audio-meta">
        <div class="audio-label"><span>鳴き声（記録極めて希少）</span><span class="audio-time">—</span></div>
        <div class="audio-note">絶滅危惧種かつ越冬期はほとんど鳴かないため、公開音声アーカイブが未収録です。</div>
      </div>
    </div>"""

AUDIO_SCRIPT = """<script>
    (function() {
      const audio = document.getElementById('birdAudio'), btn = document.getElementById('playBtn');
      const statusText = document.getElementById('statusText'), timeText = document.getElementById('timeText'), bar = document.getElementById('progressBar');
      if (!audio) return;
      const fmt = s => !isFinite(s) ? '0:00' : Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
      const sync = () => { btn.textContent = audio.paused ? '▶' : '❚❚'; statusText.textContent = audio.paused ? '鳴き声を再生' : '再生中…'; };
      const updateMeta = () => { if (isFinite(audio.duration) && audio.duration > 0) timeText.textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration); };
      btn.addEventListener('click', () => audio.paused ? audio.play().catch(()=>{}) : audio.pause());
      audio.addEventListener('play', sync); audio.addEventListener('pause', sync);
      audio.addEventListener('ended', () => { btn.textContent = '▶'; statusText.textContent = 'もう一度聴く'; bar.style.width = '0%'; audio.currentTime = 0; updateMeta(); });
      audio.addEventListener('timeupdate', () => { if (audio.duration) { bar.style.width = ((audio.currentTime/audio.duration)*100).toFixed(1)+'%'; timeText.textContent = fmt(audio.currentTime)+' / '+fmt(audio.duration); }});
      audio.addEventListener('loadedmetadata', updateMeta);
      updateMeta();
      const tryAutoplay = () => { const p = audio.play(); if (p !== undefined) p.then(sync).catch(() => { statusText.textContent = 'タップして鳴き声を聴く'; }); };
      if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', tryAutoplay); else tryAutoplay();
    })();
  </script>"""

def build_pages():
    colors = {"common": "#047857", "rare": "#B45309", "historical": "#57534E"}
    for b in EXHIBITION_BIRDS:
        bid = b["id"]
        with open(os.path.join(SVG_DIR, f"{bid}.svg"), "r", encoding="utf-8") as f:
            inline_svg = f.read().strip()
        mp3_p = os.path.join(AUDIO_DIR, f"{bid}.mp3")
        has_audio = os.path.exists(mp3_p) and os.path.getsize(mp3_p) > 1000
        html = PAGE_TEMPLATE.format(
            id=bid, num=b["num"], category_ja=b["category_ja"], accent_color=colors[b["cat_style"]],
            name_ja=b["name_ja"], name_kana=b["name_kana"], name_sci=b["name_sci"],
            intro_ja=b["intro_ja"], ohori_ja=b["ohori_ja"], inline_svg=inline_svg,
            audio_block=(AUDIO_AVAILABLE.format(id=bid) if has_audio else AUDIO_UNAVAILABLE),
            audio_script=(AUDIO_SCRIPT if has_audio else "")
        )
        out = os.path.join(EX_DIR, f"{bid}.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Built {out} (audio={has_audio})")

    links = [f'<a class="item" href="{b["id"]}.html"><span class="num">{b["num"]}</span><span class="name">{b["name_ja"]}</span><span class="cat">{b["category_ja"]}</span></a>' for b in EXHIBITION_BIRDS]
    portal = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>大濠公園 野鳥アーカイブ展 — 一覧</title><style>body{{font-family:"Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif;background:#F9F8F5;color:#1C1917;padding:36px 16px;display:flex;justify-content:center;}}.wrap{{width:100%;max-width:520px;}}h1{{font-size:20px;font-weight:700;letter-spacing:.08em;margin-bottom:6px;}}p{{font-size:12px;color:#78716C;margin-bottom:24px;}}.list{{display:flex;flex-direction:column;gap:10px;}}.item{{display:flex;align-items:center;gap:12px;background:#FFF;border:1px solid #E7E5E4;border-radius:10px;padding:14px 16px;text-decoration:none;color:inherit;}}.item:hover{{border-color:#1C1917;}}.num{{font-size:12px;color:#78716C;width:22px;}}.name{{font-size:15px;font-weight:600;flex:1;}}.cat{{font-size:11px;color:#78716C;}}</style></head><body><div class="wrap"><h1>大濠公園 野鳥アーカイブ展</h1><p>NFCタグに紐づく9種の展示ページ一覧（各ページは同一のミニマル構成です）</p><div class="list">{"".join(links)}</div></div></body></html>"""
    with open(os.path.join(EX_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(portal)
    print("Built exhibition index.html")

if __name__ == "__main__":
    build_pages()
