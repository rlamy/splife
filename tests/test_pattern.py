from hypothesis import given
from hypothesis.strategies import (
    composite, sampled_from, integers, lists)
from splife.pattern import Motif, successor

@composite
def st_motif(draw):
    m = draw(integers(min_value=1, max_value=10))
    n = draw(integers(min_value=1, max_value=10))
    return Motif.from_list(
        [draw(lists(sampled_from([0, 1]), min_size=m, max_size=m))
            for _ in range(n)])


@given(motif=st_motif())
def test_list_roundtrips(motif):
    assert Motif.from_list(motif.as_list()) == motif

@given(motif=st_motif())
def test_txt_roundtrips(motif):
    assert Motif.from_txt(motif.as_txt()) == motif

def test_succ():
    block = Motif.from_list([[1, 1], [1, 1]])
    s = successor(block)
    assert s is not block
    assert s == block

@given(motif=st_motif())
def test_canonical(motif):
    motif.canonicalize()
    s1 = motif.as_txt()
    motif.canonicalize()
    s2 = motif.as_txt()
    assert s1 == s2
