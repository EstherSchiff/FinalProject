from scrape_helpers import get_html, get_table, extract_data, insert_data, URLError
from unittest.mock import patch
import pytest
import requests
from scrape import scrape_cards
from tests.test_database import memory_db


@pytest.fixture
def mock_html():
    return """
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

@pytest.fixture
def mock_table():
    return """
    <table class="wikitable nounderlines Unicode">
            <tr>
                <td title="U+1F0A1: PLAYING CARD ACE OF SPADES">🂡</td>
                <td title="U+1F0B8: PLAYING CARD EIGHT OF CLUBS">🂸</td>
                <td title="U+1F0C1: PLAYING CARD ACE OF DIAMONDS">🃁</td>
            </tr>
    </table>
    """
def test_get_html_success(mocker, mock_html):
    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html

    # Mock requests.get to return the mock response
    mocker.patch('requests.get', return_value=mock_response)

    # Call the function
    result = get_html()

    # Assert that the result is the mocked response text
    assert result == mock_response.text
    assert mock_response.status_code == 200

def test_get_html_fail(mocker, mock_html):
    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = requests.HTTPError
    mock_response.text = mock_html

    # Mock requests.get to return the mock response
    mocker.patch('requests.get', return_value=mock_response)

    with pytest.raises(URLError):
        get_html()

def test_get_table_success(mocker, mock_html):
    mocker.patch("scrape.get_html", return_value=mock_html)
    table = get_table(mock_html)
    assert table is not None
    assert "wikitable" in table["class"]
    assert "🂡" in table.find("td").text

def test_get_table_fail(mocker):
    invalid_html = """
    <html>
        <body>
            <table class="table that doesn't exist">
                <tr><td>🂡</td></tr>
    </html>
    """
    mocker.patch("scrape.get_html", return_value=invalid_html)
    table = get_table(invalid_html)
    assert table is None

@pytest.mark.parametrize("keyword", ["Reserved", "TRUMP", "FOOL", "JOKER", "BACK", "KNIGHT"])
def test_extract_data(mocker, mock_html, keyword):
    mocker.patch("scrape.get_html", return_value=mock_html)
    table = get_table(mock_html)
    result = extract_data(table)
    assert keyword not in result

def test_insert_data(memory_db):
    cards_data = [
        ('U+1F0C2', 'TWO OF DIAMONDS'),
        ('U+1F0C3', 'THREE OF DIAMONDS'),
    ]
    with patch("database.get_code", side_effect=["2D", "3D"]):
        insert_data(cards_data, memory_db)
        guessed_values = memory_db.execute("SELECT unicode, name FROM cards").fetchall()
        assert ('U+1F0C2', 'TWO OF DIAMONDS') in guessed_values
        assert ('U+1F0C3', 'THREE OF DIAMONDS') in guessed_values


@patch('scrape_helpers.insert_card')
@patch('scrape.get_html', return_value=mock_html)
@patch('scrape.get_table', return_value=mock_table)
@patch('scrape.extract_data', return_value=[('U+1F0A1', 'ACE OF SPADES'), ('U+1F0B8', 'EIGHT OF CLUBS'), ('U+1F0C1', 'ACE OF DIAMONDS')])
def test_scrape_cards(mock_extract_data, mock_get_table, mock_get_html, mock_insert, memory_db):
    scrape_cards(memory_db)
    mock_insert.assert_any_call('U+1F0A1', 'ACE OF SPADES', memory_db)
    mock_insert.assert_any_call('U+1F0B8', 'EIGHT OF CLUBS', memory_db)
    mock_insert.assert_any_call('U+1F0C1', 'ACE OF DIAMONDS', memory_db)
