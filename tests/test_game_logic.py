import pytest
from game_logic import codes_to_symbols, get_card_code

@pytest.mark.parametrize("letter_code, symbol_code", [(["AS", "2C", "JD", "10H"], ["A♤", "2♧", "J♢", "10♡"])])
def test_codes_to_symbols(letter_code, symbol_code):
    result = codes_to_symbols(letter_code)
    assert result == symbol_code

@pytest.mark.parametrize("value, suit, code_result", [("9", "♤", "9S"), ("10", "♢", "10D"), ("K", "♧", "KC"), ("3", "♡", "3H")])
def test_get_card_code(value, suit, code_result):
    code = get_card_code(value, suit)
    assert code == code_result
