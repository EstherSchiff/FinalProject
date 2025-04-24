import streamlit as st
from openai import AzureOpenAI

# function to display an encouraging message to user using AI
def encourage():
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
                    """
                    Generate a one-line encouraging message for a player who is playing a guessing game.
                    The message should motivate the player regardless of their progress, keeping the tone positive and supportive.
                 """
                )
            }
        ],
        stream=True,
    )  # get AI response
    return stream
