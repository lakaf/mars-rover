import pytest
from marsrover.util import strip_str_list


def test_strip_str_list():
    assert strip_str_list([]) == []
    assert strip_str_list(['a']) == ['a']
    assert strip_str_list(['a', 'BB']) == ['a', 'BB']
    assert strip_str_list(['a', '']) == ['a', '']
    assert strip_str_list([' a', 'c ']) == ['a', 'c']
    assert strip_str_list([' a\n', '\n\rc \t']) == ['a', 'c']

    with pytest.raises(Exception):
        strip_str_list("A")
