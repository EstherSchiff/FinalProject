from database import init_db, insert_card, update_card, reset_db, get_guessed_cards
import os
import sqlite3
import pytest
from unittest.mock import patch

@pytest.fixture
def memory_db():
    """Provides a temporary in-memory SQLite DB."""
    conn = sqlite3.connect(":memory:")
    conn.execute('''CREATE TABLE cards (
                        code TEXT UNIQUE,
                        unicode TEXT UNIQUE,
                        name TEXT,
                        guessed BOOL DEFAULT 0)''')
    yield conn
    conn.close()

def test_init_db():
    init_db()
    assert os.path.exists("database.py")

def test_insert_card(memory_db):
    with patch("database.get_code", return_value="10S"):
        insert_card("U+1F0AA", "TEN OF SPADES", memory_db)
        result = memory_db.execute("SELECT * FROM cards").fetchall()
        assert len(result) == 1
        assert result[0][0] == "10S"

def test_update_card(memory_db):
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('AS', 'U+1F0A1', 'ACE OF SPADES', 0)")
    memory_db.commit()
    update_card(True, "AS", memory_db)
    row = memory_db.execute("SELECT guessed FROM cards WHERE code = 'AS'").fetchone()
    assert row[0] == 1

def test_reset_db(memory_db):
    with patch("sqlite3.connect", return_value=memory_db):
        memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('2D', 'U+1F0C2', 'TWO OF DIAMONDS', 1)")
        memory_db.commit()
        reset_db()
        guessed_values = memory_db.execute("SELECT guessed FROM cards").fetchall()
        assert 0 not in guessed_values

def test_get_guessed_cards(memory_db):
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('2D', 'U+1F0C2', 'TWO OF DIAMONDS', 0)")
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('3D', 'U+1F0C3', 'THREE OF DIAMONDS', 1)")
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('4D', 'U+1F0C4', 'FOUR OF DIAMONDS', 0)")
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('5D', 'U+1F0C5', 'FIVE OF DIAMONDS', 1)")
    guessed_cards = get_guessed_cards(memory_db)
    assert len(guessed_cards) == 2
    assert "5D" in guessed_cards
    assert "3D" in guessed_cards
