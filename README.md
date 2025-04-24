# Final Project

## Project Overview
This project combines web scraping, API integration, database management, data visualization, and AI interaction to create a Streamlit app for a fun card-guessing game. ChatGPT is used to generate an encouraging message for the user each time they guess. 


## Create Your Environment and Run Locally
**Open the terminal and run the following:**
```bash
git clone https://github.com/EstherSchiff/FinalProject.git
cd FinalProject
```
**Set up a virtual environment (optional) on Windows:**
```bash
python -m venv .venv
source .venv\Scripts\activate
```
**Install dependencies:**
```bash
pip install -r requirements.txt
```
**Run the app locally:**
```bash
streamlit run play.py
```
Streamlit should launch automatically in your browser. If not, you can view it here: http://localhost:8501


## Run Streamlit via Deployment
**You can access the deployed version here:** (https://cardguesser.streamlit.app)

## Deploy Streamlit App Yourself
**Clone the repository:**
```bash
git clone https://github.com/EstherSchiff/FinalProject.git
```
**Sign in to Streamlit**
Visit https://streamlit.io/cloud and sign in with your Github account.

**Create a new app:**
- Click ```new app```
- Select the Github repo and branch
- Set the main file to ```play.py```
- Click ```Deploy```

**Adding an API Key**
Visit https://share.streamlit.io/. Click on the dots for more options. Got to settings>secrets and add you API KEY in this format: 

## Badges
![Tests](https://github.com/EstherSchiff/FinalProject/actions/workflows/run-tests.yml/badge.svg)

## Dependencies
```bash
streamlit
pandas
openai
requests
beautifulsoup4
pytest-cov
pytest
pytest-mock
```
**To install:**
```bash
pip install -r requirements.txt
```
