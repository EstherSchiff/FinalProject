import streamlit as st
from database import init_db, reset_game, update_card
from scrape import scrape_cards
from api import get_secret_card


@st.cache_resource
def initialize_db():
    init_db()


def secret_card():
    if "secret_card" not in st.session_state:
        st.session_state.secret_card = get_secret_card()


def get_card_code():
    suit_dict = {'♤': 'S', '♡': 'H', '♢': 'D', '♧': 'C'}
    # build guess
    return value+suit_dict[suit]


def check_guess():
    return card_code == st.session_state.secret_card


initialize_db()
scrape_cards()
secret_card()

# page set up
st.header("Welcome to Card Guesser!")
st.write("Choose a card value and suit, then press the button to check!")
with st.form("Guess", enter_to_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        value = st.selectbox("Value", [
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
    with col2:
        suit = st.selectbox("Suit", ['♤', '♡', '♢', '♧'])
    submit_button = st.form_submit_button("Guess")
new_game = st.button("New Game")

if submit_button:
    card_code = get_card_code()
    st.write(st.session_state.secret_card)
    update_card(1, card_code)
    if check_guess() is True:
        st.write("You got it!")

if new_game:
    reset_game()
