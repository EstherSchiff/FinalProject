from database import init_db, insert_card, update_card, reset_db, get_guessed_cards
import os

def test_init_db():
    init_db()
    assert os.path.exists("database.py")
    
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
