from api_helpers import create_deck, draw_cards

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
