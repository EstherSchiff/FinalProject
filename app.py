import streamlit as st
from database import init_db, reset_db, update_card, code_to_words, get_card_data
from scrape import scrape_cards
from api import get_secret_card
from ai import encourage


def secret_card():
    if "secret_card" not in st.session_state:
        st.session_state["secret_card"] = get_secret_card()


def set_guesses():
    if "guesses_left" not in st.session_state:
        st.session_state["guesses_left"] = 5


def get_card_code(value, suit):
    suit_dict = {'♤': 'S', '♡': 'H', '♢': 'D', '♧': 'C'}
    # build guess
    return value+suit_dict[suit]


def codes_to_symbols(card_codes):
    reverse_suit_dict = {'S': '♤', 'H': '♡', 'D': '♢', 'C': '♧'}
    card_symbols = []
    for code in card_codes:
        num = code[:-1]
        letter = code[-1]
        symbol = reverse_suit_dict[letter]
        card_symbols.append(num+symbol)
    return card_symbols


# def check_guess(card_code):
#     return card_code == st.session_state["secret_card"]


def reset_game():
    reset_db()
    for key in ["secret_card", "guesses_left", "game_result", "game_over", "submit_disabled"]:
        if key in st.session_state:
            del st.session_state[key]
    secret_card()
    set_guesses()


def game_over():
    if st.session_state["game_result"] == "win":
        st.success("You won! Game over!")
    if st.session_state["game_result"] == "lose":
        st.error(
            f"Game over! The card was {code_to_words(st.session_state['secret_card'])}.")


def continue_game(card_code):
    if st.session_state["submit_button"] and "game_result" not in st.session_state:
        st.write(st.session_state["secret_card"])  # JUST FOR DEBUGGING!
        update_card(1, card_code)
        st.session_state["guesses_left"] -= 1
        st.write(f"Guesses remaining: {st.session_state['guesses_left']}")


def header():
    st.header("Welcome to Card Guesser!")
    st.write("Choose a card value and suit, then press the button to check!")


def form_input():
    with st.form("Guess", enter_to_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            value = st.selectbox("Value", [
                '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
        with col2:
            suit = st.selectbox("Suit", ['♤', '♡', '♢', '♧'])
        st.session_state["submit_button"] = st.form_submit_button(
            "Guess", disabled=st.session_state["guesses_left"] <= 1)
        return get_card_code(value, suit)


def process_guess(card_code):
    if st.session_state["submit_button"]:
        if card_code == st.session_state["secret_card"]:
            st.session_state["game_result"] = "win"
            st.session_state["submit_disabled"] = True
            game_over()
            st.balloons()
        elif st.session_state["guesses_left"] == 0:
            st.session_state["game_result"] = "lose"
            st.session_state["submit_disabled"] = True
            game_over()
        else:
            continue_game(card_code)


def display_data():
    card_codes = get_card_data()
    card_symbols = codes_to_symbols(card_codes)
    st.write(", ".join(card_symbols))


def play_game():
    new_game = st.button("New Game")
    if new_game:
        reset_game()
    card_code = form_input()
    process_guess(card_code)


if "db_initialized" not in st.session_state:
    init_db()
    st.session_state["db_initialized"] = True

if "scraped" not in st.session_state:
    scrape_cards()
    st.session_state["scraped"] = True

secret_card()
set_guesses()

header()  # maybe not reload
play_game()
encourage()
display_data()
