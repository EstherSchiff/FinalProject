import sqlite3

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

# converts word form to code form
def get_code(name):
    value_to_code = {
        "ACE": "A", "KING": "K", "QUEEN": "Q", "JACK": "J",
        "TEN": "10", "NINE": "9", "EIGHT": "8", "SEVEN": "7",
        "SIX": "6", "FIVE": "5", "FOUR": "4", "THREE": "3", "TWO": "2"
    }
    suit_to_code = {
        "SPADES": "S", "HEARTS": "H", "DIAMONDS": "D", "CLUBS": "C"
    }
    value, suit = name.split(" OF ")
    return value_to_code[value] + suit_to_code[suit]

# converts code form back to word form
def code_to_words(code):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cards WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result[0].title()

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
