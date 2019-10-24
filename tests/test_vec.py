from befunge.caret import Vec


def test_vec_init():
    try:
        vec = Vec()
    except Exception as e:
        raise e
    else:
        assert vec is not None


def test_vec_sum():
    a = Vec(2, 3)
    b = Vec(3, 2)
    assert a + b == Vec(5, 5)
