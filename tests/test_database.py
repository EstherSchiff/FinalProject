from database import init_db, insert_card, update_card, reset_db, get_guessed_cards, get_count, update_stat_count
import sqlite3
import pytest
from unittest.mock import patch

@pytest.fixture
def memory_db():
    """Provides a temporary in-memory SQLite DB with tables."""
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    yield conn
    conn.close()

@pytest.fixture
def db_conn():
    """Provides a temporary in-memory blank SQLite DB."""
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

# ensures db is properly set up with its tables
def test_init_db(db_conn):
    init_db(db_conn)
    tables = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = [table[0] for table in tables]
    assert "cards" in table_names
    assert "stats" in table_names

# ensures a card is properly inserted into the table in the db
def test_insert_card(memory_db):
    with patch("database.get_code", return_value="10S"):
        insert_card("U+1F0AA", "TEN OF SPADES", memory_db)
        result = memory_db.execute("SELECT * FROM cards").fetchall()
        assert len(result) == 1
        assert result[0][0] == "10S"

# ensures that a card is properly updated to guessed
def test_update_card(memory_db):
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('AS', 'U+1F0A1', 'ACE OF SPADES', 0)")
    memory_db.commit()
    update_card(True, "AS", memory_db)
    row = memory_db.execute("SELECT guessed FROM cards WHERE code = 'AS'").fetchone()
    assert row[0] == 1

# ensures db is cleared
def test_reset_db(memory_db):
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('2D', 'U+1F0C2', 'TWO OF DIAMONDS', 1)")
    memory_db.commit()
    reset_db(memory_db)
    guessed = memory_db.execute("SELECT guessed FROM cards").fetchall()
    guessed_values = [row[0] for row in guessed]
    assert 1 not in guessed_values

# ensures only guessed cards are returned
def test_get_guessed_cards(memory_db):
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('2D', 'U+1F0C2', 'TWO OF DIAMONDS', 0)")
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('3D', 'U+1F0C3', 'THREE OF DIAMONDS', 1)")
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('4D', 'U+1F0C4', 'FOUR OF DIAMONDS', 0)")
    memory_db.execute("INSERT INTO cards (code, unicode, name, guessed) VALUES ('5D', 'U+1F0C5', 'FIVE OF DIAMONDS', 1)")
    guessed_cards = get_guessed_cards(memory_db)
    assert len(guessed_cards) == 2
    assert "5D" in guessed_cards
    assert "3D" in guessed_cards

# ensures win and lose counts are retreived
def test_get_count(memory_db):
    all_counts = get_count(memory_db)
    win_count = all_counts[0][0]
    lose_count = all_counts[1][0]
    assert win_count == 0
    assert lose_count == 0

# ensures stat counts are updated
def test_update_stat_count(memory_db):
    update_stat_count("win", memory_db)
    win_count = memory_db.execute("SELECT count FROM stats").fetchone()[0]
    assert win_count == 1
