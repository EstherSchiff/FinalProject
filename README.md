# Final Project

Project Overview:
This project combines web scraping, API integration, database management, data visualization, and AI interaction to create an engaging card-guessing game. It scrapes a Wikipedia page to get details about standard playing cards and then stores the information in a sqlite database. An additional field is added to the database to show whether each card has been guessed. Using the Deck of Cards API, the app randomly draws a card. The user then submits a guess using the Streamlit interface. The guess is then compared to the drawn card to determine if it's correct. The guessed field in the database is updated and the app shows a progress bar and a display of previously guessed cards. ChatGPT generates an encouraging message for the user each time they guess. When the user wins, a winning message is displayed and balloons float by! If the user runs out of guesses, a losing message is displayed. When the game ends, the submit button becomes disabled, and the user must press New Game to reset and start a new game.

To set up your environment and run the code locally:

## Run Streamlit Locally
1. **Open the terminal and run the following:**
    ```bash
    git clone https://github.com/EstherSchiff/FinalProject.git
    cd FinalProject
    ```

Set up a virtual environment (optional) on Windows:
    python -m venv .venv
    source .venv\Scripts\activate
Install dependencies:
    pip install -r requirements.txt
Run the app:
    streamlit run play.py
Streamlit should launch automatically in your browser. If not, you can view it here: http://localhost:8501



To use the Streamlit app via deployment:

I integrated ChatGPT by...

Badge (coverage or tests passing):

This application requires ___________. You can install them by ____________.