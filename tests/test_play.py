from streamlit.testing.v1 import AppTest
from unittest.mock import patch
import requests
from play import main

# ensures a toast pops up if there is an error
@patch('streamlit.toast')
def test_catch_error(mock_toast):
    with patch('requests.get', side_effect=requests.HTTPError("Test error")):
        main()
        mock_toast.assert_called_once()

# ensures there are buttons in the sidebar
def test_buttons():
    at = AppTest.from_file("play.py").run(timeout=60)
    button_labels = [btn.label for btn in at.sidebar.button]
    assert "Guess" in button_labels
    assert "New Game" in button_labels

# ensures there are selectboxes in the sidebar
def test_selectboxes():
    at = AppTest.from_file("play.py").run(timeout=60)
    selectbox_labels = [sbox.label for sbox in at.sidebar.selectbox]
    assert "Value" in selectbox_labels
    assert "Suit" in selectbox_labels
