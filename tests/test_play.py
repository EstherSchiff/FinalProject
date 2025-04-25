from streamlit.testing.v1 import AppTest

def test_buttons():
    at = AppTest.from_file("play.py").run(timeout=60)
    button_labels= [btn.label for btn in at.sidebar.button]
    assert "Guess" in button_labels
    assert "New Game" in button_labels

def test_selectboxes():
    at = AppTest.from_file("play.py").run(timeout=60)
    selectbox_labels = [sbox.label for sbox in at.sidebar.selectbox]
    assert "Value" in selectbox_labels
    assert "Suit" in selectbox_labels
