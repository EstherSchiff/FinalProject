import pytest
from card_helpers import get_code, code_to_words, get_card_code, codes_to_symbols

@pytest.mark.parametrize("name, code", [("TEN OF HEARTS", "10H"), ("ACE OF SPADES", "AS"), ("KING OF DIAMONDS", "KD")])
def test_get_code(name, code):
    card_code = get_code(name)
    assert card_code == code

@pytest.mark.parametrize("word_result, code", [("Ten Of Hearts", "10H"), ("Ace Of Spades", "AS"), ("King Of Diamonds", "KD")])
def test_code_to_words(word_result, code):
    word = code_to_words(code, "cards.db")
    assert word == word_result

@pytest.mark.parametrize("letter_code, symbol_code", [(["AS", "2C", "JD", "10H"], ["A♤", "2♧", "J♢", "10♡"])])
def test_codes_to_symbols(letter_code, symbol_code):
    result = codes_to_symbols(letter_code)
    assert result == symbol_code

@pytest.mark.parametrize("value, suit, code_result", [("9", "♤", "9S"), ("10", "♢", "10D"), ("K", "♧", "KC"), ("3", "♡", "3H")])
def test_get_card_code(value, suit, code_result):
    code = get_card_code(value, suit)
    assert code == code_result
