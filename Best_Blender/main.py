# Purpose : It reads 4 different stl files, it renders the image and prints the
#           resultant figure in HQ. Needs of a GPU!
# Author  : Daniel Morón Montesdeoca, Dario Klingenberg & ChatGPT :)
# Date    : 29/07/2025

import subprocess
import os
import time

# ======= START THE TIMER =======
start_time = time.time()

# === CONFIGURATION ===
# Full path to Blender executable
blender_executable = r"C:\Program Files\Blender Foundation\Blender 3.4\blender.exe"
# Full path to your .blend file
blend_file = r"C:\Users\damom\Documents\1A_ZARM\ADaysWork\Blender_Pipe\Best_Blender\Empty.blend"
# Path to the script that will run *inside* Blender
render_script = r"C:\Users\damom\Documents\1A_ZARM\ADaysWork\Blender_Pipe\Best_Blender\TwoStlBlend.py"
# Create the folder where to save
folder_path = r"D:\Video_Future_Puffs\Pred_59\Vd_Blnd"
os.makedirs(folder_path, exist_ok=True)

# === CAMERA! ===
x1=7;     y1=-7; z1=3;     # location 1
a1=66.9;  b1=0;  c1=30;    # angle    1
x2=1;     y2=-9; z2=0;     # location 2
a2=90;    b2=0;  c2=0;     # angle    2
frm0= 700;                 # Initial frame to move the camera
frmf= 1200;                # Final   frame to move the camera

# === LOOP ON FILES =====
for i in range(1,1251,100):
    folder_name = f"Step_{i:04d}"
    stl_path_1 = fr"D:\Video_Future_Puffs\Pred_59\Vd\S\{folder_name}\FS.stl"
    stl_path_2 = fr"D:\Video_Future_Puffs\Pred_59\Vd\S\{folder_name}\FQ.stl"
    stl_path_3 = fr"D:\Video_Future_Puffs\Pred_59\Vd_6\S\{folder_name}\FS.stl"
    stl_path_4 = fr"D:\Video_Future_Puffs\Pred_59\Vd_6\S\{folder_name}\FQ.stl"
    # Output render image path
    file_name=f"figure_{i:04d}.png"
    output_path = os.path.join(folder_path,file_name)
    # Camera position
    cn=float(i-frm0)/float(frmf-frm0);    cn=max(min(cn,1),0)
    cmr_loc=((1-cn)*x1+cn*x2,(1-cn)*y1+cn*y2,(1-cn)*z1+cn*z2)
    cmr_ang=((1-cn)*a1+cn*a2,(1-cn)*b1+cn*b2,(1-cn)*c1+cn*c2)
    # === BUILD ARGUMENT LIST ===
    args = [
        blender_executable,
        blend_file,
        "--background",             # Run in background (no UI)
        "--python", render_script, # Python script to run inside Blender
        "--",                       # Signals the end of Blender args and start of custom args
        stl_path_1,
        stl_path_2,
        stl_path_3,
        stl_path_4,
        str(cmr_loc[0]), str(cmr_loc[1]), str(cmr_loc[2]),
        str(cmr_ang[0]), str(cmr_ang[1]), str(cmr_ang[2]),
        output_path
        ]
    # === RUN BLENDER ===
    subprocess.run(args,check=True)
    print('Finished step:','{:04d}'.format(i))
    end_time = time.time(); elapsed = end_time-start_time
    print(f"⏱️ Task completed in {elapsed:.2f} seconds")







