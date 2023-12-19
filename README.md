# libsecp256k1 (coincurve)

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/MementoRC/libsecp256k1-py-boindings/actions/workflows/build.yml/badge.svg)](https://github.com/MementoRC/libsecp256k1-py-boindings/actions/workflows/build.yml) [![CI - Coverage](https://img.shields.io/codecov/c/github/MementoRC/libsecp256k1-py-boindings/master.svg?logo=codecov&logoColor=red)](https://codecov.io/github/ofek/coincurve) |
| Meta | [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black) [![imports - isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/pycqa/isort) [![License - MIT OR Apache-2.0](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-9400d3.svg)](https://spdx.org/licenses/) [![GitHub Sponsors](https://img.shields.io/github/sponsors/ofek?logo=GitHub%20Sponsors&style=social)](https://github.com/sponsors/ofek) |

-----

This library provides well-tested Python bindings for [libsecp256k1](https://github.com/bitcoin-core/secp256k1), the heavily optimized C library
used by [Bitcoin Core](https://github.com/bitcoin/bitcoin) for operations on the elliptic curve [secp256k1](https://en.bitcoin.it/wiki/Secp256k1).

It is a simple streamlining of the `coincurve` library provided by https://ofek.dev/coincurve/ that de-embeds the build process of the secp256k1 C library
This is primarily in order to provide a clean conda-forge recipe for both the `secp256k1` and its python bindings

Feel free to read the Coincurve [documentation](https://ofek.dev/coincurve/)!

## Users

- [Ethereum](https://ethereum.org)
- [LBRY](https://lbry.com)
- [libp2p](https://libp2p.io)

and [many more](https://ofek.dev/coincurve/users/)!

## License

`libsecp256k1` (`coincurve`) is distributed under the terms of any of the following licenses:

- [MIT](https://spdx.org/licenses/MIT.html)
- [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html)
