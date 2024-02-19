import logging
import os
import platform
import subprocess
import sys

import pkgconfig
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

logging.basicConfig(level=logging.INFO)


class BuildCFFI(build_ext):
    def build_extension(self, ext):
        build_script = os.path.join('_cffi_build', 'build.py')
        for c_file in ext.sources:
            cmd = [sys.executable, build_script, c_file, '0']
            subprocess.run([cmd], shell=False, check=True)  # noqa S603

        super().build_extension(ext)


# --- Coincurve package definitions ---
package_name = 'libsecp256k1_py_bindings'

# --- SECP256K1 package definitions ---
secp256k1_package = 'libsecp256k1'

libname = f'{package_name}._{secp256k1_package}'

extension = Extension(
    name=libname,
    sources=[os.path.join('src', package_name, f'_{secp256k1_package}.c')],
    extra_compile_args=['/d2FH4-'] if sys.platform == 'win32' else []
    # API mode is preferred to ABI: https://cffi.readthedocs.io/en/stable/overview.html#abi-versus-api
    # py_limited_api=True,
)

pkgconfig.configure_extension(extension, secp256k1_package, static=False)

if platform.system() == 'Windows':
    # Apparently, the linker on Windows interprets -lxxx as xxx.lib, not libxxx.lib
    for i, v in enumerate(extension.__dict__.get('extra_link_args')):
        if v.endswith('.lib'):
            extension.__dict__['extra_link_args'][i] = f'lib{v}'

setup(
    ext_modules=[extension],
    cmdclass={'build_ext': BuildCFFI},
    package_data={package_name: ['py.typed']},
    package_dir={f'{package_name}': f'src/{package_name}'},
)
