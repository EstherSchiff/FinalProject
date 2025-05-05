from connection import get_connection
# converts word form to code form (Ex. KING OF SPADE->KS)
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

# converts code form back to word form (Ex. KS->King Of Spades)
def code_to_words(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cards WHERE code = ?", (code,))
    result = cursor.fetchone()
    return result[0].title()

# converts symbol code to letter code (Ex. 2♡->2H)
def get_card_code(value, suit):
    suit_dict = {'♤': 'S', '♡': 'H', '♢': 'D', '♧': 'C'}
    # build guess
    return value + suit_dict[suit]

# converts a letter code to symbol code (Ex. 2H->2♡)
def codes_to_symbols(card_codes):
    reverse_suit_dict = {'S': '♤', 'H': '♡', 'D': '♢', 'C': '♧'}
    card_symbols = []
    for code in card_codes:
        num = code[:-1]
        letter = code[-1]
        symbol = reverse_suit_dict[letter]
        card_symbols.append(num + symbol)
    return card_symbols
