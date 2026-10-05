# Blender Scripts – Automation Tools for Game Engines

![Blender](https://img.shields.io/badge/blender-5.0%2B-orange.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Godot](https://img.shields.io/badge/godot-ready-478CBF.svg)

A growing collection of lightweight Blender Python scripts designed to automate repetitive workflows, speed up your 3D pipeline, and prepare production-ready assets for game engines like Godot, Unity, and Unreal.

## 🧰 Available Scripts

* [Mixamo Batch to GLB](#-mixamo-batch-to-glb) — Batch import `.fbx` animations, merge them onto a single skeleton, and export as a single `.glb` file.

---

## 📂 Script Details

### 1. Mixamo Batch to GLB (`mixamo_batch_to_glb.py`)
This script automates the tedious process of importing multiple `.fbx` animation files (e.g., from Mixamo), merging them into a single character rig, and exporting the result as a `.glb` file containing a full Animation Library.

#### ✨ Features
* **Batch Processing:** Automatically finds and imports all `.fbx` files from a specified directory in a single run.
* **Smart Scene Cleanup:** Keeps only one main Armature and its associated Mesh. Automatically deletes duplicate skeletons, orphaned meshes (like Mixamo's default `Aria Mesh`), and other clutter.
* **Blender 5.0+ Compatibility:** Fully supports the new Animation Action Slot system, ensuring all imported animations are correctly linked to your main target armature without `(unassigned)` track errors.
* **Game Engine Ready:** Exports a single, clean `.glb` file containing the mesh, skeleton, and the entire library of animations. Perfect for importing directly into Godot as an `AnimationLib`.

#### ⚙️ Configuration
Before running the script, update your input and output paths at the top of the `mixamo_batch_to_glb.py` file:

```python
### CONFIGURATION
# 1. Path to folder with .fbx files
IMPORT_FOLDER_PATH = r"L:\anim"

# 2. Full path for export location (.glb)
EXPORT_FILE_PATH = r"L:\anim\exported_character.glb"