import streamlit as st
from game_logic import initialize_game, load_sidebar, process_guess, display_messages, progress_bar, ai, check_game_state

# main game logic
st.header("🃏 Welcome to Card Guesser!")
initialize_game()
load_sidebar()
process_guess()
display_messages()
progress_bar()
ai()
check_game_state()
