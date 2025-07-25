import bpy
import sys
import math

# === READ ARGUMENTS FROM COMMAND LINE ===
# Blender adds its own args; we take everything after "--"
argv = sys.argv
argv = argv[argv.index("--") + 1:]
stl_path,output_path, progress = argv
progress = float(progress)
# Materials (must already exist in the .blend file)
material_1_name = "Material.001"
material_2_name = "Material.002"

# === STL OBJECT CONFIG ===
scale = (1.0, 1.0, 1.0)
location = (0.0, 0.19, 2.5)
rotation = (math.radians(90), math.radians(0), math.radians(0))

# === CAMERA CONFIG ===
#camera_location = (5.0, -5.0, 5.0)  # Move camera to this position
#camera_rotation = (math.radians(60), 0, math.radians(45))  # Look down and rotate

# === FUNCTION TO IMPORT, SCALE AND ASSIGN MATERIAL ===
def import_and_prepare_stl(filepath, scale, location, rotation, material_name, object_name=None):
    # bpy.ops.import_mesh.stl(filepath=filepath)
    bpy.ops.wm.stl_import(filepath=filepath)
    imported_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    if not imported_objs:
        raise Exception(f"Failed to import mesh from {filepath}")
    obj = imported_objs[0]
    if object_name:
        obj.name = object_name
    obj.scale = scale
    obj.location = location
    obj.rotation_euler = rotation
    material = bpy.data.materials.get(material_name)
    if not material:
        raise Exception(f"Material '{material_name}' not found in .blend file")
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
    return obj

# === IMPORT BOTH STL FILES ===
obj = import_and_prepare_stl(stl_path, scale, location, rotation, material_1_name, object_name="STL_1")
wall_obj = import_and_prepare_stl("/home/klingenberg/Documents/conferences/efdc2025/video_contest/efdc2_video/walls.stl", scale, location, rotation, material_2_name, object_name="STL_2")

# === CAMERA SETTINGS ===
camera_location_0 = (5.0, -5.0, 3.0)
camera_rotation_0 = (math.radians(77), math.radians(0), math.radians(45))
lens_0 = 22.0
camera_location_1 = (7.0, -4.5, 4.0)
camera_rotation_1 = (math.radians(77), math.radians(0), math.radians(60))
lens_1 = 28.0
def get_camera_loc_and_rot():
    def interpolate(pos_0, pos_1):
        return (1 - progress) * pos_0 + progress * pos_1
    def interpolate_tuple(pos_0, pos_1):
        return tuple(interpolate(pos_0[i], pos_1[i]) for i in range(len(pos_0)))
    loc = interpolate_tuple(camera_location_0, camera_location_1)
    rot = interpolate_tuple(camera_rotation_0, camera_rotation_1)
    lens = interpolate(lens_0, lens_1)
    return loc, rot, lens
camera_location, camera_rotation, lens = get_camera_loc_and_rot()
print(camera_location)
camera = bpy.data.objects.get("Camera")
camera.location = camera_location
camera.rotation_euler = camera_rotation
bpy.data.cameras[0].lens = lens

# === RENDER SETTINGS ===
scene = bpy.context.scene
scene.render.resolution_x = 1000
scene.render.resolution_y = 750
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

# === Set output path ===
scene.render.filepath = output_path

# === Perform rendering ===
bpy.ops.render.render(write_still=True)
print("✅ Render complete!")



# :::::::::::::::::::::::::::::::::::::::::::::::
# OPTION TO MOVE THE STUFF AND ROTATE ELEMENTS
# :::::::::::::::::::::::::::::::::::::::::::::::
#import bpy
#import sys
#import os
#import math

# === READ COMMAND-LINE ARGUMENTS ===
#argv = sys.argv
#argv = argv[argv.index("--") + 1:]
#if len(argv) != 5:
#    raise Exception("Expected 5 arguments: stl1, mat1, stl2, mat2, output_image")
#stl_path_1, material_1_name, stl_path_2, material_2_name, output_path = argv

# === STL OBJECT CONFIG ===
# STL 1
#scale_1 = (1.0, 1.0, 1.0)
#location_1 = (2.0, 0.0, 0.0)
#rotation_1 = (0.0, 0.0, math.radians(45))  # Rotate 45° around Z
# STL 2
#scale_2 = (1.0, 1.0, 1.0)
#location_2 = (0.0, 0.0, 0.0)
#rotation_2 = (0.0, 0.0, 0.0)

# === CAMERA CONFIG ===
#camera_location = (5.0, -5.0, 5.0)  # Move camera to this position
#camera_rotation = (math.radians(60), 0, math.radians(45))  # Look down and rotate

# === FUNCTION TO IMPORT AND CONFIGURE STL ===
#def import_and_prepare_stl(filepath, scale, location, rotation, material_name, object_name=None):
#    bpy.ops.import_mesh.stl(filepath=filepath)
#    imported_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
#    if not imported_objs:
#        raise Exception(f"Failed to import mesh from {filepath}")
#    obj = imported_objs[0]
#    if object_name:
#        obj.name = object_name
#    obj.scale = scale
#    obj.location = location
#    obj.rotation_euler = rotation
#    material = bpy.data.materials.get(material_name)
#    if not material:
#        raise Exception(f"Material '{material_name}' not found in .blend file")
#    if obj.data.materials:
#        obj.data.materials[0] = material
#    else:
#        obj.data.materials.append(material)
#    return obj

# === IMPORT STL OBJECTS ===
#import_and_prepare_stl(stl_path_1, scale_1, location_1, rotation_1, material_1_name, object_name="STL_1")
#import_and_prepare_stl(stl_path_2, scale_2, location_2, rotation_2, material_2_name, object_name="STL_2")

# === SET CAMERA TRANSFORM ===
#camera = bpy.data.objects.get("Camera")
#if camera:
#    camera.location = camera_location
#    camera.rotation_euler = camera_rotation
#else:
#    raise Exception("Camera not found in scene. Make sure a camera named 'Camera' exists.")

# === RENDER === #








# :::::::::::::::::::::::::::::::::::::::::::::::::::
# OPTION TO IMPORT THE SCALARS OF LOCATION AND STUFF
# :::::::::::::::::::::::::::::::::::::::::::::::::::

#import bpy
#import sys
#import math

# === READ ARGS ===
#argv = sys.argv
#argv = argv[argv.index("--") + 1:]
#if len(argv) != 11:
#    raise Exception("Expected 11 arguments: stl, mat, x y z rx ry rz output")
#stl_path = argv[0]
#material_name = argv[1]
#location = tuple(float(argv[i]) for i in range(2, 5))
#rotation_deg = tuple(float(argv[i]) for i in range(5, 8))
#output_path = argv[8 + 2]
#
#rotation = tuple(math.radians(r) for r in rotation_deg)

# === IMPORT STL AND TRANSFORM ===
#def import_and_prepare_stl(filepath, scale, location, rotation, material_name, object_name=None):
#    bpy.ops.import_mesh.stl(filepath=filepath)
#    imported_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
#    if not imported_objs:
#        raise Exception(f"Failed to import mesh from {filepath}")
#    obj = imported_objs[0]
#    if object_name:
#        obj.name = object_name
#    obj.scale = scale
#    obj.location = location
#    obj.rotation_euler = rotation
#    mat = bpy.data.materials.get(material_name)
#    if not mat:
#        raise Exception(f"Material '{material_name}' not found")
#    if obj.data.materials:
#        obj.data.materials[0] = mat
#    else:
#        obj.data.materials.append(mat)
#    return obj

# Default scale
#scale = (1.0, 1.0, 1.0)

# Import and apply transformations
#import_and_prepare_stl(stl_path, scale, location, rotation, material_name, object_name="STL_1")
