from unittest.mock import MagicMock, patch

from src.toot import toot_quote, toot_random_quote


@patch("src.toot.Mastodon")
def test_toot_quote(MockMastodon):
    mastodon = MockMastodon()
    mastodon.status_post = MagicMock(return_value=True)
    toot_quote({"id": "testid", "text": "my quote", "attribution": "author name"})
    mastodon.status_post.assert_called_once_with("my quote - author name")


@patch("src.toot.toot_quote")
def test_toot_random_quote(mock_toot_quote):
    mock_toot_quote.return_value = True
    toot_random_quote(fake_wednesday=True)
    mock_toot_quote.assert_called_once()
