import sqlite3
from card_helpers import get_code
db = "cards.db"

# Database setup
def init_db():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cards (
                    code TEXT UNIQUE,
                    unicode TEXT UNIQUE,
                    name TEXT,
                    guessed BOOL DEFAULT 0)''')
    conn.commit()
    conn.close()

# insert a card into the database
def insert_card(unicode, name, db_name=db):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    code = get_code(name)
    c.execute("INSERT OR IGNORE INTO cards (code, unicode, name) VALUES (?,?,?)",
              (code, unicode, name))
    conn.commit()
    conn.close()

# Update if card was chosen
def update_card(guessed, code):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("UPDATE cards SET guessed = ? WHERE code = ?", (guessed, code))
    conn.commit()
    conn.close()

# set all card's guessed to false for new game
def reset_db():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("UPDATE cards SET guessed = 0")
    conn.commit()
    conn.close()

# returns all guessed cards
def get_guessed_cards():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM cards WHERE guessed == 1")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
