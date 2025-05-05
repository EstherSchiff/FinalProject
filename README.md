# Card Guesser  
![Tests](https://github.com/EstherSchiff/FinalProject/actions/workflows/run-tests.yml/badge.svg)

## Project Overview
**Card Guesser** is an interactive Streamlit app that combines web scraping, API integration, and database management to create a fun card-guessing game. It scrapes Wikipedia to get details on playing cards which are stored in an SQLite3 database. The app selects a random card using the Deck of Cards API and challenges the user to guess it. The user’s guesses are tracked and progress bar shows users how far the game has come.

To enhance the user experience, ChatGPT is integrated to provide personalized, encouraging messages after each guess, making the game more engaging and interactive.

## Run Streamlit via Deployment
**You can access the deployed version here:** (https://cardguesser.streamlit.app)

## Deploy Streamlit App Yourself
**Fork the repository:**
Visit https://github.com/EstherSchiff/FinalProject.git and fork the repository.

**Sign in to Streamlit:**
Visit https://streamlit.io/cloud and sign in with your Github account.

**Create a new app:**
- Click ```create app```
- Select the Github repo and branch
- Set the main file to ```play.py```
- Click ```Deploy```

**Adding an API Key**
- Visit https://share.streamlit.io/
- Click on the dots for more options
- Go to settings>secrets and add your API KEY in this format:
```bash
[api_keys]
API_KEY = "addkeyhere"
```

## Running on Codespace
**Fork the Repository:**
Visit https://github.com/EstherSchiff/FinalProject.git and fork the repository. 

**Create a Codespace:**
Go to your forked repo and click Code > Open with Codespaces > New codespace.  

**Add API Key:**  
In the terminal, run the following code to make the necessary file and folder:
```bash
mkdir .streamlit
```
```bash
touch .streamlit/secrets.toml
```
Add this to the secrets.toml file:
```bash
[api_keys]
API_KEY = "addkeyhere"
```

## Dependencies
`beautifulsoup4`- parsing HTML and web scraping  
`emoji`- working with emojis in Python strings  
`openai`- interacting with OpenAI’s API and accessing GPT models  
`pytest`- testing framework  
`pytest-cov`- pytest plug-in for coverage reports  
`pytest-mock`- mocking in test  
`requests`- handles HTTP requests  
`streamlit`- web application framwork  

**To install:**
```bash
pip install -r requirements.txt
```
