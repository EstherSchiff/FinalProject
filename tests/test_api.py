from unittest.mock import Mock
import pytest
from api_helpers import create_deck, draw_cards, CreateDeckError, DrawCardError
from api import get_secret_card

@pytest.fixture
def card_api_response():
    return {'success': True,
            'deck_id': '2vw2ivgaebo6',
            'cards':
                [{'code': '0D',
                  'image': 'https://deckofcardsapi.com/static/img/0D.png',
                  'images': {'svg': 'https://deckofcardsapi.com/static/img/0D.svg',
                             'png': 'https://deckofcardsapi.com/static/img/0D.png'},
                  'value': '10', 'suit': 'DIAMONDS'}],
            'remaining': 51}

@pytest.fixture
def card_api_response_err():
    return {'success': False,
            'deck_id': '2vw2ivgaebo6',
            'cards':
                [{'code': '0D',
                  'image': 'https://deckofcardsapi.com/static/img/0D.png',
                  'images': {'svg': 'https://deckofcardsapi.com/static/img/0D.svg',
                             'png': 'https://deckofcardsapi.com/static/img/0D.png'},
                  'value': '10', 'suit': 'DIAMONDS'}],
            'remaining': 51}

@pytest.fixture
def simple_api_response():
    return {
        'success': True,
        'deck_id': '2vw2ivgaebo6',
        'shuffled': True,
        'remaining': 52
    }

@pytest.fixture
def fail_api_response():
    return {
        'success': False,
        'deck_id': '2vw2ivgaebo6',
        'shuffled': True,
        'remaining': 52
    }

@pytest.fixture
def mock_requests_get(mocker):
    """
    A fixture that patches requests.get via pytest-mock (mocker).
    Returns the mock object so you can configure it within tests.
    """
    return mocker.patch("requests.get")

# test ensures deck is created with proper api call
def test_create_deck(simple_api_response, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = simple_api_response
    mock_requests_get.return_value = mock_response
    deck_id = create_deck()
    assert deck_id == simple_api_response["deck_id"]
    mock_requests_get.assert_called_once_with("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1", timeout=60)

# test checks that an error is raised if the api request fails
def test_create_deck_err(fail_api_response, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = fail_api_response
    mock_requests_get.return_value = mock_response
    with pytest.raises(CreateDeckError):
        create_deck()

# test checks successful draw cards
def test_draw_cards(card_api_response, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = card_api_response
    mock_requests_get.return_value = mock_response
    deck_id = create_deck()
    cards = draw_cards(deck_id)
    assert cards.json() == card_api_response

# test checks that error is raised when api gives an error
def test_draw_cards_err(card_api_response_err, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = card_api_response_err
    mock_requests_get.return_value = mock_response
    deck_id = '2vw2ivgaebo6'
    with pytest.raises(DrawCardError):
        draw_cards(deck_id)

# test checks that it gets a secret card
def test_get_secret_card(card_api_response, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = card_api_response
    mock_requests_get.return_value = mock_response
    result = get_secret_card()
    assert result == "10D"
