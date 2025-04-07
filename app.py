import streamlit as st
from database import init_db, reset_db, update_card, code_to_words
from scrape import scrape_cards
from api import get_secret_card


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


# def check_guess(card_code):
#     return card_code == st.session_state["secret_card"]


def reset_game():
    reset_db()
    for key in ["secret_card", "guesses_left", "game_result", "game_over"]:
        if key in st.session_state:
            del st.session_state[key]
    secret_card()
    set_guesses()


def game_over():
    if "game_result" in st.session_state:
        if st.session_state["game_result"] == "win":
            st.success("You won! Game over!")
        if st.session_state["game_result"] == "lose":
            st.error(
                f"Game over! The card was {code_to_words(st.session_state['secret_card'])}.")
        return True
    else:  # game not over
        return False


def continue_game(card_code, submitted):
    if submitted and "game_result" not in st.session_state:
        st.write(st.session_state["secret_card"])  # JUST FOR DEBUGGING!
        update_card(1, card_code)
        st.session_state["guesses_left"] -= 1
        st.write(f"Guesses remaining: {st.session_state['guesses_left']}")


def check_game_status(card_code):
    if card_code == st.session_state["secret_card"]:
        st.session_state["game_result"] = "win"
        return True
    if st.session_state["guesses_left"] == 0:
        st.session_state["game_result"] = "lose"
        return True
    return False


def header():
    st.header("Welcome to Card Guesser!")
    st.write("Choose a card value and suit, then press the button to check!")
    st.write("You have 5 guesses.")


def user_guess():
    if game_over():
        return None  # Prevent further guesses if game is over

    with st.form("Guess", enter_to_submit=True):
        submit_disabled = st.session_state["guesses_left"] <= 0

        # card_code = None
        col1, col2 = st.columns(2)
        with col1:
            value = st.selectbox("Value", [
                '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])
        with col2:
            suit = st.selectbox("Suit", ['♤', '♡', '♢', '♧'])
        submit_button = st.form_submit_button(
            "Guess", disabled=submit_disabled)
        card_code = get_card_code(value, suit)
        if submit_button and not game_over():  # Proceed if the game is not over
            if "game_result" not in st.session_state:
                if check_game_status(card_code):  # Check if win or lose
                    st.session_state["game_over"] = True  # Set the game as over
                else:
                    continue_game(card_code, submit_button)
    return card_code


def play_game():
    new_game = st.button("New Game")
    if new_game:
        reset_game()
    card_code = user_guess()

    if card_code and check_game_status(card_code):
        st.session_state["game_over"] = True


if __name__ == "__main__":
    if "db_initialized" not in st.session_state:
        init_db()
        st.session_state["db_initialized"] = True

    if "scraped" not in st.session_state:
        scrape_cards()
        st.session_state["scraped"] = True

    secret_card()
    set_guesses()

    header()
    play_game()
