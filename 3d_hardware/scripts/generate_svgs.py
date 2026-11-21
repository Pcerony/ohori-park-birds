# -*- coding: utf-8 -*-
"""
生成 9 只大濠公园代表性鸟类的极简均匀连笔 Logo/Icon SVG 文件。
输出位置：../svg/*.svg 与 ../previews/preview_logos.png
"""
import os
import re
from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HW_DIR = os.path.dirname(SCRIPT_DIR)
SVG_DIR = os.path.join(HW_DIR, "svg")
PREVIEW_DIR = os.path.join(HW_DIR, "previews")
os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

STROKE_WIDTH = 10.0
STROKE_COLOR = "#111827"

BIRDS_LOGO_SPEC = {
    "01_black_headed_gull": {
        "title": "01 Black-headed Gull",
        "paths": [
            "M 48 76 C 80 68, 112 88, 128 114 C 146 96, 174 96, 192 108 L 220 116 L 188 126 C 174 150, 144 170, 108 176 L 52 184 C 82 160, 98 140, 106 126 C 80 116, 56 98, 48 76 Z",
            "M 136 104 C 142 74, 158 52, 184 52 C 170 72, 162 88, 160 100",
            "M 164 122 C 158 130, 150 134, 142 134"
        ],
        "dots": [(178, 110, 4.0)],
        "rings": []
    },
    "02_common_kingfisher": {
        "title": "02 Common Kingfisher",
        "paths": [
            "M 222 96 L 152 88 C 142 62, 108 56, 86 76 C 68 92, 66 128, 72 154 L 48 184 L 82 172 C 98 192, 128 194, 146 172 C 162 152, 160 124, 152 110 L 222 96 Z",
            "M 96 108 C 122 118, 126 148, 94 164"
        ],
        "dots": [(132, 86, 4.2)],
        "rings": []
    },
    "03_grey_heron": {
        "title": "03 Grey Heron",
        "paths": [
            "M 218 64 L 154 62 C 144 50, 122 52, 114 66 C 92 92, 98 118, 120 128 C 98 130, 76 136, 52 158 L 86 166 C 110 172, 136 168, 148 150 C 160 134, 148 112, 134 98 C 124 88, 128 76, 152 74 L 218 64 Z",
            "M 130 54 C 106 46, 82 52, 66 66",
            "M 118 168 L 118 214 L 136 214",
            "M 98 166 L 90 214 L 106 214"
        ],
        "dots": [(144, 64, 3.8)],
        "rings": []
    },
    "04_baers_pochard": {
        "title": "04 Baers Pochard",
        "paths": [
            "M 214 116 L 168 110 C 162 82, 140 68, 116 74 C 98 80, 98 104, 104 114 C 82 118, 60 126, 46 142 L 62 162 L 166 162 C 180 148, 178 130, 162 122 L 214 116 Z",
            "M 80 148 C 104 134, 134 136, 148 148",
            "M 120 116 C 132 121, 144 121, 154 118"
        ],
        "dots": [],
        "rings": [(142, 90, 6.0)]
    },
    "05_falcated_duck": {
        "title": "05 Falcated Duck",
        "paths": [
            "M 214 114 L 168 108 C 160 76, 134 56, 90 58 C 78 58, 78 76, 98 86 C 110 92, 110 106, 102 114 C 78 118, 52 134, 42 168 L 76 164 L 166 164 C 182 148, 178 130, 162 122 L 214 114 Z",
            "M 106 130 C 88 134, 76 146, 72 162",
            "M 124 108 C 136 114, 148 114, 158 110"
        ],
        "dots": [(146, 88, 4.0)],
        "rings": []
    },
    "06_osprey": {
        "title": "06 Osprey",
        "paths": [
            "M 108 106 L 52 62 C 44 84, 52 106, 72 122 L 106 132 C 102 152, 98 170, 92 188 L 134 188 L 134 152 C 146 158, 158 168, 166 180 L 154 186",
            "M 108 106 C 116 78, 140 70, 158 80 L 178 92 L 162 98 C 156 98, 152 104, 148 114 L 146 136",
            "M 146 74 L 200 48 C 212 70, 206 96, 186 114 L 154 122",
            "M 126 94 L 144 94"
        ],
        "dots": [(146, 82, 3.6)],
        "rings": []
    },
    "07_feral_pigeon": {
        "title": "07 Feral Pigeon",
        "paths": [
            "M 196 88 L 172 84 C 166 64, 142 62, 134 78 C 128 90, 126 104, 114 118 L 52 172 L 84 172 L 138 168 C 172 164, 186 138, 172 114 C 166 104, 168 98, 174 94 L 196 88 Z",
            "M 96 138 L 112 154",
            "M 112 128 L 128 144",
            "M 134 170 L 140 206 L 156 206",
            "M 112 170 L 102 206 L 118 206"
        ],
        "dots": [(154, 78, 3.8)],
        "rings": []
    },
    "08_northern_pintail": {
        "title": "08 Northern Pintail",
        "paths": [
            "M 216 78 L 172 72 C 164 50, 134 50, 126 68 C 116 86, 118 112, 102 122 L 72 128 L 32 94 L 66 146 L 84 166 L 174 166 C 182 144, 170 124, 166 106 C 162 92, 164 84, 172 82 L 216 78 Z",
            "M 142 146 C 142 122, 142 100, 146 82"
        ],
        "dots": [(152, 66, 3.8)],
        "rings": []
    },
    "09_ferruginous_duck": {
        "title": "09 Ferruginous Duck",
        "paths": [
            "M 212 114 L 168 110 C 160 88, 152 68, 142 68 C 132 68, 120 90, 114 112 C 92 116, 72 120, 48 108 L 66 144 L 82 164 L 166 164 C 180 150, 178 130, 162 122 L 212 114 Z",
            "M 88 142 C 110 132, 132 134, 146 146"
        ],
        "dots": [],
        "rings": [(144, 92, 6.2)]
    }
}

def eval_cubic(p0, p1, p2, p3, steps=28):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        x = (mt**3)*p0[0] + 3*(mt**2)*t*p1[0] + 3*mt*(t**2)*p2[0] + (t**3)*p3[0]
        y = (mt**3)*p0[1] + 3*(mt**2)*t*p1[1] + 3*mt*(t**2)*p2[1] + (t**3)*p3[1]
        pts.append((x, y))
    return pts

def parse_svg_path(d_str, curve_steps=28):
    tokens = re.findall(r'[MLCZmlcz]|[-+]?\d*\.?\d+', d_str)
    subpaths, cur_sub = [], []
    cur, start = (0.0, 0.0), (0.0, 0.0)
    idx, cmd = 0, None
    while idx < len(tokens):
        t = tokens[idx]
        if t.isalpha():
            cmd = t
            idx += 1
            if cmd in ('Z', 'z'):
                if cur_sub:
                    cur_sub.append(start)
                    subpaths.append((cur_sub, True))
                    cur_sub = []
                cur = start
            continue
        if cmd == 'M':
            if cur_sub:
                subpaths.append((cur_sub, False))
            x, y = float(tokens[idx]), float(tokens[idx+1])
            idx += 2
            cur = start = (x, y)
            cur_sub = [cur]
            cmd = 'L'
        elif cmd == 'L':
            x, y = float(tokens[idx]), float(tokens[idx+1])
            idx += 2
            cur = (x, y)
            cur_sub.append(cur)
        elif cmd == 'C':
            x1, y1, x2, y2, x3, y3 = map(float, tokens[idx:idx+6])
            idx += 6
            pts = eval_cubic(cur, (x1, y1), (x2, y2), (x3, y3), steps=curve_steps)
            cur_sub.extend(pts[1:])
            cur = (x3, y3)
    if cur_sub:
        subpaths.append((cur_sub, False))
    return subpaths

def write_svg(filename, spec):
    lines = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">']
    lines.append(f'  <g fill="none" stroke="{STROKE_COLOR}" stroke-width="{STROKE_WIDTH}" stroke-linecap="round" stroke-linejoin="round">')
    for d in spec["paths"]:
        lines.append(f'    <path d="{d}"/>')
    for cx, cy, r in spec["rings"]:
        lines.append(f'    <circle cx="{cx}" cy="{cy}" r="{r}" stroke-width="{STROKE_WIDTH * 0.72:.1f}"/>')
    lines.append('  </g>')
    if spec["dots"]:
        lines.append(f'  <g fill="{STROKE_COLOR}">')
        for cx, cy, r in spec["dots"]:
            lines.append(f'    <circle cx="{cx}" cy="{cy}" r="{r}"/>')
        lines.append('  </g>')
    lines.append('</svg>')
    out_path = os.path.join(SVG_DIR, f"{filename}.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path

if __name__ == "__main__":
    cell = 300
    grid_img = Image.new("RGB", (cell * 3, cell * 3), (248, 250, 252))
    draw = ImageDraw.Draw(grid_img)

    for i, (bird_id, spec) in enumerate(BIRDS_LOGO_SPEC.items()):
        path = write_svg(bird_id, spec)
        print(f"Generated SVG: {path}")
        col, row = i % 3, i // 3
        cx_cell, cy_cell = col * cell + cell // 2, row * cell + cell // 2
        draw.ellipse([cx_cell - 126, cy_cell - 126, cx_cell + 126, cy_cell + 126], outline=(226, 232, 240), fill=(255, 255, 255), width=2)
        scale = 220 / 256.0
        ox, oy = cx_cell - 128 * scale, cy_cell - 128 * scale
        sw = max(2, int(round(STROKE_WIDTH * scale)))
        for d in spec["paths"]:
            for pts, _ in parse_svg_path(d, curve_steps=32):
                spts = [(ox + x * scale, oy + y * scale) for x, y in pts]
                for k in range(len(spts) - 1):
                    draw.line([spts[k], spts[k+1]], fill=(17, 24, 39), width=sw)
                r_pt = sw / 2.0
                for px, py in spts[::2]:
                    draw.ellipse([px - r_pt, py - r_pt, px + r_pt, py + r_pt], fill=(17, 24, 39))
        for cx, cy, r in spec["rings"]:
            px, py, pr = ox + cx * scale, oy + cy * scale, r * scale
            rsw = max(2, int(round(STROKE_WIDTH * 0.72 * scale)))
            draw.ellipse([px - pr - rsw/2, py - pr - rsw/2, px + pr + rsw/2, py + pr + rsw/2], outline=(17, 24, 39), width=rsw)
        for cx, cy, r in spec["dots"]:
            px, py, pr = ox + cx * scale, oy + cy * scale, r * scale
            draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(17, 24, 39))
        draw.text((col * cell + 16, row * cell + 12), spec["title"], fill=(71, 85, 105))

    grid_img.save(os.path.join(PREVIEW_DIR, "preview_logos.png"))
    print("Done.")
