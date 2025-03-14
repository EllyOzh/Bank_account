from src.masks import get_mask_card_number, get_mask_account
import pytest

@pytest.fixture
def card_number(request):
    return request.param

@pytest.mark.parametrize('card_number', [7896541236985478965, 9685741236985, 7458963214523698], indirect = True)

def test_get_mask_card_number(card_number):
    assert card_number in [7896541236985478965, 9685741236985, 7458963214523698]

@pytest.fixture
def account_number(request):
    return request.param

@pytest.mark.parametrize('account_number', [25417811479632587412, 2521156511335, 'lalalal'], indirect = True)

def test_get_mask_card_number(card_number):
    assert card_number in [25417811479632587412, 2521156511335, 'lalalal']
