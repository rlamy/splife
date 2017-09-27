from hypothesis import given
from hypothesis.strategies import (
    composite, sampled_from, integers, lists)
from splife.pattern import Pattern, successor

@composite
def st_pattern(draw):
    m = draw(integers(min_value=1, max_value=10))
    n = draw(integers(min_value=1, max_value=10))
    return Pattern.from_list(
        [draw(lists(sampled_from([0, 1]), min_size=m, max_size=m))
            for _ in range(n)])


@given(pattern=st_pattern())
def test_list_roundtrips(pattern):
    assert Pattern.from_list(pattern.as_list()) == pattern

@given(pattern=st_pattern())
def test_txt_roundtrips(pattern):
    assert Pattern.from_txt(pattern.as_txt()) == pattern

def test_succ():
    block = Pattern.from_list([[1, 1], [1, 1]])
    s = successor(block)
    assert s is not block
    assert s == block

@given(pattern=st_pattern())
def test_canonical(pattern):
    pattern.canonicalize()
    s1 = pattern.as_txt()
    pattern.canonicalize()
    s2 = pattern.as_txt()
    assert s1 == s2
