from calculator import calculation
import pytest

def test_calculation():
    assert calculation(93) == 4.0
    assert calculation(91) == 3.7
    assert calculation(89) == 3.3
    assert calculation(83) == 3.0
    assert calculation(82) == 2.7
    assert calculation(79) == 2.3
    assert calculation(74) == 2.0
    assert calculation(72) == 1.7
    assert calculation(69) == 1.3
    assert calculation(64) == 1.0
    assert calculation(61) == 0.7
    assert calculation(55) == 0

def test_calculation_TypeError():
    with pytest.raises(TypeError):
        calculation('string')

def test_calculation_ValueError():
    with pytest.raises(ValueError):
        calculation(-10)