from ai import encourage
from unittest.mock import patch
from emoji import is_emoji

# tests ai response using mocking
@patch("ai.st")
@patch("ai.AzureOpenAI")
def test_encourage(mock_azure, mock_st):
    mock_st.secrets = {"api_keys": {"API_KEY": "fake_key"}}
    mock_azure.return_value.chat.completions.create.return_value = ["You're doing great! You have 2 guesses left. 😊"]
    response = encourage(2)
    mock_azure.assert_called_once()
    full_response = "".join(response)  # combines streamed response
    assert "guesses left" in full_response
    assert any(is_emoji(char) for char in full_response) == True
