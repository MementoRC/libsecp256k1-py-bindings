from libsecp256k1_py_bindings.ecdsa import cdata_to_der, der_to_cdata
import pytest


def test_der(samples):
    assert cdata_to_der(der_to_cdata(samples.get('SIGNATURE'))) == samples.get('SIGNATURE')


if __name__ == '__main__':
    import pytest

    pytest.main(['-s', __file__])
