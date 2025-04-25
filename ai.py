import streamlit as st
from openai import AzureOpenAI

# function to display an encouraging message to user using AI
def encourage(guesses_left):
    client = AzureOpenAI(
        api_key=st.secrets["api_keys"]["API_KEY"],
        api_version="2024-02-15-preview",
        azure_endpoint="https://streamlit-oai.openai.azure.com/"
    )  # connect to Azure OpenAI

    stream = client.chat.completions.create(
        model="gpt-35-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": (
                    f"""
                    Generate a one-line encouraging message for a player who is playing a card guessing game. Include a cute happy emoji.
                    The message should motivate the player. Tell the user they have {guesses_left} guesses left, but in a positive tone. Don't pressure them that the game is almost over.
                 """
                )
            }
        ],
        stream=True,
    )  # get AI response
    return stream
