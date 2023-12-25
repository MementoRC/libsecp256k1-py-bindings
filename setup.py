import logging
import os
import shutil

import pkgconfig
import subprocess
import sys

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

logging.basicConfig(level=logging.INFO)


class BuildCFFI(build_ext):
    def build_extensions(self):
        build_script = os.path.join('_cffi_build', 'build.py')
        c_file = self.extensions[0].sources[0]
        python_exe = shutil.which('python', path=os.environ['PATH'])
        subprocess.run([python_exe, build_script, c_file, '0'], shell=False, check=True)  # noqa S603
        super().build_extensions()

# --- Coincurve package definitions ---
package_name = 'libsecp256k1_py_bindings'
libname = f'{package_name}._libsecp256k1'

package_data = {package_name: ['py.typed']}

# --- SECP256K1 package definitions ---
secp256k1_package = 'libsecp256k1'

extension = Extension(
    name=libname,
    sources=[os.path.join(package_name, '_libsecp256k1.c')],
    # API mode is preferred to ABI: https://cffi.readthedocs.io/en/stable/overview.html#abi-versus-api
    # py_limited_api=True,
)

pkgconfig.configure_extension(extension, secp256k1_package, static=False)
package_info = pkgconfig.parse(secp256k1_package, static=False)

if os.name == 'nt' or sys.platform == 'win32':
    # Apparently, the linker on Windows interprets -lxxx as xxx.lib, not libxxx.lib
    for i, v in enumerate(extension.__dict__.get('extra_link_args')):
        if v.endswith('.lib'):
            extension.__dict__['extra_link_args'][i] = f'lib{v}'

setup(
    ext_modules=[extension],
    cmdclass={'build_ext': BuildCFFI},
    package_data=package_data,
)
