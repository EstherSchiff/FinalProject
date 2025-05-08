from stats import game_stats
from unittest.mock import patch
import matplotlib

# ensures game stats returns a chart
@patch("stats.get_count")
def test_game_stats(mock_get_count):
    mock_get_count.return_value = [(5,), (3,)]
    chart = game_stats()
    assert isinstance(chart, matplotlib.figure.Figure)
    mock_get_count.assert_called_once()
