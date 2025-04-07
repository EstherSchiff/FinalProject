import requests
import sys


# request to create a deck, returns the deck ID
def create_deck():
    try:
        request = requests.get(
            "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        request.raise_for_status()
    except requests.HTTPError:
        sys.exit("Couldn't complete request!")

    # if request is not successful
    if not request.ok:
        sys.exit('There was an error creating the deck of cards.')
    return request.json()["deck_id"]


# request to draws cards from an existing deck
def draw_cards(deck_id):
    try:
        request = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={1}")
        request.raise_for_status()
    except requests.HTTPError:
        sys.exit("Couldn't complete request!")

    # if request is not successful
    if not request.ok:
        sys.exit('There was an error drawing a card.')
    return request


def get_secret_card():
    deck_id = create_deck()
    mycards = draw_cards(deck_id)
    mycards = mycards.json()
    cards = mycards["cards"]
    result = cards[0]["code"]
    if "0" in result:
        result = result.replace("0", "10")  # api returns 0 for 10
    return result
