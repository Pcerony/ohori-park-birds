# -*- coding: utf-8 -*-
"""
重新设计的极简曲线中空倒圆锥高台支架：
1. 贯穿中空（无底封、无顶封，仅外围一圈薄壁曲面壳）
2. 优雅的曲线感（底部窄小挺拔，向上光滑外展成流畅花萼/酒杯曲线）
3. 顶部无外凸台阶：曲线直接汇聚至 Ø26.15mm 插入环，直接插卡进盖子 Ø26.4mm 内侧凹槽
4. 预置为“倒扣打印朝向”（宽口 Ø26.15mm 置于 Z=0 热床，窄口 Ø15.0mm 朝上），
   在 Bambu Studio 中拖入即可零支撑直接打印！
"""
import os
import math
import numpy as np
import trimesh
from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HW_DIR = os.path.dirname(SCRIPT_DIR)
STAND_DIR = os.path.join(HW_DIR, "models", "stand_cone")
PREVIEW_DIR = os.path.join(HW_DIR, "previews")
os.makedirs(os.path.join(STAND_DIR, "stl"), exist_ok=True)
os.makedirs(os.path.join(STAND_DIR, "obj"), exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

# 关键参数 (单位: mm)
R_BOT = 7.5            # 底部接触环外径 Ø15.0 mm
R_TOP = 13.075         # 顶部插入环外径 Ø26.15 mm (完美卡入盖子 Ø26.4 mm 内壁，无任何多余外凸台子)
WALL_T = 1.55          # 均匀水平径向壁厚 1.55 mm（垂直法向等效厚 ~1.2-1.55mm，3~4道实心壁，极省料）
INSERT_H = 1.1         # 顶部插入盖槽的直壁高度 1.1 mm (加上 ~0.2mm 超薄芯片刚好贴合 1.3mm 深槽)
CURVE_H = 16.0         # 下段优雅曲线高度 16.0 mm (总高 17.1 mm)
TOTAL_H = CURVE_H + INSERT_H  # 17.1 mm

def eval_bezier_curve(n_steps=40):
    p0 = np.array([R_BOT, 0.0])
    p1 = np.array([R_BOT, CURVE_H * 0.45])
    p2 = np.array([R_BOT + (R_TOP - R_BOT) * 0.35, CURVE_H * 0.78])
    p3 = np.array([R_TOP, CURVE_H])

    ts = np.linspace(0.0, 1.0, n_steps)
    pts = []
    for t in ts:
        mt = 1.0 - t
        p = (mt**3)*p0 + 3*(mt**2)*t*p1 + 3*mt*(t**2)*p2 + (t**3)*p3
        pts.append(p)
    pts = np.array(pts)

    max_ang = 0.0
    for i in range(len(pts) - 1):
        dr = abs(pts[i+1, 0] - pts[i, 0])
        dz = abs(pts[i+1, 1] - pts[i, 1])
        ang = math.degrees(math.atan2(dr, dz)) if dz > 1e-6 else 90.0
        max_ang = max(max_ang, ang)
    return pts, max_ang

def build_curved_hollow_stand(print_upside_down=True):
    outer_curve, max_ang = eval_bezier_curve(n_steps=36)
    print(f"Curve max angle from vertical: {max_ang:.1f} deg")

    # 构建完整严格闭合截面的环形轮廓（逆时针），保持单调无交叉点：
    # 1. 底部环内侧点 -> 外沿微倒角 -> 外侧贝塞尔曲线至 CURVE_H -> 插入环直壁至 TOTAL_H -> 顶部导角
    # 2. 内环顶角 -> 内侧等壁厚曲线下降回底部 -> 明确闭合回起点！
    prof = []
    # 底部环平底（Z=0）
    prof.append([R_BOT - WALL_T, 0.0])
    prof.append([R_BOT - 0.15, 0.0])
    prof.append([R_BOT, 0.15])
    # 外曲线（严格递增 z > 0.15）
    for r, z in outer_curve[1:]:
        if z > 0.2:
            prof.append([float(r), float(z)])
    # 顶部插入盖内侧的直环段 (Ø26.15 mm) + 顶部 0.22mm 引导倒角
    prof.append([R_TOP, TOTAL_H - 0.22])
    prof.append([R_TOP - 0.22, TOTAL_H])
    prof.append([R_TOP - WALL_T, TOTAL_H])
    # 内环降落回曲线段
    for r, z in reversed(outer_curve[1:]):
        if z > 0.2:
            prof.append([float(r - WALL_T), float(z)])
    # 明确闭合回第一个点，使环形截面 100% 闭合水密！
    prof.append(prof[0])

    profile = np.array(prof)
    if print_upside_down:
        # 倒扣翻转用于直接打印：Z_print = TOTAL_H - Z_upright
        profile[:, 1] = TOTAL_H - profile[:, 1]
        profile = profile[::-1]

    m = trimesh.creation.revolve(profile, sections=128)
    m.merge_vertices()
    m.fix_normals()
    return m

def render_iso_mesh(mesh, max_dim=32.0, img_size=340, rx_deg=-68, rz_deg=-25, color_fn=None):
    verts = mesh.vertices.copy()
    faces = mesh.faces
    v_center = np.array([0.0, 0.0, (verts[:,2].min() + verts[:,2].max()) / 2.0])
    rv_base = verts - v_center

    rx, rz = np.radians(rx_deg), np.radians(rz_deg)
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0], [np.sin(rz), np.cos(rz), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(rx), -np.sin(rx)], [0, np.sin(rx), np.cos(rx)]])
    rv = rv_base @ (Rx @ Rz).T

    v0, v1, v2 = rv[faces[:, 0]], rv[faces[:, 1]], rv[faces[:, 2]]
    fn = np.cross(v1 - v0, v2 - v0)
    norms = np.linalg.norm(fn, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    fn = fn / norms

    light = np.array([0.35, 0.55, 0.76])
    light /= np.linalg.norm(light)
    intensity = np.clip(fn @ light, 0.2, 1.0)

    z_cent = (v0[:, 2] + v1[:, 2] + v2[:, 2]) / 3.0
    order = np.argsort(z_cent)

    scale = (img_size * 0.72) / max_dim
    cx, cy = img_size / 2.0, img_size / 2.0
    img = Image.new("RGB", (img_size, img_size), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    for idx in order:
        if fn[idx, 2] <= 0:
            continue
        pts = [
            (cx + v0[idx, 0] * scale, cy - v0[idx, 1] * scale),
            (cx + v1[idx, 0] * scale, cy - v1[idx, 1] * scale),
            (cx + v2[idx, 0] * scale, cy - v2[idx, 1] * scale),
        ]
        base_col = np.array(color_fn(verts[faces[idx]])) if color_fn else np.array([148, 163, 184])
        c = tuple((base_col * (0.45 + 0.62 * intensity[idx])).clip(0, 255).astype(int))
        draw.polygon(pts, fill=c)
    return img

def render_cutaway_2d(mass_g, img_size=340):
    img = Image.new("RGB", (img_size, img_size), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    scale = 7.6
    cx = img_size / 2.0
    cy = img_size - 55.0

    def pt(r, z):
        return (cx + r * scale, cy - z * scale)

    outer_curve, _ = eval_bezier_curve(n_steps=36)
    prof = [[R_BOT - WALL_T, 0.0], [R_BOT - 0.15, 0.0], [R_BOT, 0.15]]
    for r, z in outer_curve[1:]:
        if z > 0.2:
            prof.append([float(r), float(z)])
    prof.extend([[R_TOP, TOTAL_H - 0.22], [R_TOP - 0.22, TOTAL_H], [R_TOP - WALL_T, TOTAL_H]])
    for r, z in reversed(outer_curve[1:]):
        if z > 0.2:
            prof.append([float(r - WALL_T), float(z)])

    draw.polygon([pt(r, z) for r, z in prof], fill=(100, 116, 139))
    draw.polygon([pt(-r, z) for r, z in prof], fill=(100, 116, 139))

    cap_z0 = CURVE_H
    cap_prof = [
        (0.0, cap_z0 + 1.3), (13.2, cap_z0 + 1.3), (13.2, cap_z0 + 0.25), (13.45, cap_z0 + 0.0),
        (15.3, cap_z0 + 0.0), (15.5, cap_z0 + 0.2), (15.5, cap_z0 + 2.6), (15.1, cap_z0 + 3.0), (0.0, cap_z0 + 3.0)
    ]
    draw.polygon([pt(r, z) for r, z in cap_prof], fill=(203, 213, 225), outline=(51, 65, 85))
    draw.polygon([pt(-r, z) for r, z in cap_prof], fill=(203, 213, 225), outline=(51, 65, 85))

    draw.rectangle([pt(-13.0, cap_z0 + 1.3), pt(13.0, cap_z0 + 1.08)], fill=(234, 88, 12))
    draw.line([pt(-18, 0), pt(18, 0)], fill=(148, 163, 184), width=2)

    draw.text((14, 14), "4. Cutaway Fit (Open Hollow)", fill=(15, 23, 42))
    draw.text((14, 34), "No outer ledge! Plugs straight inside", fill=(71, 85, 105))
    draw.text((14, 52), f"Through-hole shell: ~{mass_g:.2f}g PLA", fill=(234, 88, 12))
    draw.text((14, img_size - 28), "Base OD 15mm -> Curve -> Top OD 26.15mm", fill=(71, 85, 105))
    return img

if __name__ == "__main__":
    stand_print = build_curved_hollow_stand(print_upside_down=True)
    stand_upright = build_curved_hollow_stand(print_upside_down=False)

    vol_mm3 = abs(stand_print.volume)
    mass_g = (vol_mm3 / 1000.0) * 1.24

    stand_print.export(os.path.join(STAND_DIR, "stl", "nfc_stand_cone.stl"))
    stand_print.export(os.path.join(STAND_DIR, "obj", "nfc_stand_cone.obj"))
    print(f"Stand (upside down) watertight={stand_print.is_watertight}, "
          f"extents={stand_print.extents.round(2).tolist()}, vol={vol_mm3:.1f}mm^3 (~{mass_g:.2f}g PLA)")

    plate = []
    for i in range(9):
        col, row = i % 3, i // 3
        m = stand_print.copy()
        m.apply_translation([(col - 1) * 32.0, (1 - row) * 32.0, 0.0])
        plate.append(m)
    p = trimesh.util.concatenate(plate)
    p.export(os.path.join(STAND_DIR, "all_9_stand_cones_plate.stl"))
    p.export(os.path.join(STAND_DIR, "all_9_stand_cones_plate.3mf"))
    print("Exported print-ready upside-down 9-in-1 curved stand plates (.stl & .3mf).")

    cap = trimesh.load(os.path.join(HW_DIR, "models", "caps_embossed", "stl", "01_black_headed_gull_nfc_cap.stl"))
    cap_seated = cap.copy()
    cap_seated.apply_translation([0, 0, CURVE_H])
    assembled = trimesh.util.concatenate([stand_upright, cap_seated])

    w = 340
    sheet = Image.new("RGB", (w * 4, w), (248, 250, 252))
    draw = ImageDraw.Draw(sheet)

    im1 = render_iso_mesh(stand_print, 32.0, w, -65, -25, lambda tri: [100, 116, 139])
    im2 = render_iso_mesh(stand_upright, 32.0, w, -72, -25, lambda tri: [100, 116, 139])

    def assem_color(tri):
        z = tri[:, 2].mean()
        if z > CURVE_H + 2.52:
            return [220, 38, 38]
        elif z >= CURVE_H:
            return [226, 232, 240]
        else:
            return [71, 85, 105]

    im3 = render_iso_mesh(assembled, 34.0, w, -66, -25, assem_color)
    im4 = render_cutaway_2d(mass_g, w)

    sheet.paste(im1, (0, 0))
    sheet.paste(im2, (w, 0))
    sheet.paste(im3, (w * 2, 0))
    sheet.paste(im4, (w * 3, 0))

    draw.text((14, 14), "1. Print Orientation (Upside Down!)", fill=(15, 23, 42))
    draw.text((w + 14, 14), "2. Upright Curved Profile", fill=(15, 23, 42))
    draw.text((w * 2 + 14, 14), "3. Assembled (Cap + Curved Stand)", fill=(15, 23, 42))

    preview_p = os.path.join(PREVIEW_DIR, "preview_stand_cone.png")
    sheet.save(preview_p)
    print(f"Saved updated curved stand preview: {preview_p}")
