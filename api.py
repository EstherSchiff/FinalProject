import requests

# custom errors
class DrawCardError(Exception):
    pass


class CreateDeckError(Exception):
    pass


# request to create a deck, returns the deck ID
def create_deck():
    try:
        request = requests.get(
            "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        request.raise_for_status()
    except requests.HTTPError:
        raise CreateDeckError("There was a problem creating the deck.")
    if not request.json().get('success', True):  # If 'success' is False
        raise CreateDeckError("There was a problem creating the deck.")
    return request.json()["deck_id"]


# request to draws cards from an existing deck
def draw_cards(deck_id):
    try:
        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={1}")
        request.raise_for_status()
    except requests.HTTPError:
        raise DrawCardError("There was a problem drawing a card.")
    if not request.json().get('success', True):  # If success is false
        raise DrawCardError("There was a problem drawing a card.")
    return request

# uses create and draw to get one secret card
def get_secret_card():
    deck_id = create_deck()
    mycards = draw_cards(deck_id)
    mycards = mycards.json()
    cards = mycards["cards"]
    result = cards[0]["code"]
    if "0" in result:
        result = result.replace("0", "10")  # api returns 0 for 10
    return result
