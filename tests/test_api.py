from unittest.mock import Mock
import pytest
from api import create_deck, draw_cards, get_secret_card, CreateDeckError, DrawCardError

# to get pytest to find the api file
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


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
    return mocker.patch("api.requests.get")


def test_create_deck(simple_api_response, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = simple_api_response
    mock_requests_get.return_value = mock_response
    deck_id = create_deck()
    assert deck_id == simple_api_response["deck_id"]
    mock_requests_get.assert_called_once_with(
        # call api once with this link
        "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")


def test_create_deck_err(fail_api_response, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = fail_api_response
    mock_requests_get.return_value = mock_response
    with pytest.raises(CreateDeckError):
        create_deck()


def test_draw_cards(card_api_response, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = card_api_response
    mock_requests_get.return_value = mock_response
    deck_id = create_deck()
    cards = draw_cards(deck_id)
    assert cards.json() == card_api_response


def test_draw_cards_err(card_api_response_err, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = card_api_response_err
    mock_requests_get.return_value = mock_response
    deck_id = '2vw2ivgaebo6'
    with pytest.raises(DrawCardError):
        draw_cards(deck_id)


def test_get_secret_card(card_api_response, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = card_api_response
    mock_requests_get.return_value = mock_response
    result = get_secret_card()
    assert result == "10D"
