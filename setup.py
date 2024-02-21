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
        os.makedirs(self.build_temp, exist_ok=True)
        for i, c_file in enumerate(ext.sources):
            c_file = os.path.join(self.build_temp, os.path.basename(c_file))
            ext.sources[i] = c_file
            cmd = [sys.executable, build_script, c_file, '0']
            subprocess.run(cmd, shell=False, check=True)  # noqa S603

        logging.info(f'Extension build: {ext.__dict__}')

        super().build_extension(ext)


def main():
    package_name = 'libsecp256k1_py_bindings'
    secp256k1_package = 'libsecp256k1'

    libname = f'{package_name}._{secp256k1_package}'

    extension = Extension(
        name=libname,
        sources=[f'_{secp256k1_package}.c'],
        extra_compile_args=['/d2FH4-'] if sys.platform == 'win32' else [],
        # API mode is preferred to ABI: https://cffi.readthedocs.io/en/stable/overview.html#abi-versus-api
        py_limited_api=False,
    )

    logging.info(f'Extension build: {extension.__dict__}')

    pkgconfig.configure_extension(extension, secp256k1_package, static=False)

    if platform.system() == 'Windows':
        # Apparently, the linker on Windows interprets -lxxx as xxx.lib, not libxxx.lib
        for i, v in enumerate(extension.__dict__.get('extra_link_args')):
            if v.endswith('.lib'):
                extension.__dict__['extra_link_args'][i] = f'lib{v}'

    setup(
        ext_modules=[extension],
        cmdclass={'build_ext': BuildCFFI,},
        package_data={package_name: ['py.typed',]},

        package_dir={f'{package_name}': f'src/{package_name}'},
    )


if __name__ == '__main__':
    main()
