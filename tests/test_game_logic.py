import pytest
from unittest.mock import patch
import streamlit as st
from streamlit.testing.v1 import AppTest
from game_logic import initialize_game, calc_used_guesses, calc_progress_fraction, win, lose, reset_game, continue_game # progress_bar, display_data, load_sidebar, process_guess, ai, display_messages, check_game_state

def test_initialize_game():
    initialize_game()
    assert st.session_state["game_initialized"] == True
    assert st.session_state["db_initialized"] == True
    assert st.session_state["scraped"] == True
    assert st.session_state["secret_card"] is not None
    assert st.session_state["guesses_left"] == 5
    assert st.session_state["guess_disabled"] == False
    assert st.session_state["launched"] == True

@pytest.mark.parametrize("guesses_left, expected", [(5, 0), (4, 1), (1, 4), (0, 5)])
def test_calc_used_guesses(guesses_left, expected):
    st.session_state["guesses_left"] = guesses_left
    result = calc_used_guesses()
    assert result == expected

@pytest.mark.parametrize("used, expected", [(5, 1), (4, 0.8), (1, 0.2), (0, 0)])
def test_calc_used_guesses(used, expected):
    result = calc_progress_fraction(used)
    assert result == expected

def test_win():
    win()
    assert st.session_state["guess_disabled"] == True
    assert st.session_state["win_message"] == "You guessed it! Press New Game to play again."

def test_lose():
    st.session_state["secret_card"] = "2S"
    lose()
    assert st.session_state["guess_disabled"] == True
    assert "You ran out of guesses" in st.session_state["lose_message"]

def test_reset_game():
    reset_game()
    for key in ["secret_card", "guesses_left", "guess_disabled", "win_message", "lose_message"]:
        assert key not in st.session_state

@pytest.mark.parametrize("guesses_left, ending_guesses", [(4, 3), (1, 0), (2,1)])
def test_continue_game(guesses_left, ending_guesses):
    st.session_state["guesses_left"] = guesses_left
    continue_game("2S")
    assert st.session_state["guesses_left"] == ending_guesses

