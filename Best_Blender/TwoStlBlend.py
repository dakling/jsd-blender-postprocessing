import bpy
import sys
import math
import os

# === READ ARGUMENTS FROM COMMAND LINE ===
# Blender adds its own args; we take everything after "--"
argv = sys.argv
argv = argv[argv.index("--") + 1:]
if len(argv) != 11:
    raise Exception("Expected 11 arguments: stl1, stl2,stl3,stl4,loc,rot, output_image")
# Extract the inputs
stl_path_1=argv[0]
stl_path_2=argv[1]
stl_path_3=argv[2]
stl_path_4=argv[3]
location = tuple(float(argv[i]) for i in range(4,7))
rotation = tuple(float(argv[i]) for i in range(7,10))
rot_rad  = tuple(math.radians(r) for r in rotation)
output_path=argv[-1]
# Scale factors (custom per model)
scale_1 = (0.5,0.5,0.5)
# Materials (must already exist in the .blend file)
material_1_name = "Material.001"
material_2_name = "Material.002"
material_3_name = "Material.003"
material_4_name = "Material.005"

# === FUNCTION TO IMPORT, SCALE AND ASSIGN MATERIAL ===
def import_and_prepare_stl(filepath, scale, material_name, object_name=None):
    if not os.path.exists(filepath):
        print(f"⚠️ Skipping: File not found - {filepath}")
        return None  # Skip this object
    # Import
    bpy.ops.import_mesh.stl(filepath=filepath)
    imported_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    if not imported_objs:
        raise Exception(f"Failed to import mesh from {filepath}")
    obj = imported_objs[0]
    if object_name:
        obj.name = object_name
    # Scale the object
    obj.scale = scale
    obj.location = (-25,0,0)
    obj.rotation_euler = (0,math.radians(90),0)
    # Assign material
    material = bpy.data.materials.get(material_name)
    if not material:
        raise Exception(f"Material '{material_name}' not found in .blend file")
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
    return obj

# === IMPORT BOTH STL FILES ===
obj1 = import_and_prepare_stl(stl_path_1, scale_1, material_1_name, object_name="STL_1")
obj2 = import_and_prepare_stl(stl_path_2, scale_1, material_2_name, object_name="STL_2")
obj3 = import_and_prepare_stl(stl_path_3, scale_1, material_3_name, object_name="STL_3")
obj4 = import_and_prepare_stl(stl_path_4, scale_1, material_4_name, object_name="STL_4")

# === Apply Camera Transform ===
camera = bpy.data.objects.get("Camera")
if not camera:
    raise Exception("Camera not found in scene (must be named 'Camera')")
camera.location = location
camera.rotation_euler = rot_rad

# === RENDER SETTINGS ===
scene = bpy.context.scene
# Use Cycles
scene.render.engine = 'CYCLES'
# Set render quality
scene.cycles.samples = 256  # Try 256 or 512 for better quality
scene.cycles.use_denoising = True
scene.cycles.use_adaptive_sampling = True  # Optional: reduces overkill in flat areas
scene.cycles.device = 'GPU'  # Optional: if you have GPU enabled
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 80
scene.render.image_settings.file_format = 'PNG'

# === Set output path ===
scene.render.filepath = output_path

# === Perform rendering ===
bpy.ops.render.render(write_still=True)
print("✅ Render complete!")

