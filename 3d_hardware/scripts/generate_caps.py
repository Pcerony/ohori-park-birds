# -*- coding: utf-8 -*-
"""
生成 9 款大濠公园鸟类 NFC 芯片盖子 3D 模型（凸起浮雕版 + 凹刻挖槽版），输出 STL / OBJ / 9合1整盘 3MF。
物理参数（单位：mm，修改后重新运行即可同步调整公差）：
- OUTER_DIAMETER = 31.0 (外径)
- CAVITY_DIAMETER = 26.4 (背面为 Ø26mm 芯片预留 +0.4mm 防缩裕量)
- CAVITY_DEPTH = 1.3 (背面凹槽深度，入口含 0.25mm 导角)
"""
import os
import sys
import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import trimesh
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from generate_svgs import BIRDS_LOGO_SPEC, STROKE_WIDTH, parse_svg_path

HW_DIR = os.path.dirname(SCRIPT_DIR)
MODELS_DIR = os.path.join(HW_DIR, "models")
EMB_DIR = os.path.join(MODELS_DIR, "caps_embossed")
ENG_DIR = os.path.join(MODELS_DIR, "caps_engraved")
PREVIEW_DIR = os.path.join(HW_DIR, "previews")

for d in (
    os.path.join(EMB_DIR, "stl"), os.path.join(EMB_DIR, "obj"),
    os.path.join(ENG_DIR, "stl"), os.path.join(ENG_DIR, "obj"),
    PREVIEW_DIR
):
    os.makedirs(d, exist_ok=True)

OUTER_DIAMETER = 31.0
CAVITY_DIAMETER = 26.4
CAVITY_DEPTH = 1.3
EMB_BASE_HEIGHT = 2.5
EMB_RELIEF_HEIGHT = 0.6
ENG_BASE_HEIGHT = 3.0
ENG_CARVE_DEPTH = 0.6
SVG_MAP_SIZE = 26.0

def create_base_cap_mesh(base_height):
    r_out = OUTER_DIAMETER / 2.0
    r_in = CAVITY_DIAMETER / 2.0
    profile = np.array([
        [0.0, CAVITY_DEPTH],
        [r_in, CAVITY_DEPTH],
        [r_in, 0.25],
        [r_in + 0.25, 0.0],
        [r_out - 0.2, 0.0],
        [r_out, 0.2],
        [r_out, base_height - 0.4],
        [r_out - 0.4, base_height],
        [0.0, base_height]
    ])
    cap = trimesh.creation.revolve(profile, sections=128)
    cap.fix_normals()
    return cap

def svg_to_shapely_geometry(spec):
    scale = SVG_MAP_SIZE / 256.0
    half_w = (STROKE_WIDTH * 0.5) * scale
    half_ring_w = (STROKE_WIDTH * 0.72 * 0.5) * scale
    def map_pt(x, y):
        return ((x - 128.0) * scale, -(y - 128.0) * scale)
    geoms = []
    for d in spec["paths"]:
        for pts, _ in parse_svg_path(d, curve_steps=32):
            if len(pts) < 2:
                continue
            buf = sg.LineString([map_pt(x, y) for x, y in pts]).buffer(half_w, resolution=16, cap_style='round', join_style='round')
            if not buf.is_empty:
                geoms.append(buf)
    for cx, cy, r in spec["rings"]:
        px, py = map_pt(cx, cy)
        pr = r * scale
        ring = sg.Point(px, py).buffer(pr + half_ring_w, resolution=24).difference(
            sg.Point(px, py).buffer(max(0.05, pr - half_ring_w), resolution=24)
        )
        if not ring.is_empty:
            geoms.append(ring)
    for cx, cy, r in spec["dots"]:
        px, py = map_pt(cx, cy)
        dot = sg.Point(px, py).buffer(r * scale, resolution=16)
        if not dot.is_empty:
            geoms.append(dot)
    return so.unary_union(geoms).buffer(0)

def extrude_shapely(geom, z_bottom, z_top):
    height = z_top - z_bottom
    polys = [geom] if isinstance(geom, sg.Polygon) else [
        g for g in getattr(geom, "geoms", []) if isinstance(g, sg.Polygon) and g.area > 1e-4
    ]
    meshes = []
    for poly in polys:
        m = trimesh.creation.extrude_polygon(poly, height=height)
        m.apply_translation([0.0, 0.0, z_bottom])
        meshes.append(m)
    return meshes[0] if len(meshes) == 1 else trimesh.boolean.union(meshes, engine='manifold')

if __name__ == "__main__":
    emb_base = create_base_cap_mesh(EMB_BASE_HEIGHT)
    eng_base = create_base_cap_mesh(ENG_BASE_HEIGHT)
    emb_plate_meshes, eng_plate_meshes = [], []

    for i, (bird_id, spec) in enumerate(BIRDS_LOGO_SPEC.items()):
        geom_2d = svg_to_shapely_geometry(spec)
        relief = extrude_shapely(geom_2d, EMB_BASE_HEIGHT - 0.15, EMB_BASE_HEIGHT + EMB_RELIEF_HEIGHT)
        emb_cap = trimesh.boolean.union([emb_base, relief], engine='manifold')
        emb_cap.fix_normals()
        emb_cap.export(os.path.join(EMB_DIR, "stl", f"{bird_id}_nfc_cap.stl"))
        emb_cap.export(os.path.join(EMB_DIR, "obj", f"{bird_id}_nfc_cap.obj"))

        cutter = extrude_shapely(geom_2d, ENG_BASE_HEIGHT - ENG_CARVE_DEPTH, ENG_BASE_HEIGHT + 0.5)
        eng_cap = trimesh.boolean.difference([eng_base, cutter], engine='manifold')
        eng_cap.fix_normals()
        eng_cap.export(os.path.join(ENG_DIR, "stl", f"{bird_id}_nfc_cap_engraved.stl"))
        eng_cap.export(os.path.join(ENG_DIR, "obj", f"{bird_id}_nfc_cap_engraved.obj"))

        print(f"[{i+1}/9] {bird_id}: emb_watertight={emb_cap.is_watertight}, eng_watertight={eng_cap.is_watertight}")
        col, row = i % 3, i // 3
        for m, lst in ((emb_cap, emb_plate_meshes), (eng_cap, eng_plate_meshes)):
            mc = m.copy()
            mc.apply_translation([(col - 1) * 37.0, (1 - row) * 37.0, 0.0])
            lst.append(mc)

    trimesh.util.concatenate(emb_plate_meshes).export(os.path.join(EMB_DIR, "all_9_caps_embossed_plate.stl"))
    trimesh.util.concatenate(emb_plate_meshes).export(os.path.join(EMB_DIR, "all_9_caps_embossed_plate.3mf"))
    trimesh.util.concatenate(eng_plate_meshes).export(os.path.join(ENG_DIR, "all_9_caps_engraved_plate.stl"))
    trimesh.util.concatenate(eng_plate_meshes).export(os.path.join(ENG_DIR, "all_9_caps_engraved_plate.3mf"))
    print("All embossed & engraved caps exported cleanly.")
