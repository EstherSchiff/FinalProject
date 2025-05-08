from connection import get_connection
from card_helpers import get_code

# set up table
def init_db(conn=None):
    if conn is None:
        conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cards (
                    code TEXT UNIQUE,
                    unicode TEXT UNIQUE,
                    name TEXT,
                    guessed BOOL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (
                    name TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0)''')
    c.execute("INSERT OR IGNORE INTO stats (name, count) VALUES ('win', 0)")
    c.execute("INSERT OR IGNORE INTO stats (name, count) VALUES ('lose', 0)")
    conn.commit()

# gets the counts of win and lose as a list of tuples
def get_count(conn=None):
    if conn is None:
        conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT count FROM stats")
    return c.fetchall()

# updates the win or lose count
def update_stat_count(count_type, conn=None):
    if conn is None:
        conn = get_connection()
    c = conn.cursor()
    c.execute(f"UPDATE stats SET count = count + 1 WHERE name = ?", (count_type,))
    conn.commit()

# insert a card into the database
def insert_card(unicode, name, conn=None):
    if conn is None:
        conn = get_connection()
    c = conn.cursor()
    code = get_code(name)
    c.execute("INSERT OR IGNORE INTO cards (code, unicode, name) VALUES (?,?,?)",
              (code, unicode, name))
    conn.commit()

# Update if card was chosen
def update_card(guessed, code, conn=None):
    if conn is None:
        conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE cards SET guessed = ? WHERE code = ?", (guessed, code))
    conn.commit()

# set all card's guessed to false for new game
def reset_db(conn=None):
    if conn is None:
        conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE cards SET guessed = 0")
    conn.commit()

# returns all guessed cards
def get_guessed_cards(conn=None):
    if conn is None:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM cards WHERE guessed == 1")
    rows = cursor.fetchall()
    return [row[0] for row in rows]
