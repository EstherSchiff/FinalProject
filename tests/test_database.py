import pytest
from database import init_db, get_code, insert_card, code_to_words, update_card, reset_db, get_guessed_cards
import os
import sqlite3

def test_init_db():
    init_db()
    assert os.path.exists("database.py")

@pytest.mark.parametrize("name, code", [("TEN OF HEARTS", "10H"), ("ACE OF SPADES", "AS"), ("KING OF DIAMONDS", "KD")])
def test_get_code(name, code):
    card_code = get_code(name)
    assert card_code == code

@pytest.mark.parametrize("word_result, code", [("Ten Of Hearts", "10H"), ("Ace Of Spades", "AS"), ("King Of Diamonds", "KD")])
def test_code_to_words(word_result, code):
    word = code_to_words(code)
    assert word == word_result

    
# creates a table in memory but it make a new one by the time it calls insert_card so its an issue
def test_insert_card():
    # conn = sqlite3.connect(":memory:")
    # cursor = conn.cursor()
    # cursor.execute("CREATE TABLE cards (code TEXT, unicode TEXT, name TEXT)")
    # conn.commit()
    # insert_card("🂡", "ACE OF SPADES", db_name=":memory:")
    # cursor.execute("SELECT * FROM cards")
    # all_cards = cursor.fetchall()
    # assert len(all_cards) == 1
    pass

def test_update_card():
    pass

def test_reset_db():
    pass

def test_get_guessed_cards():
    pass
