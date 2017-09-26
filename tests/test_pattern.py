from hypothesis import given
from hypothesis.strategies import (
    composite, sampled_from, integers, lists)
from splife.pattern import Pattern

@composite
def st_pattern(draw):
    m = draw(integers(min_value=0, max_value=10))
    n = draw(integers(min_value=0, max_value=10))
    return Pattern.from_list(
        [draw(lists(sampled_from([0, 1]), min_size=m, max_size=m))
            for _ in range(n)])


@given(pattern=st_pattern())
def test_list_roundtrips(pattern):
    assert Pattern.from_list(pattern.as_list()) == pattern

@given(pattern=st_pattern())
def test_txt_roundtrips(pattern):
    assert Pattern.from_txt(pattern.as_txt()) == pattern

