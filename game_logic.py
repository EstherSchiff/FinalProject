import streamlit as st
from database import init_db, reset_db, update_card, get_guessed_cards, update_stat_count
from scrape import scrape_cards
from api import get_secret_card
from ai import encourage
from card_helpers import codes_to_symbols, get_card_code, code_to_words
from stats import game_stats

total_guesses = 5

# displays guessed cards
def display_data():
    card_codes = get_guessed_cards()
    card_symbols = codes_to_symbols(card_codes)
    col1, col2 = st.columns([2, 8])
    with col1:
        st.write("Guessed cards: ")
    with col2:
        st.write(", ".join(card_symbols))

# called when the user guesses correctly
def win():
    st.session_state["guess_disabled"] = True
    st.session_state["win_message"] = "You guessed it! Press New Game to play again."
    update_stat_count('win')
    st.rerun()

# called when the user runs out of guesses
def lose():
    st.session_state["guess_disabled"] = True
    st.session_state["lose_message"] = f'You ran out of guesses! The card was {code_to_words(st.session_state["secret_card"])}. Press New Game to play again.'
    update_stat_count('lose')
    st.rerun()

# loads the sidebar to enter a guess
def load_sidebar():
    with st.sidebar:
        st.session_state["new_game"] = st.button("New Game")
        st.session_state["value"] = st.selectbox("Value", [
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], disabled=st.session_state["guess_disabled"])
        st.session_state["suit"] = st.selectbox("Suit", ['♤', '♡', '♢', '♧'], disabled=st.session_state["guess_disabled"])
        st.session_state["guess"] = st.button("Guess", disabled=st.session_state["guess_disabled"])
    if st.session_state["new_game"]:
        reset_game()
        st.rerun()

# checks to see if the guess is correct and processes accordingly
def process_guess():
    if st.session_state["guess"]:
        card_code = get_card_code(st.session_state["value"], st.session_state["suit"])
        if card_code == st.session_state["secret_card"]:
            win()
        elif st.session_state["guesses_left"] == 1:
            lose()
        else:
            continue_game(card_code)

# resets the necessary keys in session state and resets the guess column in the database
def reset_game():
    reset_db()
    for key in ["secret_card", "guesses_left", "guess_disabled", "win_message", "lose_message"]:
        if key in st.session_state:
            del st.session_state[key]

# called if user guesses incorrectly, but still has remaining guesses
def continue_game(card_code):
    update_card(1, card_code)  # mark as guessed
    st.session_state["guesses_left"] -= 1

# gives the user an encouraging message from AI
def ai():
    if "win_message" not in st.session_state and "lose_message" not in st.session_state:
        st.write(encourage(st.session_state["guesses_left"]))

def calc_used_guesses():
    return total_guesses - st.session_state["guesses_left"]

def calc_progress_fraction(used):
    return used / total_guesses

# displays a progress bar showing how far the game progressed
def progress_bar():
    if "win_message" not in st.session_state and "lose_message" not in st.session_state:
        used_guesses = calc_used_guesses()
        progress = calc_progress_fraction(used_guesses)
        col1, col2 = st.columns([2, 8])
        with col1:
            st.write("Game progress: ")
        st.session_state["progress"] = progress  # Store the progress in session state
        with col2:
            st.progress(st.session_state["progress"])

def show_game_stats():
    plot = game_stats()
    with st.expander("See Game Stats"):
        st.pyplot(plot)

# initializes session state variables
def initialize_game():
    if "game_initialized" not in st.session_state:
        reset_game()
        st.session_state["game_initialized"] = True

    if "db_initialized" not in st.session_state:
        init_db()
        st.session_state["db_initialized"] = True

    if "scraped" not in st.session_state:
        scrape_cards()
        st.session_state["scraped"] = True

    if "secret_card" not in st.session_state:
        st.session_state["secret_card"] = get_secret_card()

    if "guesses_left" not in st.session_state:
        st.session_state["guesses_left"] = 5

    if "guess_disabled" not in st.session_state:
        st.session_state["guess_disabled"] = False

# displays a winning or losing message or the cards already guessed
def display_messages():
    if "lose_message" in st.session_state:
        st.error(st.session_state["lose_message"])
    elif "win_message" in st.session_state:
        st.success(st.session_state["win_message"])
        st.balloons()
    else:
        display_data()

# if game is over, resets game
def check_game_state():
    # If the game is over and the user hasn't pressed "New Game"
    if "win_message" in st.session_state or "lose_message" in st.session_state:
        reset_game()
