import bpy
import os

"""
This code allows to import folder filled with .fbx animations and merge them into one .glb file that can be imported in Godot
- Find and import all .fbx files in folder
- Leave only one Armature with mesh and remove other scene elements
- Attach all animation slots to this one Armature
- Export .glb file with skeleton, mesh, animations

Then you can import this file into Godot and use these animations as AnimationLib
"""

### CONFIGURATION
# 1. Path to folder with .fbx files
IMPORT_FOLDER_PATH = r"L:\anim"

# 2. Full path for export location
EXPORT_FILE_PATH = r"L:\anim\exported_character.glb"


def process_fbx_animations(folder_path, target_armature_name="Armature"):
    """
    Correct slots in all animations to use the same Armature name
    """

    if not os.path.exists(folder_path):
        print(f"Error: Provided folder '{folder_path}' does not exist.")
        return False

    fbx_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.fbx')]
    
    if not fbx_files:
        print(f"No .fbx files in folder: {folder_path}")
        return False
        
    print(f"Found {len(fbx_files)} FBX files. Importing...")

    for file in fbx_files:
        filepath = os.path.join(folder_path, file)
        base_name = os.path.splitext(file)[0]
        
        existing_actions = set(bpy.data.actions)
        
        # Import
        bpy.ops.import_scene.fbx(filepath=filepath)
        
        # Set name for animation the same as file name
        new_actions = set(bpy.data.actions) - existing_actions
        for action in new_actions:
            action.name = base_name
            print(f"Imported: {action.name}")

    # Find main armature
    main_armature = None
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE':
            main_armature = obj
            break
            
    if not main_armature:
        print("Error: No skeleton in imported assets")
        return False

    main_armature.name = target_armature_name

    # Find mesh in main armature
    main_mesh = None
    for child in main_armature.children:
        if child.type == 'MESH':
            main_mesh = child
            break
            
    if not main_mesh:
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                main_mesh = obj
                break

    # Clean up scene
    objects_to_delete = []
    for obj in bpy.data.objects:
        if obj != main_armature and obj != main_mesh:
            objects_to_delete.append(obj)

    deleted_count = len(objects_to_delete)
    for obj in objects_to_delete:
        if bpy.data.objects.get(obj.name):
            bpy.data.objects.remove(obj, do_unlink=True)
            
    print(f"Cleaning up: Removed {deleted_count} objects.")

    # Attach animations to main armature
    updated_count = 0
    for action in bpy.data.actions:
        if hasattr(action, 'slots'):
            for slot in action.slots:
                if slot.target_id_type == 'OBJECT' and slot.identifier != target_armature_name:
                    old_name = slot.identifier
                    slot.identifier = target_armature_name
                    print(f"[{action.name}] Attached slot: {old_name} -> {slot.identifier}")
                    updated_count += 1
                    
    print(f"Attached {updated_count} animations to '{target_armature_name}'.")
    return True


def export_armature_to_gltf(export_filepath, target_armature_name="Armature"):
    """
    Export armature with mesh and animation lib to .glb format
    """

    export_dir = os.path.dirname(export_filepath)
    if export_dir and not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)

    bpy.ops.object.select_all(action='DESELECT')

    target_armature = bpy.data.objects.get(target_armature_name)
    if not target_armature:
        print(f"Error: No object found for export: '{target_armature_name}'.")
        return

    target_armature.select_set(True)
    bpy.context.view_layer.objects.active = target_armature

    for child in target_armature.children:
        if child.type == 'MESH':
            child.select_set(True)

    # Rozpoznajemy format na podstawie rozszerzenia pliku (.glb lub .gltf)
    ext = os.path.splitext(export_filepath)[1].lower()
    export_format = 'GLB' if ext == '.glb' else 'GLTF_EMBEDDED'

    print(f"Exporting {export_format}: {export_filepath}")

    # Export to glTF / GLB
    bpy.ops.export_scene.gltf(
        filepath=export_filepath,
        export_format=export_format,
        use_selection=True,
        export_animations=True,
        export_animation_mode='ACTIONS'
    )

    print(f"Exported .glb file: {export_filepath}")

### Execution

if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

if process_fbx_animations(IMPORT_FOLDER_PATH, "Armature"):
    export_armature_to_gltf(EXPORT_FILE_PATH, "Armature")