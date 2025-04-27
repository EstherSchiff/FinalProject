import pytest
from unittest.mock import patch
import sqlite3
import streamlit as st
from streamlit.testing.v1 import AppTest
# progress_bar
from game_logic import initialize_game, calc_used_guesses, calc_progress_fraction, win, lose, reset_game, continue_game, check_game_state, display_messages, display_data, ai, process_guess, load_sidebar

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

@pytest.mark.parametrize("guesses_left, ending_guesses", [(4, 3), (1, 0), (2, 1)])
def test_continue_game(guesses_left, ending_guesses):
    st.session_state["guesses_left"] = guesses_left
    continue_game("2S")
    assert st.session_state["guesses_left"] == ending_guesses

@pytest.mark.parametrize("message_type", ["win_message", "lose_message"])
@patch("game_logic.reset_game")
def test_check_game_state(mock_reset, message_type):
    st.session_state[message_type] = "Game over"
    check_game_state()
    mock_reset.assert_called_once()

@patch("streamlit.error")
def test_display_messages_lose(mock_error_message):
    st.session_state["lose_message"] = "Game over"
    display_messages()
    mock_error_message.assert_called_once_with("Game over")

# why does this pass individually, but not when i run pytest --cov
@patch("streamlit.success")
@patch("streamlit.balloons")
def test_display_messages_win(mock_balloons, mock_success_message):
    st.session_state["win_message"] = "Game over"
    display_messages()
    mock_success_message.assert_called_once_with("Game over")
    mock_balloons.assert_called_once()

@patch("game_logic.display_data")
def test_display_messages_continue(mock_display_data):
    for key in ["win_message", "lose_message"]:
        if key in st.session_state:
            del st.session_state[key]
    display_messages()
    mock_display_data.assert_called_once()

@patch("game_logic.get_guessed_cards")
@patch("game_logic.codes_to_symbols")
@patch("streamlit.write")
def test_display_data(mock_write, mock_codes_to_symbols, mock_get_guessed_cards):
    mock_get_guessed_cards.return_value=["2S", "3D"]
    mock_codes_to_symbols.return_value=["2♤", "3♢"]
    display_data()
    mock_write.assert_any_call("Guessed cards: ")
    mock_write.assert_any_call(", ".join(["2♤", "3♢"]))

@patch("game_logic.encourage")
def test_ai(mock_encourage):
    st.session_state["guesses_left"] = 3
    ai()
    mock_encourage.assert_called_once()

@patch("game_logic.get_card_code")
@patch("game_logic.win")
def test_process_guess_win(mock_win, mock_get_card_code):
    mock_get_card_code.return_value = "2S"
    st.session_state["secret_card"] = "2S"
    st.session_state["guess"] = True
    st.session_state["value"] ="2"
    st.session_state["suit"] = "♤"
    st.session_state["guesses_left"] = 0
    process_guess()
    mock_win.assert_called_once()

@patch("game_logic.get_card_code")
@patch("game_logic.lose")
def test_process_guess_lose(mock_lose, mock_get_card_code):
    mock_get_card_code.return_value = "2S"
    st.session_state["secret_card"] = "2D"
    st.session_state["guess"] = True
    st.session_state["value"] ="2"
    st.session_state["suit"] = "♤"
    st.session_state["guesses_left"] = 1
    process_guess()
    mock_lose.assert_called_once()

@patch("game_logic.get_card_code")
@patch("game_logic.continue_game")
def test_process_guess_continue(mock_continue, mock_get_card_code):
    mock_get_card_code.return_value = "2S"
    st.session_state["secret_card"] = "2D"
    st.session_state["guess"] = True
    st.session_state["value"] ="2"
    st.session_state["suit"] = "♤"
    st.session_state["guesses_left"] = 2
    process_guess()
    mock_continue.assert_called_once()

@patch("streamlit.button")
@patch("streamlit.selectbox")
@patch("game_logic.reset_game")
def test_load_sidebar(mock_reset, mock_selectbox, mock_button):
    st.session_state["guess_disabled"] = False
    load_sidebar()
    mock_button.assert_any_call("New Game")
    mock_selectbox.assert_any_call("Value", [
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], disabled=False)
    mock_selectbox.assert_any_call("Suit", ['♤', '♡', '♢', '♧'], disabled=False)


# keep testing load sidebar