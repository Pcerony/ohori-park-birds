# -*- coding: utf-8 -*-
"""
生成备选平底封底件（外包托盘、等径齐平底盖、内嵌超薄塞片）。
输出位置：../models/legacy_bases/
"""
import os
import numpy as np
import trimesh

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HW_DIR = os.path.dirname(SCRIPT_DIR)
BASES_DIR = os.path.join(HW_DIR, "models", "legacy_bases")
os.makedirs(os.path.join(BASES_DIR, "stl"), exist_ok=True)
os.makedirs(os.path.join(BASES_DIR, "obj"), exist_ok=True)

def build_tray_base():
    profile = np.array([
        [0.0, 0.0], [16.7, 0.0], [17.1, 0.4], [17.1, 2.4], [16.8, 2.7],
        [15.9, 2.7], [15.65, 2.45], [15.65, 1.2], [0.0, 1.2]
    ])
    m = trimesh.creation.revolve(profile, sections=128)
    m.fix_normals()
    return m

def build_flush_base():
    profile = np.array([
        [0.0, 0.0], [15.2, 0.0], [15.5, 0.3], [15.5, 1.2],
        [13.0, 1.2], [13.0, 1.45], [12.85, 1.6], [0.0, 1.6]
    ])
    m = trimesh.creation.revolve(profile, sections=128)
    m.fix_normals()
    return m

def build_inner_plug():
    profile = np.array([
        [0.0, 0.0], [12.85, 0.0], [13.0, 0.15], [13.0, 0.65], [12.85, 0.8], [0.0, 0.8]
    ])
    m = trimesh.creation.revolve(profile, sections=128)
    m.fix_normals()
    return m

if __name__ == "__main__":
    for name, fn in [("nfc_base_tray", build_tray_base), ("nfc_base_flush", build_flush_base), ("nfc_base_plug", build_inner_plug)]:
        m = fn()
        m.export(os.path.join(BASES_DIR, "stl", f"{name}.stl"))
        m.export(os.path.join(BASES_DIR, "obj", f"{name}.obj"))
        print(f"Exported {name}: watertight={m.is_watertight}")
