from samples import SIGNATURE

from libsecp256k1_py_bindings.ecdsa import cdata_to_der, der_to_cdata


def test_der():
    assert cdata_to_der(der_to_cdata(SIGNATURE)) == SIGNATURE
