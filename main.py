import subprocess
import glob

# === CONFIGURATION ===

# Full path to Blender executable
blender_executable = "/usr/bin/blender"

base_path = "/home/klingenberg/Documents/conferences/efdc2025/video_contest/efdc2_video/"
# Full path to your .blend file
blend_file = base_path + "Empty1.blend"

# Path to the script that will run *inside* Blender
render_script = base_path +  "blender_script.py"

# STL file paths
stl_paths = glob.glob("./data/plot_isosurfaces_velocity_x_t_*.stl")
# stl_paths = glob.glob("./*000050.stl")

# Output render image path
output_path = lambda x, y: base_path + "plots/plot_isosurfaces_velocity_x_t_" + "{:06}".format(x) + "_" + "{:01}".format(y) + ".png"

newpaths = ["./plots", "./img"]
for newpath in newpaths:
    if not os.path.exists(newpath):
        os.makedirs(newpath)


# === BUILD ARGUMENT LIST ===
N = len(stl_paths)
n_substeps = 3
# n_substeps = 1
for i in range(1, N):
# for i in [N-1]:
    print("Doing image", i + 1, "out of", N)
    for j in range(n_substeps):
        print("substep", j + 1, "out of", n_substeps)
        progress = (i * n_substeps + j) / (n_substeps * N)
        args = [
            blender_executable,
            blend_file,
            "--background",             # Run in background (no UI)
            "--python", render_script, # Python script to run inside Blender
            "--",                       # Signals the end of Blender args and start of custom args
            base_path + "data/" + stl_paths[i][2:],
            output_path(i, j),
            str(progress)
        ]

        # === RUN BLENDER ===
        subprocess.run(args)
