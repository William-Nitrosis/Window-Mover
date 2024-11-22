import subprocess
import os
import shutil

def build_exe():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        # Run the pyinstaller command with --noconsole and --distpath options
        subprocess.run(
            #["pyinstaller", "--onefile", "--noconsole", "--distpath", current_dir, "window_mover.py"],
            ["pyinstaller", "--onefile", "--distpath", current_dir, "window_mover.py"],
            check=True
        )
        print("Executable built successfully in:", current_dir)
        
        # Remove the build directory
        build_dir = os.path.join(current_dir, "build")
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
            print("Build folder deleted.")
        
        # Remove the .spec file
        spec_file = os.path.join(current_dir, "window_mover.spec")
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print("Spec file deleted.")
    except subprocess.CalledProcessError:
        print("An error occurred during the build process.")

if __name__ == "__main__":
    build_exe()
