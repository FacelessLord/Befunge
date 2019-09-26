from befunge.field import Field


def test_field_init():
    lines = [['>', 'v'], ['<', '^']]
    try:
        fld = Field(2, 2, lines)
    except Exception as e:
        raise e
    else:
        assert fld is not None
        assert fld.width == 2
        assert fld.height == 2


def test_field_get():
    lines = [['>', 'v'], ['^', '<']]
    fld = Field(2, 2, lines)
    assert fld.get_symbol_at(0, 0) == '>'
    assert fld.get_symbol_at(1, 0) == 'v'
    assert fld.get_symbol_at(0, 1) == '^'
    assert fld.get_symbol_at(1, 1) == '<'


def test_field_set():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    fld.set_symbol_at(0, 0, 'v')
    fld.set_symbol_at(1, 0, '<')
    fld.set_symbol_at(1, 1, '^')
    fld.set_symbol_at(0, 1, '>')

    assert fld.get_symbol_at(0, 0) == 'v'
    assert fld.get_symbol_at(1, 0) == '<'
    assert fld.get_symbol_at(0, 1) == '>'
    assert fld.get_symbol_at(1, 1) == '^'


def test_load_file():
    fld = Field.load_file("tests/fld_test_program.txt")
    assert fld.width == 11
    assert fld.height == 5
    assert fld.get_symbol_at(0, 0) == '>'
    assert fld.get_symbol_at(10, 0) == 'v'
    assert fld.get_symbol_at(10, 4) == '<'
    assert fld.get_symbol_at(0, 4) == '^'
