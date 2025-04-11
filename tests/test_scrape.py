from scrape import scrape_cards, get_html, get_table, extract_data, URLError
import pytest
import requests


@pytest.fixture
def mock_response():
    return """
<table class="wikitable nounderlines Unicode">
    <tr>
        <td title="U+1F0A1: PLAYING CARD ACE OF SPADES">&#x1f0a1;</td>
    </tr>
    <tr>
        <td title="U+1F0A2: PLAYING CARD TWO OF SPADES">&#x1f0a2;</td>
    </tr>
    <tr>
        <td title="U+1F0A3: PLAYING CARD THREE OF SPADES">&#x1f0a3;</td>
    </tr>
    <tr>
        <td title="U+1F0A4: PLAYING CARD FOUR OF SPADES">&#x1f0a4;</td>
    </tr>
</table>
"""


def test_get_html_success(mocker):
    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = """
    <table class="wikitable nounderlines Unicode">
    <tr>
        <td title="U+1F0A1: PLAYING CARD ACE OF SPADES">&#x1f0a1;</td>
    </tr>
    </table>
    """

    # Mock requests.get to return the mock response
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function
    result = get_html()

    # Assert that the result is the mocked response text
    assert result == mock_response.text
    assert mock_response.status_code == 200


def test_get_html_fail(mocker):
    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = requests.HTTPError
    mock_response.text = """
    <table class="wikitable nounderlines Unicode">
    <tr>
        <td title="U+1F0A1: PLAYING CARD ACE OF SPADES">&#x1f0a1;</td>
    </tr>
    </table>
    """

    # Mock requests.get to return the mock response
    mocker.patch('requests.get', return_value=mock_response)

    with pytest.raises(URLError):
        get_html()


def test_get_table_success(mocker):
    mock_html = """
    <html>
    <body>
        <h1>Some Random Header</h1>
        <p>Random content outside the table.</p>
        <table class="wikitable nounderlines Unicode">
            <tr>
                <td title="U+1F0A1: PLAYING CARD ACE OF SPADES">🂡</td>
                <td title="U+1F0B8: PLAYING CARD EIGHT OF CLUBS">🂸</td>
                <td title="U+1F0C1: PLAYING CARD ACE OF DIAMONDS">🃁</td>
            </tr>
        </table>
    </body>
    </html>
    """
    mocker.patch("scrape.get_html", return_value=mock_html)
    table = get_table(mock_html)
    # assert table.find_all("h1")==0
    assert '' in table
    # continue here################
