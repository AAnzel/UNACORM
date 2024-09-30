from subprocess import run
from venv import create
import os


def create_norec_env(current_path):
    venv_dir = os.path.join(current_path, "NOREC4DNA", "venv")
    create(venv_dir, with_pip=True)


def install_norec_packages(current_path):
    run([os.path.join(current_path, "NOREC4DNA", "venv", "bin", "pip"),
         "install", "wheel"],
        cwd=os.path.join(current_path, "NOREC4DNA"))
    run([os.path.join(current_path, "NOREC4DNA", "venv", "bin", "pip"),
         "install", "-r",
         os.path.join(current_path, "NOREC_requirements.txt")],
        cwd=os.path.join(current_path, "NOREC4DNA"))


def compile_dna_aeon(current_path):
    run(["cmake", current_path])
    run(["cmake", "--build", current_path]) 


if __name__ == "__main__":
    cpath = os.path.dirname(os.path.realpath(__file__))
    #print('Current_Path:\t', cpath, '\n')
    #print("Setting up NOREC4DNA virtual environment.")
    #create_norec_env(cpath)
    #print("Installing packages required for NOREC4DNA.")
    #install_norec_packages(cpath)
    print("Compiling DNA Aeon")
    compile_dna_aeon(cpath)
    print("Installation finished!")
