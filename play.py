import streamlit as st
from game_logic import initialize_game, load_sidebar, process_guess, display_messages, progress_bar, ai, show_game_stats, check_game_state

def main():
    try:
        # main game flow
        st.header("🃏 Welcome to Card Guesser!")
        initialize_game()
        load_sidebar()
        process_guess()
        display_messages()
        progress_bar()
        ai()
        show_game_stats()
        check_game_state()
    except Exception as e:
        st.toast(f"An unexpected error has occurred: {str(e)} ⚠️")

if __name__ == "__main__":
    main()
