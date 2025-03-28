import subprocess
import os
import shutil

def build_target(script_name, output_dir, no_console=False):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dist_path = os.path.join(current_dir, output_dir)

    os.makedirs(dist_path, exist_ok=True)

    base_cmd = [
        "pyinstaller",
        "--onefile",
        "--distpath", dist_path,
        script_name
    ]
    if no_console:
        base_cmd.insert(1, "--noconsole")

    try:
        print(f"Building: {script_name} (no_console={no_console})")
        subprocess.run(base_cmd, check=True)
        print(f"Executable for {script_name} built in: {dist_path}")
    except subprocess.CalledProcessError:
        print(f"Error building {script_name}")
        return

def build_exe():
    build_dir = "bin"
    build_target("window_mover.py", build_dir, no_console=False)
    build_target("gui.py", build_dir, no_console=True)

    # Remove the intermediate build folder
    intermediate_build = os.path.join(os.getcwd(), "build")
    if os.path.exists(intermediate_build) and intermediate_build != os.path.abspath(build_dir):
        shutil.rmtree(intermediate_build)
        print("Intermediate build folder deleted.")

    # Remove spec files
    for spec in ["window_mover.spec", "gui.spec"]:
        if os.path.exists(spec):
            os.remove(spec)
            print(f"Spec file {spec} deleted.")

if __name__ == "__main__":
    build_exe()
