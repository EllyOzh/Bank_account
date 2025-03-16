import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize('num, expected', [
    ('1234567890123456', '1234 56** **** 3456'),
    (1234567890123456, '1234 56** **** 3456'),
    (1234, '')
])
def test_get_mask_card_number_ok(num, expected):
    assert get_mask_card_number(num) == expected

@pytest.mark.parametrize("account_num, expected", [
    ('98765432109876543210', '**3210'),
    (98765432109876543210, '**3210'),
    (4321, '')
])
def test_get_mask_account_ok(account_num, expected):
    assert get_mask_account(account_num) == expected

