import pytest
from unittest.mock import patch
import streamlit as st
from game_logic import initialize_game, calc_used_guesses, calc_progress_fraction, win, lose, reset_game, continue_game, check_game_state, display_messages, display_data, ai, process_guess, load_sidebar, progress_bar

# ensures session state variables are initialized and required functions called
@patch("game_logic.reset_game")
@patch("game_logic.init_db")
@patch("game_logic.scrape_cards")
def test_initialize_game(mock_scrape, mock_init, mock_reset):
    initialize_game()
    assert st.session_state["game_initialized"] == True
    assert st.session_state["db_initialized"] == True
    assert st.session_state["scraped"] == True
    assert st.session_state["secret_card"] is not None
    assert st.session_state["guesses_left"] == 5
    assert st.session_state["guess_disabled"] == False
    mock_init.assert_called_once()
    mock_reset.assert_called_once()
    mock_scrape.assert_called_once()

# ensures that the remaining guesses are calculated correctly
@pytest.mark.parametrize("guesses_left, expected", [(5, 0), (4, 1), (1, 4), (0, 5)])
def test_calc_used_guesses(guesses_left, expected):
    st.session_state["guesses_left"] = guesses_left
    result = calc_used_guesses()
    assert result == expected

# ensures that progress is converted to a fraction correctly
@pytest.mark.parametrize("used, expected", [(5, 1), (4, 0.8), (1, 0.2), (0, 0)])
def test_calc_progress_fraction(used, expected):
    result = calc_progress_fraction(used)
    assert result == expected

# ensures win function updates session state and updates the stats
@patch("game_logic.update_stat_count")
def test_win(mock_update_stat):
    st.session_state.clear()
    win()
    assert st.session_state["guess_disabled"] == True
    assert st.session_state["win_message"] == "You guessed it! Press New Game to play again."
    mock_update_stat.assert_called_once()

# ensures lose function updates session state and updates the stats
@patch("game_logic.update_stat_count")
def test_lose(mock_update_stat):
    st.session_state["secret_card"] = "2S"
    lose()
    assert st.session_state["guess_disabled"] == True
    assert "You ran out of guesses" in st.session_state["lose_message"]
    mock_update_stat.assert_called_once()

# ensures the database is properly reset and session state is cleared
@patch("game_logic.reset_db")
def test_reset_game(mock_reset):
    reset_game()
    for key in ["secret_card", "guesses_left", "guess_disabled", "win_message", "lose_message"]:
        assert key not in st.session_state

# ensures guesses left is updated properly
@pytest.mark.parametrize("guesses_left, ending_guesses", [(4, 3), (1, 0), (2, 1)])
def test_continue_game(guesses_left, ending_guesses):
    st.session_state["guesses_left"] = guesses_left
    continue_game("2S")
    assert st.session_state["guesses_left"] == ending_guesses

# ensures game ends when a win or lose message is in session state
@pytest.mark.parametrize("message_type", ["win_message", "lose_message"])
@patch("game_logic.reset_game")
def test_check_game_state(mock_reset, message_type):
    st.session_state[message_type] = "Game over"
    check_game_state()
    mock_reset.assert_called_once()

# ensures proper lose message is displayed to user
@patch("streamlit.error")
def test_display_messages_lose(mock_error_message):
    st.session_state["lose_message"] = "Game over"
    display_messages()
    mock_error_message.assert_called_once_with("Game over")

# ensures proper win message is displayed to user
@patch("streamlit.success")
@patch("streamlit.balloons")
def test_display_messages_win(mock_balloons, mock_success_message):
    st.session_state.clear()
    st.session_state["win_message"] = "Game over"
    display_messages()
    mock_success_message.assert_called_once_with("Game over")
    mock_balloons.assert_called_once()

# ensures display data is called since it shouldn't show win or lose
@patch("game_logic.display_data")
def test_display_messages_continue(mock_display_data):
    st.session_state.pop("win_message", None)
    st.session_state.pop("lose_message", None)
    display_messages()
    mock_display_data.assert_called_once()

# ensures guessed cards are show to the user
@patch("game_logic.get_guessed_cards")
@patch("game_logic.codes_to_symbols")
@patch("streamlit.write")
def test_display_data(mock_write, mock_codes_to_symbols, mock_get_guessed_cards):
    mock_get_guessed_cards.return_value = ["2S", "3D"]
    mock_codes_to_symbols.return_value = ["2♤", "3♢"]
    display_data()
    mock_write.assert_any_call("Guessed cards: ")
    mock_write.assert_any_call(", ".join(["2♤", "3♢"]))

# ensures an ai message is generated
@patch("game_logic.encourage")
def test_ai(mock_encourage):
    st.session_state["guesses_left"] = 3
    ai()
    mock_encourage.assert_called_once()

# makes sure process guess calls win if the user guesses correctly
@patch("game_logic.get_card_code")
@patch("game_logic.win")
def test_process_guess_win(mock_win, mock_get_card_code):
    mock_get_card_code.return_value = "2S"
    st.session_state["secret_card"] = "2S"
    st.session_state["guess"] = True
    st.session_state["value"] = "2"
    st.session_state["suit"] = "♤"
    st.session_state["guesses_left"] = 0
    process_guess()
    mock_win.assert_called_once()

# ensures process guess calls lose if the user guesses incorrectly on the last try
@patch("game_logic.get_card_code")
@patch("game_logic.lose")
def test_process_guess_lose(mock_lose, mock_get_card_code):
    mock_get_card_code.return_value = "2S"
    st.session_state["secret_card"] = "2D"
    st.session_state["guess"] = True
    st.session_state["value"] = "2"
    st.session_state["suit"] = "♤"
    st.session_state["guesses_left"] = 1
    process_guess()
    mock_lose.assert_called_once()

# ensures the game continues if the user has more guesses and hasn't guessed yet
@patch("game_logic.get_card_code")
@patch("game_logic.continue_game")
def test_process_guess_continue(mock_continue, mock_get_card_code):
    mock_get_card_code.return_value = "2S"
    st.session_state["secret_card"] = "2D"
    st.session_state["guess"] = True
    st.session_state["value"] = "2"
    st.session_state["suit"] = "♤"
    st.session_state["guesses_left"] = 2
    process_guess()
    mock_continue.assert_called_once()

# ensures the sidebar is properly loaded
@patch("streamlit.button")
@patch("streamlit.selectbox")
def test_load_sidebar_elements(mock_selectbox, mock_button):
    st.session_state["guess_disabled"] = False
    load_sidebar()
    mock_button.assert_any_call("New Game")
    mock_selectbox.assert_any_call("Value", [
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], disabled=False)
    mock_selectbox.assert_any_call("Suit", ['♤', '♡', '♢', '♧'], disabled=False)

# checks that reset is called when user presses new game
@patch("streamlit.button")
@patch("streamlit.selectbox")
@patch("game_logic.reset_game")
def test_load_sidebar_new_game(mock_reset, *_):  # patches also button and selectbox even though not called directly
    st.session_state["new_game"] = True
    st.session_state["guess_disabled"] = False
    load_sidebar()
    mock_reset.assert_called_once()

# ensures the progress bar is properly displayed
@patch("streamlit.progress")
@patch("streamlit.write")
@patch("game_logic.calc_progress_fraction")
@patch("game_logic.calc_used_guesses")
def test_progress_bar(mock_calc_used_guesses, mock_calc_progress_fraction, mock_write, mock_progress):
    st.session_state.pop("win_message", None)
    st.session_state.pop("lose_message", None)
    mock_calc_used_guesses.return_value = 2
    mock_calc_progress_fraction.return_value = 0.4
    progress_bar()
    mock_calc_used_guesses.assert_called_once()
    mock_calc_progress_fraction.assert_called_once()
    mock_write.assert_called_once_with("Game progress: ")
    mock_progress.assert_called_once_with(st.session_state["progress"])
    assert st.session_state["progress"] == 0.4
