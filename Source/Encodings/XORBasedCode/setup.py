import os
import subprocess
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name):
        Extension.__init__(self, name, sources=[])


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        config = 'debug' if self.debug else 'release'

        python_path = sys.executable
        project_dir = os.path.abspath('')
        lib_dir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        build_dir = os.path.join(self.build_temp, ext.name)
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        cmake_args = [
            f'-DCMAKE_BUILD_TYPE={config}',
            f'-DPYTHON_EXECUTABLE={python_path}',
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={lib_dir}'
        ]
        build_args = []

        if self.compiler.compiler_type == 'unix':  # use Ninja on unix systems
            import ninja

            ninja_path = os.path.join(ninja.BIN_DIR, 'ninja')
            cmake_args += [
                '-GNinja',
                f'-DCMAKE_MAKE_PROGRAM:FILEPATH={ninja_path}'
            ]

        else:
            cmake_args += [f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{config.upper()}={lib_dir}']
            build_args += ['--config', config]

        subprocess.check_call(['cmake', project_dir] + cmake_args, cwd=build_dir)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=build_dir)


setup(
    name='xor_code_python',
    version='1.0.0',
    author='Luca Staus, Leon Wimbes',
    description='Python bindings for the implementation of the xor based DNA Encoding created by Bornholt et al.',
    ext_modules=[CMakeExtension('xor_code_python')],
    cmdclass={'build_ext': CMakeBuild},
    zip_safe=False
)
