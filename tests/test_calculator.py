import pytest

from bluserver.calculator import calculate


@pytest.mark.parametrize("expression, expected_result", (
    ('38 - 83 - 52 + 30 - 24 - 89 / 66 + 18 / 7 * 77', '105.65151515151518'),
    ('57 + 87 - 24 * 27 / 8\n + 53 - 87 * 6 * 60 - 30', '-31234.0'),
    ('1 + 1     - 0-1 * 1\n + 2 - 2    *    6 *  60-30', '-747'),
    ('0+0+0+0+0+0-0', '0'),
    ('1*1*0', '0'),
    ('1 / 1000000000001', '9.99999999999e-13'),
    ('1 * 1000000000001', '1000000000001'),
    ('7  +   1-\n\n\n\n1-1\t\t\t\t\n-1\n-\n1\n-\n1-1-1-1\n\n\n\n', '0'),
    ('', ''),
    ('\n\n', ''),
    ('\n\t \n', ''),
    ('1', '1'),
    # ('-1', '-1'),  # TODO: not handled yet
))
def test_dependency_creation(expression, expected_result):
    """Test calculator module, calculate method."""
    assert str(calculate(expression)) == expected_result
