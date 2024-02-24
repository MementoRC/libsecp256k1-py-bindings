import logging
import os
import shutil
import subprocess
import sys
import tempfile

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

logging.basicConfig(level=logging.INFO)


def execute_command_with_temp_log(cmd, *, debug=False, capture_output=False, **kwargs):
    with tempfile.NamedTemporaryFile(mode='w+') as temp_log:
        try:
            if capture_output:
                ret = subprocess.check_output(cmd, stderr=temp_log, **kwargs)  # noqa S603
            else:
                subprocess.check_call(cmd, stdout=temp_log, stderr=temp_log, **kwargs)  # noqa S603

            if debug:
                temp_log.seek(0)
                log_contents = temp_log.read()
                logging.info(f'Command log:\n{log_contents}')

            if capture_output:
                return ret.rstrip().decode()

        except subprocess.CalledProcessError as e:
            logging.error(f'An error occurred during the command execution: {e}')
            temp_log.seek(0)
            log_contents = temp_log.read()
            logging.error(f'Command log:\n{log_contents}')
            raise e


def _parse_pkginfo(definitions, msvc=False):
    import re

    inc, lib = [], []
    definitions.replace('\\"', '')
    for arg in re.split(r'(?<!\\) ', definitions):
        if arg.startswith('-I'):
            inc.append(arg)
        elif arg.startswith('-L'):
            lib.append(f'/libpath:{arg[2:]}' if msvc else arg)
        elif arg.startswith('-l'):
            # SECP256K1 should have both libsecp256k1.lib abd secp256k1.lib
            lib.append(f'{arg[2:]}.lib' if msvc else arg)
    return inc, lib


class BuildCFFI(build_ext):
    def build_extension(self, ext):
        build_script = os.path.join('_cffi_build', 'build.py')
        os.makedirs(self.build_temp, exist_ok=True)
        for i, c_file in enumerate(ext.sources):
            c_file = os.path.join(self.build_temp, os.path.basename(c_file))
            ext.sources[i] = c_file
            cmd = [sys.executable, build_script, c_file, '0']
            subprocess.run(cmd, shell=False, check=True)  # noqa S603

        pkgconfig = shutil.which('pkg-config')

        logging.info(f'DBG - PKG_CONFIG_PATH: {os.getenv("PKG_CONFIG_PATH")}')
        logging.info(f'DBG - CONDA_PREFIX: {os.getenv("CONDA_PREFIX")}:')

        pkg_cmd = [pkgconfig, '--cflags', '--libs', '--dont-define-prefix', SECP256K1_PKG]
        lib_def = execute_command_with_temp_log(pkg_cmd, capture_output=True)
        inc, lib = _parse_pkginfo(lib_def, self.compiler.compiler_type == 'msvc')

        ext.extra_compile_args.extend(inc)
        ext.extra_link_args.extend(lib)

        super().build_extension(ext)


SECP256K1_PKG = 'libsecp256k1'


def main():
    package_name = 'libsecp256k1_py_bindings'

    libname = f'{package_name}._{SECP256K1_PKG}'

    extension = Extension(
        name=libname,
        sources=[f'_{SECP256K1_PKG}.c'],
        extra_compile_args=['/d2FH4-'] if sys.platform == 'win32' else [],
        # API mode is preferred to ABI: https://cffi.readthedocs.io/en/stable/overview.html#abi-versus-api
        py_limited_api=False,
    )

    setup(
        ext_modules=[extension],
        cmdclass={'build_ext': BuildCFFI, },
        package_data={package_name: ['py.typed', ]},
        package_dir={f'{package_name}': f'src/{package_name}'},
    )


if __name__ == '__main__':
    main()
